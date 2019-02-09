require "pal"
require "font"

-- TODO REFACTOR 128 (bank width)

--------------------------------------------------------------------------------

function get_tile(b,s,w,h,colorkey,raw)
	w=w or 1
	h=h or 1
	local bw = math.floor(banks[b]:getWidth()/8)
	local x,y = s%bw, math.floor(s/bw)
	local tile = love.image.newImageData(w*8,h*8)
	tile:paste(banks[b],0,0,x*8,y*8,w*8,h*8)
	--tile:encode('png','xxx.png')
	
	if not raw then tile = love.graphics.newImage(tile) end
	return tile
end

function col_to_rgba(c)
	if c==0 then
		return {0,0,0,0}
	else
		return {c/255,0,0,1}
	end
end

-- TODO
function rgb_to_col(r,g,b)
	for c,col in pairs(colors) do
		if col[1]/255==r and col[2]/255==g and col[3]/255==b then return c-1 end
	end
end

function set_col(c)
	c=c or COLOR
	love.graphics.setColor(col_to_rgba(c))
end

-- TODO REFACTOR
function bank_from_text(b,text,chars,values,w,h,eol)
	w=w or 128
	h=h or 128
	eol=eol or ';'
	local img = love.image.newImageData(w,h)
	local c,ch,bc
	local x,y = 0,0
	local val = {}
	for i = 1,#chars do
		val[chars:sub(i,i)] = values[i]
	end
	for i = 1,#text do
		ch = text:sub(i,i)
		if ch==eol then
			y=y+1
			x=0
		end
		c = val[ch]
		if c then 
			bc = c / 255
			--img:setPixel(x,y,bc,0,0,1) -- unpack(col_to_rgba)
			img:setPixel(x,y,unpack(col_to_rgba(c))) -- unpack(col_to_rgba)
			x=x+1
		end
	end
	banks[b]=img
end

-- TODO REFACTOR
function map_from_text(text,chars,values,w,h,eol)
	eol=eol or ';'
	local val = {}
	local out = {}
	local x,y = 0,0
	local t,ch
	for i=1,#chars do
		val[chars:sub(i,i)] = values[i]
	end
	for i = 1,#text do
		ch = text:sub(i,i)
		if ch==eol then
			y=y+1
			x=0
		end
		t = val[ch]
		if t then
			out[y*w+x] = t
			x=x+1
		end
	end
	out['w']=w
	out['h']=h
	return out
end


function img_from_page(p,b,remap)
	b=b or BANK
	p=p or PAGE
	local _draw = love.graphics.draw
	local key = PAGE -- TODO key=p+b
	local img = map_cache[key]
	if remap then img = nil end
	if not img then
		local t,tile
		local w = pages[PAGE]['w']
		local h = pages[PAGE]['h']
		img = love.image.newImageData(w*8,h*8)
		for x = 0,w-1 do
			for y = 0,h-1 do
				t = pages[PAGE][y*w+x]
				if remap then
					t = remap(t,x,y)
				end
				if t then 
					tile = get_tile(b,t,1,1,nil,true)
					img:paste(tile,x*8,y*8,0,0,8,8)
				end
			end
		end
		map_cache[key] = img
	end
	return img
end

-- TODO separate calc_width function
function font_from_text(text,w,h,fg,bg,eol)
	local cnv = love.graphics.newCanvas(128,128)
	cnv:renderTo(function ()
					love.graphics.clear({0,0,0,0}) -- TODO colorkey
				end)
	local img = cnv:newImageData()
	local j,x,y,s = 0,0,0
	font_width = {} -- GLOBAL
	font_height = h
	for i=0,255 do font_width[i]=0 end
	local ch
	for i = 1,#text do
		ch = text:sub(i,i)
		s = math.floor(x/8) + math.floor(y/8)*16
		if ch==fg then
			img:setPixel(x,y,{1,1,1,1}) -- TODO color
			font_width[s] = math.max(font_width[s], 1+x%8)
			x=x+1
			if x%8 >= w then x = x + 8-x%8 end
		elseif ch==bg then
			x=x+1
			if x%8 >= w then x = x + 8-x%8 end
		elseif ch==eol then
			y=y+1
			x=0
		end
	end
	return img
end

function export_bank(b,path)
	banks[b]:encode('png',path)
end

function import_bank(b,path)
	local bank = love.image.newImageData(128,128)
	local img = love.image.newImageData(path)
	bank:paste(img,0,0,0,0,128,128)
	banks[b] = bank
end

recolor_code = [[
	extern vec4 colors[256];
	vec4 effect( vec4 color, Image texture, vec2 texture_coords, vec2 screen_coords )
	{
		vec4 orig_color = Texel(texture, texture_coords);
		int c = int(orig_color[0]*255);
		return colors[c];
	}
]]
recolor_shader = love.graphics.newShader(recolor_code)
-- shader:sendColor('colors',unpack(rgba))

function update_shader()
	local rgba = {}
	local c
	for i=0,255 do
		c = colors[i]
		if c then
			rgba[i] = {c[1]/255,c[2]/255,c[3]/255,1}
			trace('UPDATE_SHADER',i,c[1],c[2],c[3])
		else
			rgba[i] = {0,0,0,0}
		end
	end
	recolor_shader:sendColor('colors',unpack(rgba))
end


---[ API ]----------------------------------------------------------------------

-- TODO KWARGS fixed scale sim xspace yspace
-- TODO return value
trace=print
function print(text,x,y,c,xmax,xmin,sim)
	c=c or COLOR
	x=x or CURX
	y=y or CURY
	xmin=xmin or x
	xmax=xmax or scrw
	local ch,ch2
	local s
	local skip = 0
	local c_orig = c
	text=string.upper(text)
	for i=1,#text do
		if skip>0 then
			skip=skip-1
			goto continue
		end
		ch = text:sub(i,i)
		s = string.byte(ch)
		if ch=='\n' then -- EOL
			x=xmin
			y=y+font_height+2
		elseif ch=='^' then
			ch2=text:sub(i+1,i+1)
			if ch2>='0' and ch2<='9' then
				c = tonumber(ch2)
				skip = 1
			elseif ch2=='^' then 
				c = c_orig
				skip = 1
			end
		elseif s then
			local w = font_width[s]
			if x > xmax or x+w > xmax then
				x=xmin
				y=y+font_height+2
			end
			shadow(s,x,y,1,1,c,FONT_BANK)
			if w==0 then w=5 else w=w+1 end
			x=x+w
		else
			x=x+5
		end
		CURX = x
		::continue::
		-- TODO CURY
	end
	return x,y+font_height+1
end

function cursor(x,y)
	if x==nil and y==nil then
		CURX,CURY = 0,0
	else
		if x then CURX=x end
		if y then CURY=y end
	end
end

function bank(b) BANK=b end
function page(p) PAGE=p end
function camera(x,y)
	camx = -x
	camy = -y
end

-- TODO rest of args
function shadow(s,x,y, w,h, c,b)
	w=w or 1
	h=h or 1
	b=b or BANK
	cr,cg,cb,ca = col_to_rgba(c or COLOR)
	
	-- get_shadow TODO refactor
	local bw = math.floor(banks[b]:getWidth()/8)
	local bx,by = s%bw, math.floor(s/bw)
	local tile = love.image.newImageData(w*8,h*8)
	tile:paste(banks[b],0,0,bx*8,by*8,w*8,h*8)
	function use_colorkey(x,y,r,g,b,a)
		if a>0
			then return cr,cg,cb,1
			else return 0,0,0,0
		end
	end
	tile:mapPixel(use_colorkey)
	
	love.graphics.setColor(1,1,1,1) -- required for colors to be ok
	love.graphics.draw(love.graphics.newImage(tile), x+camx, y+camy)
end 

-- draw sprite by id, can scale, flip, rotate and sheer
function spr(s,x,y, w,h, flip,scale, b)
	w = w or 1
	h = h or 1
	b = b or BANK
	flip = flip or 0
	scale = scale or 1
	
	local key = table.concat({b,s,COLORKEY,w,h},':')
	local img = spr_cache[key]
	if not img then
		img = get_tile(b,s,w,h,COLORKEY)
		spr_cache[key] = img
	end

	local scale_x,scale_y = scale,scale
	local ori_x,ori_y = 0,0
	if flip==1 or flip==3 then
		scale_x = -scale
		ori_x = 8*w
	end
	if flip==2 or flip==3 then
		scale_y = -scale
		ori_y = 8*h
	end

	love.graphics.setColor(1,1,1,1) -- required for colors to be ok
	love.graphics.draw(img, x+camx, y+camy,
		0, scale_x, scale_y, ori_x, ori_y)
end

function rectfill(x,y,w,h,c)
	set_col(c)
	love.graphics.rectangle('fill',x+camx,y+camy,w,h)
end
function rect(x,y,w,h,c)
	set_col(c)
	love.graphics.rectangle('line',x+camx,y+camy,w,h)
end

function circfill(x,y,r,c)
	set_col(c)
	love.graphics.circle('fill',x+camx,y+camy,r)
end
function circ(x,y,r,c)
	set_col(c)
	love.graphics.circle('line',x+camx,y+camy,r)
end

function pget(x,y)
	love.graphics.setCanvas()
	local img = scr:newImageData(nil,nil,x,y,1,1)
	love.graphics.setCanvas(scr)		
	local r,g,b,a = img:getPixel(0,0)
	return rgb_to_col(r,g,b) -- TODO
end

function pset(x,y,c)
	set_col(c)
	love.graphics.points(x+camx,y+camy)
end

function line(x0,y0,x1,y1,c)
	set_col(c)
	love.graphics.line(x0+camx,y0+camy,x1+camx,y1+camy)
end

function trifill(x1,y1,x2,y2,x3,y3,c)
	set_col(c)
	love.graphics.polygon('fill',x1+camx,y1+camy,x2+camx,y2+camy,x3+camx,y3+camy)
end
function tri(x1,y1,x2,y2,x3,y3,c)
	set_col(c)
	love.graphics.polygon('line',x1+camx,y1+camy,x2+camx,y2+camy,x3+camx,y3+camy)
end


function cls(c)
	local c = c or 1
	love.graphics.clear(col_to_rgba(c))
	cursor()
	clip()
end

function clip(x,y,w,h)
	if true then return else
		-- ERROR
		if x then 
			love.graphics.setScissor(x*scrs,(scrh-y-h)*scrs,w*scrs,h*scrs) -- camx camy ???
		else
			love.graphics.setScissor(0,0,scrw*scrs,scrh*scrs)
		end
	end
end

function screen(w,h,s,pal)
	s=s or scrs
	w=w or scrw
	h=h or scrh
	scrw,scrh = w,h
	scrs = s
	if pal then
		colors = {}
		local c=1
		local r,g,b
		for r,g,b in string.gmatch(pal,'#(%w%w)(%w%w)(%w%w)') do
			trace('COLORS',c,r,g,b)
			colors[c] = {tonumber(r,16),tonumber(g,16),tonumber(b,16)} -- TODO x/255
			trace('COLORS',c,unpack(colors[c]))
			c=c+1
		end
		MAX_COLOR = c-1
		trace('MAX_COLOR',MAX_COLOR)
	end
	love.window.setMode(w*s,h*s)
	update_shader()
end

function fps()
	return love.timer.getFPS()
end


function pal(c,r,g,b)
	-- TODO
end

function color(c)
	COLOR=c
	set_col(c)
end

-- TODO invalidate cache
function transparent(c)
	COLORKEY=c
end

---[ MAP ]----------------------------------------------------------------------

function map(x,y,p,remap)
	x=x or 0
	y=y or 0
	p=p or PAGE
	img = img_from_page(p,MAP_BANK,remap)
	love.graphics.setColor(1,1,1,1)
	love.graphics.draw(love.graphics.newImage(img),x+camx,y+camy)
end

function mget(mx,my)
	local w = pages[PAGE]['w']
	return pages[PAGE][my*w+mx]
end

function mset(mx,my,t)
	local w = pages[PAGE]['w']
	pages[PAGE][my*w+mx] = t
	-- invalidate cache TODO key=p+b
	map_cache[PAGE] = nil
end

---[ INPUT ]--------------------------------------------------------------------

function key(k)
	return love.keyboard.isDown(k)
end

function keyp(k)
	local d = love.keyboard.isDown(k)
	local p = PRESSED[k] 
	if d and not p then
		PRESSED[k] = 1
		return true
	elseif p and not d then
		PRESSED[k] = nil
	end
	return false
end

function mouse()
	local mx,my,b1,b2,b3
	b1 = love.mouse.isDown(1)
	b2 = love.mouse.isDown(2)
	b3 = love.mouse.isDown(3)
	mx,my = love.mouse.getPosition() 
	mx = math.floor(mx/scrs)
	my = math.floor(my/scrs)
	return {mx,my,b1,b2,b3}
end


-------------------------------------------------------------------------
-------------------------------------------------------------------------
-------------------------------------------------------------------------

-- TODO love.graphics.setBackgroundColor

function INIT(args,raw_args) end
function MAIN() end
function DRAW() end
function OVER() end -- TODO
function SCAN() end -- TODO
function POST() end -- TODO

function love.load(args,raw_args)
	BANK = 1
	PAGE = 1
	COLORKEY = 0
	COLOR = 1
	CURX,CURY = 0,0 -- cursor
	camx,camy = 0,0 -- TODO upper
	scrw,scrh = 320,200 -- TODO upper
	scrs = 2 -- TODO upper
	spr_cache={}
	map_cache={}
	banks={}
	pages={}
	PRESSED={}
	SPR_BANK = 1
	MAP_BANK = 2
	FONT_BANK = 3
	MAX_COLOR = 16
	banks[FONT_BANK] = font_from_text(moki4x,5,5,'X','.','-')
	colors=pal_chromatic -- TODO upper
	love.graphics.setLineStyle('rough')
	love.graphics.setDefaultFilter('nearest','nearest')
	screen(scrw,scrh,scrs)
	
	for i,arg in pairs(args) do
		trace('arg',i,arg)
	end
	local mod = args[1]
	if mod then 
		package.path = package.path .. ";..;?.lua"
		require(mod)
	end
	
	INIT(args,raw_args)
	
	scr = love.graphics.newCanvas(scrw,scrh)
end

function love.update()
	MAIN()
end

function love.draw()
	-- BEFORE
	love.graphics.setCanvas(scr)
	love.graphics.setShader(recolor_shader)
	
	DRAW()
	
	-- AFTER
	love.graphics.setShader()
	love.graphics.setCanvas()
	love.graphics.setColor(1,1,1,1) -- TODO store+restore color
	love.graphics.draw(scr,0,0,0, scrs,scrs)
	POST()
	
	if key("f6") then love.graphics.captureScreenshot('screen.png') end
end


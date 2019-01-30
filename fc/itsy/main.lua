require "pal"
require "font"

--------------------------------------------------------------------------------

function get_tile(b,s,w,h,colorkey,raw)
	w=w or 1
	h=h or 1
	colorkey=colorkey or COLORKEY
	local bw = math.floor(banks[b]:getWidth()/8)
	local x,y = s%bw, math.floor(s/bw)
	local tile = love.image.newImageData(w*8,h*8)
	tile:paste(banks[b],0,0,x*8,y*8,w*8,h*8)
	if colorkey and colorkey>=0 then
		
		-- TODO wybrac szybsza metode
		
		rk,gk,bk = col_to_rgb(colorkey)
		function use_colorkey(x,y,r,g,b,a)
			if r==rk and g==gk and b==bk
				then return 0,0,0,0
				else return r,g,b,1
			end
		end
		tile:mapPixel(use_colorkey)
		
		--[[
		local rk,gk,bk = col_to_rgb(colorkey)
		local r,g,b
		for x = 0,(w*8)-1 do
			for y = 0,(h*8)-1 do
				r,g,b = tile:getPixel(x,y)
				if r==rk and g==gk and b==bk then
					trace('match',x,y,r,g,b)
					tile:setPixel(x,y,0,0,0,0)
				end
			end
		end
		]]
	end
	if raw then
		return tile
	else
		return love.graphics.newImage(tile)
	end
end

function col_to_rgb(c)
	local c = c or 1
	local col = colors[c+1]
	if col then
		return col[1]/255,col[2]/255,col[3]/255
	else
		return 0,0,0,0
	end
end

function rgb_to_col(r,g,b)
	for c,col in pairs(colors) do
		if col[1]/255==r and col[2]/255==g and col[3]/255==b then return c-1 end
	end
end

function set_col(c)
	c=c or COLOR
	love.graphics.setColor(col_to_rgb(c))
end

function img_from_text(text,w,h,colormap)
	local img = love.image.newImageData(w,h)
	local c,ch
	local map={}
	for i = 1,#colormap do
		ch = colormap:sub(i,i)
		map[ch] = i-1
	end
	local j = 0
	for i = 1,#text do
		ch = text:sub(i,i)
		c = map[ch]
		if c then 
			y = math.floor(j/w)
			x = j%w
			img:setPixel(x,y,col_to_rgb(c))
			j=j+1
		end
	end
	return img
end

function map_from_text(text,w,h,chars,values)
	local val = {}
	local out = {}
	local j = 0
	local t,ch
	for i=1,#chars do
		val[chars:sub(i,i)] = values[i]
	end
	for i = 1,#text do
		ch = text:sub(i,i)
		t = val[ch]
		if t then
			y = math.floor(j/w)
			x = j%w
			out[y*w+x] = t
			j=j+1
		end
	end
	out['w']=w
	out['h']=h
	return out
end

-- w can be filename
function set_bank(b,w,h)
	banks[b] = love.image.newImageData(w,h)
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

---[ API ]----------------------------------------------------------------------

-- NEW
-- TODO ARGS fixed scale
trace=print
function print(text,x,y,c,xmax,xmin)
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
			shadow(s,x,y,c,1,1,FONT_BANK)
			if w==0 then w=5 else w=w+1 end
			x=x+w
		else
			x=x+5
		end
		CURX = x
		::continue::
		-- TODO CURY
	end
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
	camx = x
	camy = y
end

-- TODO rest of args
function shadow(s,x,y,c, w,h, b)
	w=w or 1
	h=h or 1
	b=b or BANK
	cr,cg,cb = col_to_rgb(c or COLOR)
	
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
function spr(s,x,y, w,h, scale,flip,rotate,sx,sy, b)
	w = w or 1
	h = h or 1
	b = b or BANK
	flip = flip or 0
	rotate = rotate or 0
	
	local key = table.concat({b,s,COLORKEY,w,h},':')
	local img = spr_cache[key]
	if not img then
		img = get_tile(b,s,w,h,COLORKEY)
		spr_cache[key] = img
	end

	local ori_x = 0
	local ori_y = 0

	local scale_x = scale or 1
	local scale_y = scale or 1
	if flip==1 or flip==3 then
		ori_x = w*8
		scale_x = -scale_x
	end
	if flip==2 or flip==3 then 
		ori_y = h*8
		scale_y = -scale_y
	end

	if rotate==1 then
		if ori_y>0 then ori_y=0 else ori_y=h*8 end
		rotate = math.pi/2
	elseif rotate==2 then
		if ori_y>0 then ori_y=0 else ori_y=h*8 end
		if ori_x>0 then ori_x=0 else ori_x=w*8 end
		rotate = math.pi
	elseif rotate==3 then
		if ori_x>0 then ori_x=0 else ori_x=w*8 end
		rotate = math.pi*3/2
	end

	love.graphics.setColor(1,1,1,1) -- required for colors to be ok
	love.graphics.draw(img, x+camx, y+camy,
		rotate, scale_x, scale_y,
		ori_x, ori_y, sx, sy)
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

-- TODO bank 0 or nil = screen
function pget(x,y,b)
	love.graphics.setCanvas()
	local img = scr:newImageData(nil,nil,x,y,1,1)
	love.graphics.setCanvas(scr)		
	local r,g,b,a = img:getPixel(0,0)
	return rgb_to_col(r,g,b)
end

-- TODO bank 0 or nil = screen
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
	local c = c or 0
	love.graphics.clear(col_to_rgb(c))
	cursor()
	clip()
end

function clip(x,y,w,h)
	if x then 
		love.graphics.setScissor(x,y,w,h) -- camx camy ???
	else
		love.graphics.setScissor(0,0,scrw,scrh)
	end
end

function screen(w,h,s)
	s=s or 1
	scrw,scrh = w,h
	scrs = s
	love.window.setMode(w*s,h*s)
end

function fps()
	return love.timer.getFPS()
end


function pal(c,r,g,b)
	local col = colors[c+1]
	local r0=col[1]/255
	local g0=col[2]/255
	local b0=col[3]/255
	colors[c+1] = {r,g,b}
	-- invalidate cache
	map_cache = {}
	spr_cache = {}
	-- recode banks
	for i,bank in pairs(banks) do
		banks[i]:mapPixel(
			function (x,y,rr,gg,bb,aa)
				if rr==r0 and gg==g0 and bb==b0
					then return r/255,g/255,b/255,1
					else return rr,gg,bb,1
				end
			end
		)
	end
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
	screen(scrw,scrh,scrs)
	spr_cache={}
	map_cache={}
	banks={}
	pages={}
	SPR_BANK = 1
	MAP_BANK = 2
	FONT_BANK = 3
	banks[FONT_BANK] = font_from_text(moki4x,5,5,'X','.','-')
	colors=pal_chromatic -- TODO upper
	love.graphics.setLineStyle('rough')
	love.graphics.setDefaultFilter('nearest','nearest')
	
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
	
	DRAW()
	
	-- AFTER 
	love.graphics.setCanvas()
	love.graphics.setColor(1,1,1,1) -- TODO store+restore color
	love.graphics.draw(scr,0,0,0, scrs,scrs)
	POST()
	
	if key("f6") then love.graphics.captureScreenshot('screen.png') end
end


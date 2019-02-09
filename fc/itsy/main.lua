-- TODO: upto 32 colors
-- TODO: spr-pico8 sprite api
-- NEW: one bank for spr and tile

-- DONE [TEXT]  -> print, font_from_img
-- DONE [BANK]  -> fget, fset
-- DONE [GIF]   -> gif encoder by gamax92 -> https://github.com/gamax92/picolove/blob/master/gif.lua

-- TODO [DRAW]  -> pal, palt, clip, fillp
-- TODO [MAP]   -> mget, mset, map, map_from_text
-- TODO [INPUT] -> btn, btnp, touch

local bit = require('bit')


--[ SCREEN MODE ]---------------------------------------------------------------


PAL_DEFAULT = [[
		#140c1c
		#442434
		#30346d
		#4e4a4e
		#854c30
		#346524
		#d04648
		#757161
		#597dce
		#d27d2c
		#8595a1
		#6daa2c
		#d2aa99
		#6dc2ca
		#dad45e
		#deeed6
	]]


function screen(w,h,s,pal)
	s=s or SCRS
	w=w or SCRW
	h=h or SCRH
	SCRW = w
	SCRH = h
	SCRS = s
	if pal then
		PAL = {} -- 1-base index
		local c=1
		local r,g,b
		local DENOM = 255
		for r,g,b in string.gmatch(pal,'#(%w%w)(%w%w)(%w%w)') do
			printh('pal',c,r,g,b)
			PAL[c] = {
				tonumber(r,16)/DENOM,
				tonumber(g,16)/DENOM,
				tonumber(b,16)/DENOM,
				255/DENOM}
			printh('PAL',c,unpack(PAL[c]))
			c=c+1
		end
		update_shader()
	end
	love.window.setMode(w*s,h*s)
end

function external_rgba(c)
	local rgba = PAL[c+1]
	if not rgba then rgba = {0,0,0,0} end
	return rgba
end

-- TODO transparent
function internal_rgba(c)
	if ((c>=0) and (c<=15)) then 
		local C_TO_F = 17/255 -- 255/15==17
		local v = c*C_TO_F
		return {v,v,v,1}
	else
		return {1,0,0,1} -- invalid color
	end
end

-- TODO a
-- TODO missing
function internal_rgba_to_color(r,g,b,a)
	local F_TO_C = 255/17
	return int(r*F_TO_C)
end

function set_col(c)
	c=c or COLOR
	love.graphics.setColor(internal_rgba(c))
end

recolor_code = [[
	extern vec4 colors[16]; // 0-based index !!
	vec4 effect( vec4 color, Image texture, vec2 texture_coords, vec2 screen_coords )
	{
		vec4 orig_color = Texel(texture, texture_coords);
		float F_TO_C = 255/17;
		int c = int(orig_color[0]*F_TO_C);
		vec4 rgba = colors[c];
		return rgba;
	}
]]
recolor_shader = love.graphics.newShader(recolor_code)

function update_shader()
	printh('UPDATE_SHADER',unpack(PAL))
	recolor_shader:send('colors',unpack(PAL))
end

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--[ DRAW ]----------------------------------------------------------------------


function cls(c)
	local c = c or 0
	love.graphics.clear(internal_rgba(c))
end

function camera(x,y)
	camx = -x
	camy = -y
end

function color(c)
	COLOR = c or COLOR
end

-- RECTANGLE
function rectfill(x,y,w,h,c)
	set_col(c)
	love.graphics.rectangle('fill',x+CAMX,y+CAMY,w,h)
end
function rect(x,y,w,h,c)
	set_col(c)
	love.graphics.rectangle('line',x+CAMX,y+CAMY,w,h)
end
-- CIRCLE
function circfill(x,y,r,c)
	set_col(c)
	love.graphics.circle('fill',x+camx,y+camy,r)
end
function circ(x,y,r,c)
	set_col(c)
	love.graphics.circle('line',x+camx,y+camy,r)
end
-- TRIANGLE
function trifill(x1,y1,x2,y2,x3,y3,c)
	set_col(c)
	love.graphics.polygon('fill',x1+camx,y1+camy,x2+camx,y2+camy,x3+camx,y3+camy)
end
function tri(x1,y1,x2,y2,x3,y3,c)
	set_col(c)
	love.graphics.polygon('line',x1+camx,y1+camy,x2+camx,y2+camy,x3+camx,y3+camy)
end
-- LINE
function line(x0,y0,x1,y1,c)
	set_col(c)
	love.graphics.line(x0+camx,y0+camy,x1+camx,y1+camy)
end
-- POINT
function pget(x,y)
	local F_TO_C = 255/17
	love.graphics.setCanvas()
	local img = SCR:newImageData(nil,nil,x,y,1,1)
	love.graphics.setCanvas(SCR)		
	local r,g,b,a = img:getPixel(0,0)
	return internal_rgba_to_color(r,g,b,a)
end
function pset(x,y,c)
	set_col(c)
	love.graphics.points(x+CAMX,y+CAMY)
end

function pal(c0,c1,p)
	-- TODO
end
function palt(c,t)
	-- TODO
end

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--[ BANKS ]---------------------------------------------------------------------

-- TODO cache ???
function get_tile(s,w,h,raw)
	local bw = math.floor(BANKS[BANK]:getWidth()/TILW)
	local bx,by = s%bw, math.floor(s/bw)
	local tile = love.image.newImageData(w*TILW, h*TILW)
	tile:paste(BANKS[BANK], 0, 0, bx*TILW, by*TILW, w*TILW, h*TILW)
	if not raw then tile = love.graphics.newImage(tile) end -- ERROR przestaje dzialac dla 4x4 !!!
	return tile
end 

function sprite(s,x,y,fx,fy,rot,scale,w,h)
	rot=rot or 0 -- rotation https://en.wikipedia.org/wiki/Turn_(geometry)
	w=w or 1
	h=h or 1
	scale=scale or 1
	local img = get_tile(s,w,h)
	local ox,oy = w*TILW/2, h*TILW/2
	if fx==true or fx==1 then fx=1 else fx=-1 end
	if fy==true or fy==1 then fy=1 else fy=-1 end
	love.graphics.setColor(1,1,1,1) -- required for colors to be ok
	love.graphics.draw(img, x+CAMX, y+CAMY,
		rot, fx*SPRS*scale, fy*SPRS*scale, ox, oy)
end

-- TEST
function sget(x,y)
	local img = BANKS[BANK]
	local r,g,b,a = img:getPixel(x,y)
	return internal_rgba_to_color(r,g,b,a)
end
-- TEST
function sset(x,y,c)
	local img = BANKS[BANK]
	img:setPixel(x,y,unpack(internal_rgba(c)))
end

function fget(n,f)
	local v = FLAGS[n]
	if not v then return false end
	if f then
		return bit(n,f)
	else
		return v
	end
end

-- TODO int vs bool v
function fset(n,f,v)
	if fget(n,f)==v then
	else
		if v then FLAGS[n] = FLAGS[n] + 2^f
			 else FLAGS[n] = FLAGS[n] - 2^f
		end
	end
end

-- TODO REFACTOR
-- TODO move to ASSETS section ???
function img_from_text(text,chars,values,w,h,eol)
	w=w or 128
	h=h or 128
	eol=eol or ';'
	local img = love.image.newImageData(w,h)
	local c,ch
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
			img:setPixel(x,y,unpack(internal_rgba(c)))
			x=x+1
		end
	end
	return img
end

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--[ MAP ]-----------------------------------------------------------------------


function map(x,y,p,remap)
	-- TODO
end

function mget(mx,my)
	-- TODO
end

function mset(mx,my,t)
	-- TODO
end

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--[ TEXT ]----------------------------------------------------------------------


_print=print

function printh(str,filename,overwrite)
	-- TODO filename
	-- TODO overwrite
	if filename=='@clip' then
		love.system.setClipboardText(str)
	else
		_print(str)
	end
end

-- TODO recolor jako shader
function print(str,x,y,c,scale)
	CURX = x
	CURY = y
	local skip = 0
	for i=1,#str do
		local ch = str:sub(i,i)
		if ch=='\n' then
			x = CURX
			y = y + 5*scale + 1*scale -- TODO font_height
		else
			local w = letter(ch,x,y,c,scale)
			x = x + w*scale + 1*scale -- TODO SPACING
		end
	end
	CURX = x
	CURY = y
end

function cursor(x,y)
	if x==nil and y==nil then
		CURX,CURY = 0,0
	else
		if x then CURX=x end
		if y then CURY=y end
	end
end



function font_from_img(img,w,h,s,chars)
	for i=1,#chars do
		local max_x = 0

		local bw = math.floor(img:getWidth()/w)
		local bx,by = s%bw, math.floor(s/bw)
		local tile = love.image.newImageData(w, h)
		tile:paste(img, 0, 0, bx*w, by*h, w, h)

		for y=0,h-1 do
			for x=0,w-1 do
				local r,g,b,a = tile:getPixel(x,y)
				if r>0 then
					max_x = math.max(x,max_x)
				end
			end
		end
		local tile2 = love.image.newImageData(max_x+1,h)
		tile2:paste(tile,0,0,0,0,max_x+1,h)
		local ch = chars:sub(i,i)
		FONT[ch] = tile2
		s=s+1
	end
end

function letter(ch,x,y,color,scale)
	scale = scale or 1
	color = color or COLOR
	local glyph = FONT[ch]
	if not glyph then
		CURX=CURX+5*scale -- TODO space width
		return
	end
	local w,h = glyph:getWidth(), glyph:getHeight()
	local img = love.image.newImageData(w,h)
	img:paste(glyph,0,0,0,0)
	function recolor(x,y,r,g,b,a)
		if r>0 then return unpack(internal_rgba(color))
		       else return 0,0,0,0
		end
	end
	img:mapPixel(recolor) -- TODO preserve colors
	img = love.graphics.newImage(img)
	-- TODO cache
	love.graphics.setColor(1,1,1,1) -- required for colors to be ok
	love.graphics.draw(img, x+CAMX, y+CAMY,
		0, scale, scale)
	return w,h
end

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--[ INPUT ]---------------------------------------------------------------------


function key(k)
	return love.keyboard.isDown(k)
end

-- TODO delay+cycle
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
	-- b3 = love.mouse.isDown(3)
	mx,my = love.mouse.getPosition()
	mx = math.floor(mx/SCRS)
	my = math.floor(my/SCRS)
	return {mx,my,b1,b2}
end

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--[ TABLES ]--------------------------------------------------------------------


function add(t,v)
	table.add(t,v)
end

function del(t,v)
	table.delete(t,v)
end

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--[ INFO ]----------------------------------------------------------------------


function fps()
	return love.timer.getFPS()
end

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
--[ BIT OPERATIONS ]------------------------------------------------------------


function bit(v,b)
	-- b=0 -> LSB
	local is_set = math.floor(v/(2^b))%2==1
	if is_set then return 1 else return 0 end
end

function binary(v,bits)
	bits=bits or 8
	local str = ''
	for b=bits-1,0,-1 do
		str = str..bit(v,b)
	end
	return str
end

--------------------------------------------------------------------------------

local gif = require('gif')

function _init(args,raw_args) end
function _update() end
function _draw() end

function _reset()
	BANK = 1
	PAGE = 1 -- TODO rename to ROOM ???
	COLORKEY = 1 -- TODO colorkey vs palt vs TRAN
	COLOR = 2 -- default color
	CURX,CURY = 0,0 -- cursor
	CAMX,CAMY = 0,0 -- camera
	SCRW,SCRH = 320,200 -- screen width,height
	SCRS = 1 -- screen scale
	TILW = 8 -- tile width
	SPRS = 3 -- sprite scale
	LINW = 1 -- line width
	BANKS={}
	PRESSED={}
	FLAGS={}
	FONT={}
	PAL = {}
	SPR_BANK = 1
	MAP_BANK = 2
	FONT_BANK = 3
	MAX_COLOR = 0
	
	love.graphics.setLineStyle('rough')
	love.graphics.setLineWidth(LINW)
	love.graphics.setDefaultFilter('nearest','nearest')
	SCR = love.graphics.newCanvas(SCRW,SCRH)
	screen(SCRW,SCRH,SCRS,PAL_DEFAULT)
end

function love.load(args,raw_args)
	_reset()
	
	-- for i,arg in pairs(args) do
		-- printh('arg',i,arg)
	-- end
	-- local mod = args[1]
	-- if mod then 
		-- package.path = package.path .. ";..;?.lua"
		-- require(mod)
	-- end
	
	_init(args,raw_args)
end

function love.update()
	_update()
end

rec=nil
function love.draw()
	if keyp('f6') then
		if rec then
			rec:close()
			rec = nil
		else
			config = {}
			config.palette = {}
			config.palette2 = {}
			for c=0,15 do
				local r,g,b,a = unpack(internal_rgba(c))
				config.palette[c+1] = {r*255,g*255,b*255}
				local r,g,b,a = unpack(external_rgba(c))
				config.palette2[c+1] = {r*255,g*255,b*255}
			end
			config.resolution = {SCRW,SCRH}
			config.scale = 1 -- ERROR when >= 2
			rec = gif.new('test1.gif',config)
		end
	end
	-- BEFORE
	love.graphics.setCanvas(SCR)

	_draw()
	
	-- AFTER
	love.graphics.setCanvas()
	love.graphics.setShader(recolor_shader)
	love.graphics.draw(SCR,0,0,0, SCRS,SCRS)
	love.graphics.setShader()
	
	if rec then
		rec:frame(SCR:newImageData())
	end
end

--love.graphics.setColor(1,1,1,1) -- czy potrzebne???


--------------------------------------------------------------------------------
--------------------------------------------------------------------------------	
--[ SANDBOX ]-------------------------------------------------------------------

t=0
function _draw()
	local fx,fy,ss
	if key('up') then fx=1 else fx=0 end
	if key('down') then fy=1 else fy=0 end
	if key('left') then ss=2 else ss=1 end
	cls(0)
	for c=0,15 do
		rectfill(8+16*c,8,12,24,c)
	end
	sprite(0,SCRW/2,SCRH/2,fx,fy,t*0.1,ss,2,1)
	t=t+1
	print('01 to jest\ntest',30,40,8,2)
	--letter('a',30,20,5,6)
end

function _init()
	local img = img_from_text([[
		##xxxxxx ######## ;
		#......x #......# ;
		x.oooo.x #.oooo.# ;
		x.oxx..x #......# ;
		x.oxx..x #......# ;
		x.o....x #.o..o.# ;
		#......x #......# ;
		##xxxxxx ######## ;
		
	]],'.xo#',{0,8,14,6})
	img:encode('png','test-new.png')
	BANKS[BANK] = img
	require('font')
	img = img_from_text(moki4x,'.X',{0,1},80,15)
	font_from_img(img,5,5,0,'0123456789 .....abcdefghijklmnopqrstuvwxyz')
	
	for v=0,255 do
		printh(v..' -> '..binary(v))
	end
end


function get_tile(b,s,w,h,colorkey)
	w=w or 1
	h=h or 1
	local bw = math.floor(banks[b]:getWidth()/8)
	local x,y = s%bw, math.floor(s/bw)
	local tile = love.image.newImageData(w*8,h*8)
	tile:paste(banks[b],0,0,x*8,y*8,w*8,h*8)
	if colorkey and colorkey>=0 then
		
		-- TODO wybrac szybsza metode
		
		function use_colorkey(x,y,r,g,b,a)
			rk,gk,bk = col_to_rgb(colorkey)
			if r==rk and g==gk and b==bk
				then trace('ok',x,y) return 0,0,0,0
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
	return love.graphics.newImage(tile)
end

function col_to_rgb(c)
	local c = c or 1
	local col = colors[c+1]
	return col[1]/255,col[2]/255,col[3]/255
end

function set_col(c)
	if c then love.graphics.setColor(col_to_rgb(c)) end
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

-- w can be filename
function set_bank(b,w,h)
	banks[b] = love.image.newImageData(w,h)
end

--------------------------------------------------------------------------------

function bank(b) BANK=b end

-- draw sprite by id, can scale, flip, rotate and sheer
function spr(s,x,y, colorkey,w,h, scale,flip,rotate,sx,sy, b)
	w = w or 1
	h = h or 1
	b = b or BANK
	flip = flip or 0
	rotate = rotate or 0
	
	local key = table.concat({b,s,colorkey or -1,w,h},':')
	local img = sprite_cache[key]
	if not img then
		img = get_tile(b,s,w,h,colorkey)
		sprite_cache[key] = img
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

function rect(x,y,w,h,c)
	set_col(c)
	love.graphics.rectangle('fill',x+camx,y+camy,w,h)
end
function rectb(x,y,w,h,c)
	set_col(c)
	love.graphics.rectangle('line',x+camx,y+camy,w,h)
end

function circ(x,y,r,c)
	set_col(c)
	love.graphics.circle('fill',x+camx,y+camy,r)
end
function circb(x,y,r,c)
	set_col(c)
	love.graphics.circle('line',x+camx,y+camy,r)
end

-- TODO get color
function pix(x,y,c)
	set_col(c)
	love.graphics.points(x+camx,y+camy)
end

function line(x0,y0,x1,y1,c)
	set_col(c)
	love.graphics.line(x0+camx,y0+camy,x1+camx,y1+camy)
end

function tri(x1,y1,x2,y2,x3,y3,c)
	set_col(c)
	love.graphics.polygon('fill',x1+camx,y1+camy,x2+camx,y2+camy,x3+camx,y3+camy)
end
function trib(x1,y1,x2,y2,x3,y3,c)
	set_col(c)
	love.graphics.polygon('line',x1+camx,y1+camy,x2+camx,y2+camy,x3+camx,y3+camy)
end

-- TODO font
-- TODO rest
trace = print
function print(text,x,y,c,fixed,scale,smallfont)
	scale=scale or 1
	set_col(c)
	love.graphics.print(text,x+camx,y+camy,0,scale,scale)
end

function cls(c)
	local c = c or 0
	love.graphics.clear(col_to_rgb(c))
end

function cam(x,y)
	camx = x
	camy = y
end

function clip(x,y,w,h)
	love.graphics.setScissor(x,y,w,h) -- camx camy ???
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
	return {mx,my,b1,b2,b3}
end

--------------------------------------------------------------------------------

pal_pico8 = {
	{0,0,0},{29,43,83},{126,37,83},{0,135,81},
	{171,82,54},{95,87,79},{194,195,199},{255,241,232},
	{255,0,77},{255,163,0},{255,236,39},{0,228,54},
	{41,173,255},{131,118,156},{255,119,168},{255,204,170},
}

pal_tic80 = {
	{0x14,0x0C,0x1C},{0x44,0x24,0x34},{0x30,0x34,0x6D},{0x4E,0x4A,0x4F},
	{0x85,0x4C,0x30},{0x34,0x65,0x24},{0xD0,0x46,0x48},{0x75,0x71,0x61},
	{0x59,0x7D,0xCE},{0xD2,0x7D,0x2C},{0x85,0x95,0xA1},{0x6D,0xAA,0x2C},
	{0xD2,0xAA,0x99},{0x6D,0xC2,0xCA},{0xDA,0xD4,0x5E},{0xDE,0xED,0xD6},
}

-- https://lospec.com/palette-list/castpixel-16
pal_pv8 = {
	{0x2D,0x1B,0x2E},{0x21,0x8A,0x91},{0x3C,0xC2,0xFA},{0x9A,0xF6,0xFD},
	{0x4A,0x24,0x7C},{0x57,0x4B,0x67},{0x93,0x7A,0xC5},{0x8A,0xE2,0x5D},
	{0x8E,0x2B,0x45},{0xF0,0x41,0x56},{0xF2,0x72,0xCE},{0xD3,0xC0,0xA8},
	{0xC5,0x75,0x4A},{0xF2,0xA7,0x59},{0xF7,0xDB,0x53},{0xF9,0xF4,0xEA},
}

-- https://lospec.com/palette-list/zx-spectrum
-- https://lospec.com/palette-list/zxarne-5-2
-- https://lospec.com/palette-list/endesga-16
-- https://lospec.com/palette-list/sweetie-16
-- https://lospec.com/palette-list/chromatic16

-- https://lospec.com/palette-list/armor-8
-- https://lospec.com/palette-list/generic-8
-- https://lospec.com/palette-list/endesga-8
-- https://lospec.com/palette-list/3-bit-rgb
-- https://lospec.com/palette-list/dawnbringers-8-color
-- https://lospec.com/palette-list/matriax8c

-- https://lospec.com/palette-list/en4


-------------------------------------------------------------------------
-------------------------------------------------------------------------

-- TODO love.graphics.setBackgroundColor

function love.load()
	camx,camy = 0,0
	sprite_cache={}
	banks={}
	colors=pal_pico8
	BANK = 1
	set_bank(1,'128.png')
	
	love.graphics.setLineStyle('rough')
	love.graphics.setDefaultFilter('nearest','nearest')
	banks[2]=img_from_text([[
		.##.
		#xx#
		..#.
		x..x
		####
		.xx.
	]],4,6,'.---------x-#')
	t=get_tile(2,0,0.5,0.75,10)
end

function love.draw()
	scr = love.graphics.newCanvas(600,600)
	love.graphics.setCanvas(scr)
	
	r1 = math.random(-2,2)
	r2 = math.random(-2,2)
	-- cam(r1,r2)
	
	cls()
	bank(1)
	spr(1,100,100)
	rect(400,400,50,80,4)
	circ(200,200,30)
	line(100,100,200,200)
	tri(300,300,380,340,300,340)
	print("to jest test",10,10)
	for i=0,15 do
		rect(8+i*32,8,32,32,i)
	end
	if key("up") then print("UP",500,500) end
	m = mouse()
	print(m[1].." "..m[2],200,500)
	bank(2)
	spr(2,140,140, 0,0.5,0.75, 32,0,0)
	spr(2,140,410, 0,0.5,0.75, 32,3,3)
	spr(2,410,410, 0,0.5,0.75, 32,0,0,0.25,-0.25)
	
	love.graphics.setCanvas()
	love.graphics.setColor(1,1,1,1) -- TODO store+restore color
	love.graphics.draw(scr,0,0,0)
	
	if key("f6") then love.graphics.captureScreenshot('screen.png') end
end

-- TODO sprite bank
function get_tile(cnv,x,y,w,h)
	w=w or 1
	h=h or 1
	return love.graphics.newImage(cnv:newImageData(nil,nil,x,y,w*8,h*8))
end

function col_to_rgb(c)
	local c = c or 1
	local col = colors[c+1]
	return col[1]/255,col[2]/255,col[3]/255
end

function set_col(c)
	love.graphics.setColor(col_to_rgb(c))
end

-- TODO colormap
function cnv_from_text(text,w,h)
	local cnv = love.graphics.newCanvas(w,h)
	local ch
	love.graphics.setCanvas(cnv)
	for i = 1,#text do
		ch = text:sub(i,i)
		y = math.floor(i/w)
		x = i%w
		if ch=='#' then set_col(14); love.graphics.points(x,y) end
	end
	love.graphics.setCanvas()
	return cnv
end

--------------------------------------------------------------------------------

-- TODO sprite bank
-- TODO rest of args
function spr(s,x,y,colorkey,scale,flip,rotate,w,h)
	s=sprites[s] or s
	love.graphics.draw(s,x+camx,y+camy,rotate,scale,scale)
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
function prn(text,x,y,c,fixed,scale,smallfont)
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
	sprites={}
	colors=pal_pv8
	love.graphics.setLineStyle('rough')
	cnv=love.graphics.newCanvas(128,128)
	love.graphics.setCanvas(cnv)
	love.graphics.circle('fill',64,64,32)
	love.graphics.setCanvas()
	s=get_tile(cnv,64,64)
	sprites[1]=s
end

function love.draw()
	cls()
	spr(1,100,100)
	rect(400,400,50,80,4)
	circ(200,200,30)
	line(100,100,200,200)
	tri(300,300,380,340,300,340)
	prn("to jest test",10,10)
	for i=0,15 do
		rect(8+i*32,8,32,32,i)
	end
	if key("up") then prn("UP",500,500) end
	m = mouse()
	prn(m[1].." "..m[2],500,500)
	c=cnv_from_text(".##.####....#..#",4,4)
	t=get_tile(c,0,0,0.5,0.5)
	sprites[2]=t
	spr(2,140,140,nil,32)
end

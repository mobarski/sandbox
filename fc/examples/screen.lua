function INIT()
	screen(300,200,3,[[
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
	]])

	local pixelcode = [[
		extern vec4 colors[32];
		vec4 effect( vec4 color, Image texture, vec2 texture_coords, vec2 screen_coords )
		{
			if ((mod(screen_coords.x,2)<=1) && (mod(screen_coords.y,2)<=1) ||
				(mod(screen_coords.x,2)>1) && (mod(screen_coords.y,2)>1) )
			{
				return colors[0];
			} else {
				return color;
			};
		}
	]]
	 
	shader = love.graphics.newShader(pixelcode)
	local rgba = {}
	local c
	for i=1,#colors do
		c = colors[i]
		rgba[i] = {c[1]/255,c[2]/255,c[3]/255,1}
		trace(i,c[1],c[2],c[3])
	end
	for i=1,#rgba do
		trace(i,unpack(rgba[i]))
	end
	shader:sendColor('colors',unpack(rgba))
	 
	x,y = 0,0
end

function DRAW()
	cls()
	camera(x,y)
	love.graphics.setShader(shader)
	for c=0,MAX_COLOR do
		rectfill(8+16*c,8,12,12,c)
	end
	love.graphics.setShader()
	for c=0,MAX_COLOR do
		rectfill(8+16*c,28,12,12,c)
	end
	if key("down") then y=y+1 end
	if key("up") then y=y-1 end
end


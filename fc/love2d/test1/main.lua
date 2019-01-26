require "engine"
require "font"

function INIT()
	set_bank(1,'128.png')
	banks[2]=img_from_text([[
		xxxxxxxx ########
		x......x #......#
		x......x #......#
		x..xx..x #......#
		x..xx..x #......#
		x......x #......#
		x......x #......#
		xxxxxxxx ########
		
	]],16,8,'.---------x-#')
	local map = map_from_text([[
		########
		#......#
		#......#
		#......#
		########
		
	]],8,5,'.#',{0,1})
	pages[1]=map
	banks[3] = img_from_text(moki0,32,20,'.----x')
	screen(250,250,3)
end

function MAIN()
	m = mouse()
	if m[3] then
		local r=math.random(0,255)
		local g=math.random(0,255)
		local b=math.random(0,255)
		pal(10,r,g,b)
	end
end

function DRAW()
	cls()
	
	r1 = math.random(-2,2)
	r2 = math.random(-2,2)
	--camera(r1,r2)

	rect(130,140,20,20,1)
	if true then
		bank(2)
		map(0,0)
		map(0,40)
		map(0,80)
		map(0,120)
		map(80,0)
		map(84,36)
		map(80,80)
		map(80,120)
	end
	if true then
		bank(3)
		spr(0,10,164,20,5, 1)
	end
	print(m[1].." "..m[2],0,0)
	print(fps(),200,0)
	print(pix(m[1],m[2]) or 0,100,0)
end


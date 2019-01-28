require "engine"
require "font"

function INIT()
	colors = pal_sweetie
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
	
	banks[4] = font_from_text(moki4x,5,5,'X','.','-')
	for s = 0,255 do
		trace(s,string.char(s),font_width[s])
	end
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

	rectfill(130,140,20,20,1)
	if false then
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
		for i=0,15 do
			rectfill(10+i*14,80,12,12,i)
		end
	end
	color(11)
	if true then
		bank(4)
		shadow(0,10,0,6, 16,16)
		print("wow the is airplane hit low fuel eject now",10,200,5)
	end
	print(m[1].." "..m[2],0,0)
	print(fps(),200,0)
	print(pget(m[1],m[2]) or 0,100,0)
end


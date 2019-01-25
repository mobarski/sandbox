require "engine"

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
	screen(200,200,3)
end

function MAIN()
	m = mouse()
end

function DRAW()
	r1 = math.random(-2,2)
	r2 = math.random(-2,2)
	-- cam(r1,r2)
	
	cls()
	bank(1)
	if false then 
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
		bank(2)
		spr(2,140,140, 0,0.5,0.75, 32,0,0)
		spr(2,140,410, 0,0.5,0.75, 32,3,3)
		spr(2,410,410, 0,0.5,0.75, 32,0,0,0.25,-0.25)
	end
	if true then
		map(0,0,8,5,0,0)
		map(0,0,8,5,0,40)
		map(0,0,8,5,0,80)
		map(0,0,8,5,0,120)
		map(0,0,8,5,80,0)
		map(0,0,8,5,80,40)
		map(0,0,8,5,80,80)
		map(0,0,8,5,80,120)
		
	end
	print(m[1].." "..m[2],0,180)
	print(fps(),100,180)
end


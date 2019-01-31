function INIT()
	colors = pal_sweetie
	
	bank_from_text(2,[[
		xxxxxxxx ######## ;
		x......x #......# ;
		x......x #.oooo.# ;
		x..xx..x #......# ;
		x..xx..x #......# ;
		x......x #.o..o.# ;
		x......x #......# ;
		xxxxxxxx ######## ;
		
	]],'.xo#',{0,10,1,12})
	local map = map_from_text([[
		######## ;
		#......# ;
		#......# ;
		#......# ;
		######## ;
		
	]],'.#',{0,1},8,5)
	pages[1]=map
	
	export_bank(2,'bank2.png')
	import_bank(5,'bank2.png')
	banks[5]:encode('png','bank5v2.png')
	export_bank(5,'bank5.png')
	MAP_BANK=2
	
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

	rectfill(0,0,20,20,1)
	rectfill(130,140,20,20,1)
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
		for i=0,15 do
			rectfill(10+i*14,80,12,12,i)
		end
	end
	if true then
		color(11)
		shadow(0, 10,130, 16,16, 5,FONT_BANK)
		print("wow the is airplane hit low fuel eject now",10,200,5)
	end
	print(m[1].." "..m[2],0,0)
	print(fps(),200,0)
	print(pget(m[1],m[2]) or 0,100,0)
	--clip(0,0,250,125)
end


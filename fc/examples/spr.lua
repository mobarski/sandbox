function INIT()
	colors = pal_sweetie
	
	bank_from_text(1,[[
		xxxxxxxx ######## ;
		x......x #......# ;
		x.o..o.x #.x..o.# ;
		x..xx..x #......# ;
		x..xx..x #.x..x.# ;
		x.o....x #.oooo.# ;
		x......x #......# ;
		xxxxxxxx ######## ;
		
	]],'.xo#',{0,10,4,12})
	export_bank(1,'spr.png')
	get_tile(1,1,1,1,0,true):encode('png','tile.png')
	export_bank(3,'font.png')
end

function DRAW()
	cls()
	local f = 0
	if key('left') then f=1 end
	if key('up') then f=f+2 end
	spr(0, 100,100, 1,1, f,6)
	spr(1, 200,100, 1,1, f,6)
end

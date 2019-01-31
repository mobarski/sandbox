function INIT()
	colors = pal_sweetie
	
	bank_from_text(1,[[
		xxxxxxxx ######## ;
		x......x #......# ;
		x......x #.o..o.# ;
		x..xx..x #......# ;
		x..xx..x #.x..x.# ;
		x......x #.oooo.# ;
		x......x #......# ;
		xxxxxxxx ######## ;
		
	]],'.xo#',{0,10,1,12})
	export_bank(1,'spr.png')
	get_tile(1,1,1,1,0,true):encode('png','tile.png')
	export_bank(3,'font.png')
end

function DRAW()
	cls()
	spr(0,100,100,1,1,6)
	spr(1,200,100,1,1,6)
end

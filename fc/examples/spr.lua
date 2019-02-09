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
	cls(2)
	local r
	for c=1,16 do
		rectfill(8+16*c,8,12,12,c)
		r = col_to_rgba(c)[0]
		--trace(c,r,r*255,int(r*255))
	end
	local f = 0
	if key('left') then f=1 end
	if key('up') then f=f+2 end
	spr(0, 100,100, 1,1, f,6)
	spr(1, 200,100, 1,1, f,6)
end

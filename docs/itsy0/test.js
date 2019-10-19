function _init() {
	px = 300
	py = 300
	sx = 300
	sy = 200
	vx = 1.4
	vy = 0
	MG = 300
	font('30px Moonbeam')
}

sign = Math.sign

function _main() {
	sx += vx
	sy += vy
	rx = sx-px
	ry = sy-py
	r2 = rx*rx + ry*ry
	f = MG / r2
	dvx = sign(rx) * f * rx*rx / r2
	dvy = sign(ry) * f * ry*ry / r2
	vx -= dvx
	vy -= dvy
}

function _draw() {
	cls(0)

	//camera(Math.random()*10,Math.random()*10)

	color(1)
	circ(px,py,12)
	
	color(2)
	circ(sx,sy,2)
	
	color(3)
	print("¶®ΨѦ",sx+10,sy+10)
	
	color(1)
	line(sx,sy,sx+10*vx,sy+10*vy)
	
	color(1,1)
	rect(10,10,50,50)
	
	xrect(100,500,55,55,2,1,true)
	xrect(100,500,45,45,0,0.8,true)
	
	color(2)
	xprint('Au',100,500)
	
	color(3)
	shape(200,500,[[50,0],[50,50],[0,50],[0,0]],0,false,true)
	
	color(5)
	print("Hail to Crail",300,500)
	print("dv = 1.432",300,550)

	
	snap = snapshot()
}

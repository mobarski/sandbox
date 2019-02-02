function INIT()
	screen(1600,1000,1)
end

cx,cy=600,500
rs=1.0
ds=rs/3
function DRAW()
	cls()
	jupiter()
end

function body(d,r)
	color(4)
	circ(cx,cy,d*ds)
	color(1)
	circfill(cx+d*ds,cy,r*rs)
end

function earth()
	body(0, 6.4)
	body(384, 1.7)
end

function uranus()
	body(0,25)
	body(129, 0.47)
	body(190, 1.16)
	body(266, 1.17)
	body(436, 1.58)
	body(583, 1.52)
end

function saturn()
	body(0,58)
	body(185, 0.4)
	body(238, 0.5)
	body(294, 1.0)
	body(377, 1.1)
	body(527, 1.5)
	body(1221, 5.1)
end

function jupiter()
	body(0, 69.9)
	body(421, 3.6)
	body(671, 3.1)
	body(1070, 5.2)
	body(1882, 4.8)
end
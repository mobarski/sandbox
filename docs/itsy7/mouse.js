// ---[ API ]-------------------------------------------------------------------

function mouse() {
	return [MX,MY,M1,M2]
}

// ---[ MOUSE ]-----------------------------------------------------------------

var MX = -1
var MY = -1
var M1 = 0 // status -> 3210 3:down 2:held 1:up 0:none
var M2 = 0 // status -> 3210 3:down 2:held 1:up 0:none
var MW = 0

var cnv_bcr = cnv.getBoundingClientRect()

function on_mouse_move(e) {
	MX = e.clientX - cnv_bcr.left // TODO - cnv_x
	MY = e.clientY - cnv_bcr.top // TODO - cnv_y
}

function on_mouse_up(e) {
	if (e.button==0) {
		M1 = 1
	} else if (e.button==2) {
		M2 = 1
	}
}

function on_mouse_down(e) {
	if (e.button==0) {
		M1 = 3
	} else if (e.button==2) {
		M2 = 3
	}
}

function on_wheel(e) {
	if (e.deltaY > 0) {
		MW = 1
	} else if (e.deltaY < 0) {
		MW = -1
	} else {
		MW = 0
	}
}

function mouse_after() {
	switch (M1) {
		case 3: M1=2; break
		case 1: M1=0; break
	}
	switch (M2) {
		case 3: M2=2; break
		case 1: M2=0; break
	}
}

_after.push(mouse_after)

document.addEventListener('mousemove',on_mouse_move)
cnv.addEventListener('mouseup',on_mouse_up)
cnv.addEventListener('mousedown',on_mouse_down)
cnv.addEventListener('wheel',on_wheel)
cnv.addEventListener("contextmenu",function(e){e.preventDefault()})

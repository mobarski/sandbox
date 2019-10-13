// ---[ API ]-------------------------------------------------------------------

function rect(x,y,w,h,c) {
	ctx.fillStyle = fc.pal.style[c]
	ctx.fillRect(x,y,w,h)
}

function cls(c) {
	rect(0,0,fc.w,fc.h,c)
}

function blit(data,x,y,w,h,sx,sy,ckey) {
	for (var i=0; i<w; i++) {
		for (var j=0; j<h; j++) {
			var c = data[i+j*w]
			if (c == ckey) continue 
			rect(x+i*sx,y+j*sy,sx,sy,c)
		}
	}
}

function spr(n,x,y,ckey=0,scx=fc.sx,scy=fc.sy) {
	var b = fc.bank
	blit(b.data[n], x,y, b.w,b.h, scx,scy, ckey)
}

function pix(x,y) {
	var [r,g,b,a] = ctx.getImageData(x,y,1,1).data
	var rgb = fc.pal.rgb
	for (var i=0; i<rgb.length; i++) {
		if (rgb[i][0]==r && rgb[i][1]==g && rgb[i][2]==b) {
			return i
		}
	}
	return null
}

function status(text) {
	out.innerHTML = text
}

// -----------------------------------------------------------------------------

function _fullscreen(elem) {
	if (elem.requestFullscreen) {
		elem.requestFullscreen()
	} else if (elem.mozRequestFullScreen) { /* Firefox */
		elem.mozRequestFullScreen()
	} else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
		elem.webkitRequestFullscreen()
	} else if (elem.msRequestFullscreen) { /* IE/Edge */
		elem.msRequestFullscreen()
	}
}

function _init_screen() {
	fc.w = fc.w || 800
	fc.h = fc.h || 400
	fc.sx = fc.sx || 8
	fc.sy = fc.sy || 8
	
	var screen = document.getElementById("screen")
	screen.innerHTML = `<canvas id="main_canvas" width="${fc.w}" height="${fc.h}" style="border:1px solid #000000;"></canvas>`
	
	// TODO fc.*
	out = document.getElementById("output")
	cnv = document.getElementById("main_canvas")
	
	ctx = cnv.getContext("2d")
}

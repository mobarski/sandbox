// TODO - move
function status(text) {
	out.innerHTML = text
}

// ---[ API ]-------------------------------------------------------------------

// TODO - benchmark recv vs xrect, circ vs xcirc

function color(c,a=1) {
	ctx.fillStyle = fc.pal.style[c].slice(0,-1)+`,${a})`
	ctx.strokeStyle = ctx.fillStyle
}

function cls(c) {
	color(c)
	rect(0,0,fc.w,fc.h)
}

function rect(x,y,w,h) {
	ctx.fillRect(x,y,w,h)
}

function xrect(x,y,w,h,c,a=1,center=false) {
	color(c,a)
	if (center) {
		ctx.fillRect(x-0.5*w,y-0.5*h,w,h)
	} else {
		ctx.fillRect(x,y,w,h)
	}
}


function circ(x,y,r) {
	ctx.beginPath()
	ctx.arc(x,y,r,0,2*Math.PI)
	ctx.fill()
}

function xcirc(x,y,r,c,a=1) {
	color(c,a)
	ctx.beginPath()
	ctx.arc(x,y,r,0,2*Math.PI)
	ctx.fill()
}


// TODO - lepsze api ???
function line(x,y,x2,y2,w=1) {
	ctx.beginPath()
	ctx.lineCap = "round"
	ctx.moveTo(x,y)
	ctx.lineTo(x2,y2)
	ctx.lineWidth = w
	ctx.stroke()
}

function camera(x,y) {
	ctx.setTransform(1,0,0,1,x,y)
}

// ---[ TEXT ]------------------------------------------

function font(s) {
	ctx.font = s
}

function print(s,x,y) {
	ctx.fillText(s,x,y)
}

// TODO: rename
function measure(s) {
	return ctx.measureText(s).width
}

function xprint(s,x,y,align='center',base='middle') {
	ctx.textAlign = align
	ctx.textBaseline = base
	ctx.fillText(s,x,y)
	ctx.textAlign = 'left'
	ctx.textBaseline = 'top'
}

// ---[ EXPERIMENTAL ]--------------------------------------------

function shape(x,y,dots,w=1,strk=true,fil=false) {
	ctx.beginPath()
	ctx.moveTo(x,y)
	for (var i in dots) {
		var [dx,dy] = dots[i]
		ctx.lineTo(x+dx,y+dy)
	}
	ctx.lineCap = "round"
	ctx.lineWidth = w
	if (fil)  {ctx.fill()}
	if (strk) {ctx.stroke()}
}

function snapshot() {
	return cnv.toDataURL("image/png")
}

// function blit(data,x,y,w,h,sx,sy,ckey) {
	// for (var i=0; i<w; i++) {
		// for (var j=0; j<h; j++) {
			// var c = data[i+j*w]
			// if (c == ckey) continue 
			// rect(x+i*sx,y+j*sy,sx,sy,c)
		// }
	// }
// }

// function spr(n,x,y,ckey=0,scx=fc.sx,scy=fc.sy) {
	// var b = fc.bank
	// blit(b.data[n], x,y, b.w,b.h, scx,scy, ckey)
// }

// function pix(x,y) {
	// var [r,g,b,a] = ctx.getImageData(x,y,1,1).data
	// var rgb = fc.pal.rgb
	// for (var i=0; i<rgb.length; i++) {
		// if (rgb[i][0]==r && rgb[i][1]==g && rgb[i][2]==b) {
			// return i
		// }
	// }
	// return null
// }

// -----------------------------------------------------------------------------

function _fullscreen() {
	var elem = cnv
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
	screen.innerHTML = `<canvas id="main_canvas" width="${fc.w}" height="${fc.h}""></canvas>`
	
	// TODO fc.*
	out = document.getElementById("output")
	cnv = document.getElementById("main_canvas")
	
	ctx = cnv.getContext("2d")
}

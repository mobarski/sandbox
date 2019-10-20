// TODO - move
function status(text) {
	out.innerHTML = text
}

// ---[ API ]-------------------------------------------------------------------

function color(c,a=1) {
	var _c = c % fc.pal.length
	ctx.fillStyle = fc.pal.style[_c].slice(0,-1)+`,${a})`
	ctx.strokeStyle = ctx.fillStyle
}


function cls(c=null,a=1) {
	if (c != null) { color(c,a) }
	rect(0,0,fc.w,fc.h)
}

function rect(x,y,w,h,c=null,a=1) {
	if (c != null) { color(c,a) }
	ctx.fillRect(x,y,w,h)
}

// 3.3 x wolniej niz rect !!!
function xrect(x,y,w,h,c,a=1,center=false) {
	color(c,a)
	if (center) {
		ctx.fillRect(x-0.5*w,y-0.5*h,w,h)
	} else {
		ctx.fillRect(x,y,w,h)
	}
}

// 250k -> 1800ms
function circ(x,y,r,c=null,a=1) {
	if (c != null) { color(c,a) }
	ctx.beginPath()
	ctx.arc(x,y,r,0,2*Math.PI)
	ctx.fill()
}


// TODO - lepsze api ???
// 250k -> 1200ms
function line(x,y,x2,y2,width=1,cap='round') {
	ctx.beginPath()
	ctx.lineCap = cap
	ctx.moveTo(x,y)
	ctx.lineTo(x2,y2)
	ctx.lineWidth = width
	ctx.stroke()
}

function camera(x,y,sx=1,sy=1) {
	ctx.setTransform(sx,0,0,sy,x,y)
}

function fullscreen() {
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

// ---[ EXPERIMENTAL ]--------------------------------------------

// function shape(x,y,dots) {
	// ctx.beginPath()
	// ctx.moveTo(x,y)
	// for (var i in dots) {
		// var [dx,dy] = dots[i]
		// ctx.lineTo(x+dx,y+dy)
	// }
	// ctx.closePath()
	// ctx.fill()
// }

function shape(x,y,dots) {
	ctx.beginPath()
	ctx.moveTo(x,y)
	for (var i=0; i<dots.length; i+=2) {
		var dx = dots[i]
		var dy = dots[i+1]
		ctx.lineTo(x+dx,y+dy)
	}
	ctx.closePath()
	ctx.fill()
}

function xshape(x,y,dots,w=1,cap='miter',jn='mitter',close=false,strk=true,fil=false) {
	ctx.beginPath()
	ctx.moveTo(x,y)
	for (var i in dots) {
		var [dx,dy] = dots[i]
		ctx.lineTo(x+dx,y+dy)
	}
	ctx.lineCap = cap // butt  round square
	ctx.lineJoin = jn // bevel round miter
	ctx.lineWidth = w
	if (close) {ctx.closePath()}
	if (fil)   {ctx.fill()}
	if (strk)  {ctx.stroke()}
}

function snapshot(image=false,x=0,y=0,w=0,h=0) {
	var _w = w || fc.w-x
	var _h = h || fc.h-y
	var imagedata = ctx.getImageData(0,0,_w,_h)
	return image ? _imagedata_to_image(imagedata) : imagedata.data
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

function _get_pixel_rgb(x,y) {
	return ctx.getImageData(x,y,1,1).data
}

function _imagedata_to_image(imagedata) {
    var canvas = document.createElement('canvas')
    var ctx = canvas.getContext('2d')
    canvas.width = imagedata.width
    canvas.height = imagedata.height
    ctx.putImageData(imagedata, 0, 0)

    var image = new Image()
    image.src = canvas.toDataURL()
    return image
}

function _init_screen() {
	fc.w = fc.w || 800
	fc.h = fc.h || 400
	
	fc.sx = fc.sx || 8 // NOT USED YET
	fc.sy = fc.sy || 8 // NOT USED YET
	
	var screen = document.getElementById("screen")
	screen.innerHTML = `<canvas id="main_canvas" width="${fc.w}" height="${fc.h}""></canvas>`
	
	// TODO fc.*
	out = document.getElementById("output")
	cnv = document.getElementById("main_canvas")
	
	ctx = cnv.getContext("2d")
	ctx.imageSmoothingEnabled = fc.aa || false
}

var out = document.getElementById("output")
var cnv = document.getElementById("main_canvas")
var ctx = cnv.getContext("2d")

// ----------------------------------------------------------------------------

function imagedata_to_image(imagedata) {
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    canvas.width = imagedata.width;
    canvas.height = imagedata.height;
    ctx.putImageData(imagedata, 0, 0);

    var image = new Image();
    image.src = canvas.toDataURL();
    return image;
}


function clear_screen(r,g,b) {
	ctx.fillStyle="rgb("+r+","+g+","+b+")"
	ctx.fillRect(0,0,cnv.width,cnv.height)
}

// TODO transparency separated from pal
function create_sprite(w,h,pal,pixels,sx=1,sy=1,alpha={0:0}) {
	var img = ctx.createImageData(w*sx,h*sy)
	for (var i=0;i<pixels.length;i+=1) {
		var c = pixels[i]
		var p = pal[c]
		var x = i % w
		var y = Math.floor(i / h)
		var ii = y*sy*sx*w + x*sx
		for (var iy=0; iy<sy; iy+=1) {
			for (var ix=0; ix<sx; ix+=1) {
				var iii = ii + iy*(sx*w) + ix
				img.data[4*iii + 0] = p[0]
				img.data[4*iii + 1] = p[1]
				img.data[4*iii + 2] = p[2]
				//img.data[4*iii + 3] = p.length>3 ? p[3] : 255
				img.data[4*iii + 3] = c in alpha ? alpha[c] : 255
			}
		}
	}
	return imagedata_to_image(img)
}

// TODO flip (translate(w,0) + scale(-1,1))
function draw_sprite(img,x,y,rot=0) {
	var w = img.width
	var h = img.height
	ctx.save()
	ctx.translate(x+w/2,y+h/2)
	ctx.rotate(rot * Math.PI / 180)
	ctx.drawImage(img,-w/2,-h/2)
	ctx.restore()	
}

function get_pixel_rgb(x,y) {
	return ctx.getImageData(x,y,1,1).data
}

// ---[ MOUSE ]-----------------------------------------------------------------

// IDEA - status -> 3210 3:down 2:held 1:up 0:none
// IDEA - status -> 210-1 2:down 1:held 0:none -1:up

var MX = -1
var MY = -1
var M1 = 0
var M2 = 0
var MW = 0

var cnv_bcr = cnv.getBoundingClientRect()

function on_mouse_move(e) {
	MX = e.clientX - cnv_bcr.left // TODO - cnv_x
	MY = e.clientY - cnv_bcr.top // TODO - cnv_y
}

function on_mouse_up(e) {
	if (e.button==0) {
		M1 = 0
	} else if (e.button==2) {
		M2 = 0
	}
}

function on_mouse_down(e) {
	if (e.button==0) {
		M1 = 1
	} else if (e.button==2) {
		M2 = 1
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

document.addEventListener('mousemove',on_mouse_move)
cnv.addEventListener('mouseup',on_mouse_up)
cnv.addEventListener('mousedown',on_mouse_down)
cnv.addEventListener('wheel',on_wheel)
cnv.addEventListener("contextmenu",function(e){e.preventDefault()})

// === STAGE 1 === mozliwosc zrobienia edytora spritow

// TODO gotowe palety

// TODO ustalenie przezroczystosci koloru
// TODO przemapowanie kolorow

// TODO pobranie koloru pixela i zmapowanie go na kolor z palety
// TODO rysowanie prostokata

// TODO wczytywanie / zapisywanie wynikow (localStorage)
// TODO import / export wynikow (plik tekstowy)

// === STAGE 2 === eventy

// TODO funkcja glowna
// TODO klawisze
// TODO mysz
// TODO dotyk

// === STAGE 3 === mapy

// TODO new_map(w,h,tiles,plan) -> image
// TODO draw_map(map,x,y) // x,y -> center
// TODO map_xy(scr_x, scr_y) -> tile_number

// === STAGE 4 === inne

// TODO rysowanie pixela
// TODO rysowanie kola
// TODO rysowanie lini

// TODO print
// TODO wlasne czcionki

// TODO dzwieki

// ----------------------------------------------------------------------------

var PAL = []

function cls(c,g=-1,b=-1) {
	var rgb = g>=0 ? [c,g,b] : PAL[c]
	clear_screen(rgb[0],rgb[1],rgb[2])
}

function rect(x,y,w,h,c) {
	rgb = PAL[c]
	ctx.fillStyle = "rgb("+rgb[0]+","+rgb[1]+","+rgb[2]+")" // OPTIMIZATION  OPPORTUNITY
	ctx.fillRect(x,y,w,h)
}

function sprite(w,h,colors,pixels,sx=1,sy=1,alpha={0:0}) {
	var pal = []
	for (i=0;i<colors.length;i++) {
		pal.push(PAL[colors[i]])
	}
	return create_sprite(w,h,pal,pixels,sx,sy,alpha)
}

// TODO scale
// TODO flip
// TODO n zamiast img
function spr(img,x,y,rot=0) {
	draw_sprite(img,x,y,rot)
}

function mouse() {
	return MX,MY,M1,M2
}

// ----------------------------------------------------------------------------
// ----------------------------------------------------------------------------
// ----------------------------------------------------------------------------

var pal_pv8 = [
	[0x2D,0x1B,0x2E],[0x21,0x8A,0x91],[0x3C,0xC2,0xFA],[0x9A,0xF6,0xFD],
	[0x4A,0x24,0x7C],[0x57,0x4B,0x67],[0x93,0x7A,0xC5],[0x8A,0xE2,0x5D],
	[0x8E,0x2B,0x45],[0xF0,0x41,0x56],[0xF2,0x72,0xCE],[0xD3,0xC0,0xA8],
	[0xC5,0x75,0x4A],[0xF2,0xA7,0x59],[0xF7,0xDB,0x53],[0xF9,0xF4,0xEA]
]
PAL = pal_pv8

function _init() {
	//cnv.style.cursor = "none"
	s = sprite(3,3,[0,0,1],[
		0,1,0,
		1,2,1,
		1,0,1],8,12,alpha={0:0,2:128})

	cls(0,0,0)
	spr(s,100,100,45)
	spr(s,110,110)
	for (i=0;i<16;i++) {
		rect(30+i*40,50,30,30,i)
	}
}

function _main() {
	aux = get_pixel_rgb(MX,MY)
	status = `x:${MX} y:${MY} m1:${M1} m2:${M2} mw:${MW} ${aux}`
	out.innerHTML = status

	cls(0,0,0)
	spr(s,MX,MY,45)
	for (i=0;i<16;i++) {
		rect(30+i*40,50,30,30,i)
	}
}

// ------------------------------------------------------------------------------
// ------------------------------------------------------------------------------
// ------------------------------------------------------------------------------

window.onload = function(e) {
	_init()
	window.setInterval(_main,16.6)
}

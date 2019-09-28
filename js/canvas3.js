var out = document.getElementById("output")
var c = document.getElementById("main_canvas")
var ctx = c.getContext("2d")

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

// ----------------------------------------------------------------------------

// TODO cls(pal_color)
function cls(r,g,b) {
	ctx.fillStyle="rgb("+r+","+g+","+b+")"
	ctx.fillRect(0,0,c.width,c.height)
}

// TODO transparency separated from pal
function sprite(w,h,pal,pixels,sx=1,sy=1) {
	var img = ctx.createImageData(w*sx,h*sy)
	for (var i=0;i<pixels.length;i+=1) {
		var p = pal[pixels[i]]
		var x = i % w
		var y = Math.floor(i / h)
		var ii = y*sy*sx*w + x*sx
		for (var iy=0; iy<sy; iy+=1) {
			for (var ix=0; ix<sx; ix+=1) {
				var iii = ii + iy*(sx*w) + ix
				img.data[4*iii + 0] = p[0]
				img.data[4*iii + 1] = p[1]
				img.data[4*iii + 2] = p[2]
				img.data[4*iii + 3] = p[3]
			}
		}
	}
	return imagedata_to_image(img)
}

// TODO flip (translate(w,0) + scale(-1,1))
function draw_sprite(s,x,y,rot=0) {
	var w = s.width
	var h = s.height
	ctx.save()
	ctx.translate(x+w/2,y+h/2)
	ctx.rotate(rot * Math.PI / 180)
	ctx.drawImage(s,-w/2,-h/2)
	ctx.restore()	
}

// TODO draw_map(w,h,tiles,plan,x,y) // x,y -> center
// TODO map_xy(scr_x, scr_y) -> tile_number

// ----------------------------------------------------------------------------

var pal_pv8 = [
	[0x2D,0x1B,0x2E],[0x21,0x8A,0x91],[0x3C,0xC2,0xFA],[0x9A,0xF6,0xFD],
	[0x4A,0x24,0x7C],[0x57,0x4B,0x67],[0x93,0x7A,0xC5],[0x8A,0xE2,0x5D],
	[0x8E,0x2B,0x45],[0xF0,0x41,0x56],[0xF2,0x72,0xCE],[0xD3,0xC0,0xA8],
	[0xC5,0x75,0x4A],[0xF2,0xA7,0x59],[0xF7,0xDB,0x53],[0xF9,0xF4,0xEA]
]


var pal = {0:[0,0,0,0],1:[0x2D,0x1B,0x2E,255],2:[255,0,0,128]}
var s = sprite(3,3,pal,[
	0,1,0,
	1,2,1,
	1,0,1],8,12)

cls(99,99,99)
draw_sprite(s,100,100,45)
draw_sprite(s,110,110)


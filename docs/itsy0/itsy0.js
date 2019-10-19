var fc = {}

fc.w = 640
fc.h = 640
// fc.sx = 2
// fc.sy = 2

// TODO: jakis dodatkowy prefix

function save(key,value) {
	localStorage['itsy_'+key] = JSON.stringify(value)
}

function load(key) {
	return JSON.parse(localStorage['itsy_'+key])
}

const CODE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

function _run_len_encode(text) {
	var out = ""
	for (var i=0; i<text.length;) {
		var c = text[i]
		var n = 1
		for (var j=1;j<CODE.length && i+j<=text.length;j++) {
			var c2 =text[i+j]
			//console.log(`i:${i} j:${j} c:${c} c2:${c2}`)
			if (c==c2) {
				n++
			} else if (n>=4) {
				out += '_'
				out += CODE[n]
				out += c
				i+=n-1
				break
			} else {
				out += c
				break
			}
		}
		i++
	}
	return out
}

function _run_len_decode(text) {
	var out = ""
	for (var i=0; i<text.length;) {
		var c = text[i]
		if (c=='_') {
			var c1 = text[i+1]
			var n = CODE.indexOf(c1)
			var c2 = text[i+2]
			for (var j=0; j<n; j++) {
				out += c2
			}
			i += 3
		} else {
			out += c
			i += 1
		}
	}
	return out
}
// --- [ API ]------------------------------------------------------------------

function bank(b=null) {
	console.log(`switching bank to ${b}`)
	var b_prev = fc.b
	if (b!=null) {
		fc.b = b
	}
	fc.bank = fc.banks[fc.b]
	return b_prev
}

// -----------------------------------------------------------------------------

fc.banks = {}
fc.bank = null
fc.b = null

function _init_bank(b,w,h,nx,ny,c=0) {
	var bank = {}
	bank.w = w
	bank.h = h
	bank.nx = nx
	bank.ny = ny
	if (Array.isArray(c)) {
		bank.data = c
	} else {
		bank.data = []
		for (var i=0; i<nx*ny; i++) {
			var a = new Array(w*h)
			for (j=0; j<w*h; j++) a[j]=c
			bank.data.push(a)
		}
	}
	fc.banks[b] = bank
}

function _dumps_bank(b) {
	var bank = fc.banks[b]
	return JSON.stringify(bank.data) // XXX
	// const code = CODE
	// const ver = 1
	// var out = ''
	// out += code[ver]
	// out += code[bank.w]
	// out += code[bank.h]
	// out += code[bank.nx]
	// out += code[bank.ny]
	
	// for (var i=0;i<bank.data.length; i++) {
		// var s = bank.data[i]
		// for (var j=0;j<s.length;j++) {
			// out += code[s[j]]
		// }
	// }
	// // return _run_len_encode(out)
	// return out
}

function _loads_bank(b,raw) {
	var bank = {}
	const code = CODE
	var data = raw.split('')
	var ver = code.indexOf(data.shift())
	if (ver!=1) return // ALERT
	bank.w = code.indexOf(data.shift())
	bank.h = code.indexOf(data.shift())
	bank.nx = code.indexOf(data.shift())
	bank.ny = code.indexOf(data.shift())
	bank.data = []
	for (var i=0; i<bank.nx*bank.ny; i++) {
		var a = []
		for (var j=0; j<bank.w*bank.h;) {
			var v = code.indexOf(data.shift()) 
			if (v>=0) {
				a.push(v)
				j++
			}
		}
		bank.data.push(a)
	}
	fc.banks[b] = bank
}
// REQUIRES: fc={}

fc.pal = {}
fc.pal.rgb = []
fc.pal.style = []

fc.pal.recalc = function() {
	this.length = this.rgb.length
	for (var i=0; i<this.length; i++) {
		var [r,g,b] = this.rgb[i]
		this.style[i] = `rgb(${r},${g},${b})`
	}
}

fc.pal.load = function(name) {
	this.rgb = palette[name].slice()
	this.recalc()
}

fc.pal.list = function(n=0) {
	var out = []
	for (name in palette) {
		if (n && palette[name].length==n || n==0) {
			out.push(name)
		}
	}
	return out
}

palette = {}
// color 0 must be the darkest !!!

// -----------------------------------------------------------------------------
// -----------------------------------------------------------------------------
// -----------------------------------------------------------------------------

palette["pico8"] = [
	[0,0,0],[29,43,83],[126,37,83],[0,135,81],
	[171,82,54],[95,87,79],[194,195,199],[255,241,232],
	[255,0,77],[255,163,0],[255,236,39],[0,228,54],
	[41,173,255],[131,118,156],[255,119,168],[255,204,170],
]

palette["tic80"] = [
	[0x14,0x0C,0x1C],[0x44,0x24,0x34],[0x30,0x34,0x6D],[0x4E,0x4A,0x4F],
	[0x85,0x4C,0x30],[0x34,0x65,0x24],[0xD0,0x46,0x48],[0x75,0x71,0x61],
	[0x59,0x7D,0xCE],[0xD2,0x7D,0x2C],[0x85,0x95,0xA1],[0x6D,0xAA,0x2C],
	[0xD2,0xAA,0x99],[0x6D,0xC2,0xCA],[0xDA,0xD4,0x5E],[0xDE,0xED,0xD6],
]

// https://lospec.com/palette-list/castpixel-16
palette["castpixel-16"] = [
	[0x2D,0x1B,0x2E],[0x21,0x8A,0x91],[0x3C,0xC2,0xFA],[0x9A,0xF6,0xFD],
	[0x4A,0x24,0x7C],[0x57,0x4B,0x67],[0x93,0x7A,0xC5],[0x8A,0xE2,0x5D],
	[0x8E,0x2B,0x45],[0xF0,0x41,0x56],[0xF2,0x72,0xCE],[0xD3,0xC0,0xA8],
	[0xC5,0x75,0x4A],[0xF2,0xA7,0x59],[0xF7,0xDB,0x53],[0xF9,0xF4,0xEA],
]

// https://lospec.com/palette-list/zx-spectrum
palette["zx-spectrum"] = [
	[0x00,0x00,0x00],
	[0x00,0x22,0xc7],
	[0x00,0x2b,0xfb],
	[0xd6,0x28,0x16],
	[0xff,0x33,0x1c],
	[0xd4,0x33,0xc7],
	[0xff,0x40,0xfc],
	[0x00,0xc5,0x25],
	[0x00,0xf9,0x2f],
	[0x00,0xc7,0xc9],
	[0x00,0xfb,0xfe],
	[0xcc,0xc8,0x2a],
	[0xff,0xfc,0x36],
	[0xca,0xca,0xca],
	[0xff,0xff,0xff],
]

// https://lospec.com/palette-list/zxarne-5-2
palette["zxarne-5-2"] = [
	[0x00,0x00,0x00],
	[0x3c,0x35,0x1f],
	[0x31,0x33,0x90],
	[0x15,0x59,0xdb],
	[0xa7,0x32,0x11],
	[0xd8,0x55,0x25],
	[0xa1,0x55,0x89],
	[0xcd,0x7a,0x50],
	[0x62,0x9a,0x31],
	[0x9c,0xd3,0x3c],
	[0x28,0xa4,0xcb],
	[0x65,0xdc,0xd6],
	[0xe8,0xbc,0x50],
	[0xf1,0xe7,0x82],
	[0xbf,0xbf,0xbd],
	[0xf2,0xf1,0xed],
]

// https://lospec.com/palette-list/endesga-16
palette["endesga-16"] = [
	[0xe4,0xa6,0x72],
	[0xb8,0x6f,0x50],
	[0x74,0x3f,0x39],
	[0x3f,0x28,0x32],
	[0x9e,0x28,0x35],
	[0xe5,0x3b,0x44],
	[0xfb,0x92,0x2b],
	[0xff,0xe7,0x62],
	[0x63,0xc6,0x4d],
	[0x32,0x73,0x45],
	[0x19,0x3d,0x3f],
	[0x4f,0x67,0x81],
	[0xaf,0xbf,0xd2],
	[0xff,0xff,0xff],
	[0x2c,0xe8,0xf4],
	[0x04,0x84,0xd1],
]

// https://lospec.com/palette-list/sweetie-16
palette["sweetie-16"] = [
	[0x1a,0x1c,0x2c],
	[0x57,0x29,0x56],
	[0xb1,0x41,0x56],
	[0xee,0x7b,0x58],
	[0xff,0xd0,0x79],
	[0xa0,0xf0,0x72],
	[0x38,0xb8,0x6e],
	[0x27,0x6e,0x7b],
	[0x29,0x36,0x6f],
	[0x40,0x5b,0xd0],
	[0x4f,0xa4,0xf7],
	[0x86,0xec,0xf8],
	[0xf4,0xf4,0xf4],
	[0x93,0xb6,0xc1],
	[0x55,0x71,0x85],
	[0x32,0x40,0x56],
]

// https://lospec.com/palette-list/chromatic16
palette["chromatic16"] = [
	[0x00,0x00,0x00],
	[0x90,0xB0,0xB0],
	[0xFF,0xFF,0xFF],
	[0x80,0x00,0x18],
	[0xFF,0x00,0x00],
	[0xA0,0x50,0x00],
	[0xFF,0x80,0x00],
	[0xFF,0xC0,0x80],
	[0xFF,0xFF,0x00],
	[0x20,0xAC,0x00],
	[0x40,0xFF,0x00],
	[0x00,0x30,0x70],
	[0x30,0x70,0xB0],
	[0x00,0xD0,0xFF],
	[0xA0,0x00,0xE0],
	[0xFF,0x60,0xFF],
]

// https://lospec.com/palette-list/taffy-16
palette["taffy-16"] = [
	[0x22,0x25,0x33],
	[0x62,0x75,0xba],
	[0xa3,0xc0,0xe6],
	[0xfa,0xff,0xfc],
	[0xff,0xab,0x7b],
	[0xff,0x6c,0x7a],
	[0xdc,0x43,0x5b],
	[0x3f,0x48,0xc2],
	[0x44,0x8d,0xe7],
	[0x2b,0xdb,0x72],
	[0xa7,0xf5,0x47],
	[0xff,0xeb,0x33],
	[0xf5,0x89,0x31],
	[0xdb,0x4b,0x3d],
	[0xa6,0x3d,0x57],
	[0x36,0x35,0x4d],
]

// https://lospec.com/palette-list/easter-island
palette["easter-island"] = [
	[0xf6,0xf6,0xbf],
	[0xe6,0xd1,0xd1],
	[0x86,0x86,0x91],
	[0x79,0x47,0x65],
	[0xf5,0xe1,0x7a],
	[0xed,0xc3,0x8d],
	[0xcc,0x8d,0x86],
	[0xca,0x65,0x7e],
	[0x39,0xd4,0xb9],
	[0x8d,0xbc,0xd2],
	[0x81,0x84,0xab],
	[0x68,0x60,0x86],
	[0x9d,0xc0,0x85],
	[0x7e,0xa7,0x88],
	[0x56,0x78,0x64],
	[0x05,0x16,0x25],
]

// -----------------------------------------------------------------------------
// -----------------------------------------------------------------------------
// -----------------------------------------------------------------------------

// https://lospec.com/palette-list/armor-8
palette["armor-8"] = [
	[0x18,0x18,0x19],
	[0x85,0x7d,0x7d],
	[0xf6,0xf6,0xf5],
	[0x44,0x4d,0x8e],
	[0x46,0x37,0x37],
	[0xaa,0x3d,0x33],
	[0xe9,0xb3,0x70],
	[0x4a,0x90,0x42],
]

// https://lospec.com/palette-list/generic-8
palette["generic-8"] = [
	[0x1c,0x11,0x21],
	[0xed,0xec,0xe9],
	[0xa1,0x3b,0x3b],
	[0xf3,0x7f,0x9a],
	[0xee,0x96,0x1a],
	[0x2d,0x53,0x65],
	[0x40,0xa9,0x33],
	[0x25,0xa6,0xc5],
]

// https://lospec.com/palette-list/endesga-8
palette["endesga-8"] = [
	[0xfd,0xfd,0xf8],
	[0xd3,0x27,0x34],
	[0xda,0x7d,0x22],
	[0xe6,0xda,0x29],
	[0x28,0xc6,0x41],
	[0x2d,0x93,0xdd],
	[0x7b,0x53,0xad],
	[0x1b,0x1c,0x33],
]

// https://lospec.com/palette-list/3-bit-rgb
palette["3-bit-rgb"] = [
	[0x00,0x00,0x00],
	[0xff,0x00,0x00],
	[0x00,0xff,0x00],
	[0x00,0x00,0xff],
	[0x00,0xff,0xff],
	[0xff,0x00,0xff],
	[0xff,0xff,0x00],
	[0xff,0xff,0xff],
]

// https://lospec.com/palette-list/dawnbringers-8-color
palette["dawnbringers-8-color"] = [
	[0x00,0x00,0x00],
	[0x55,0x41,0x5f],
	[0x64,0x69,0x64],
	[0xd7,0x73,0x55],
	[0x50,0x8c,0xd7],
	[0x64,0xb9,0x64],
	[0xe6,0xc8,0x6e],
	[0xdc,0xf5,0xff],
]

// https://lospec.com/palette-list/matriax8c
palette["matriax8c"] = [
	[0xf0,0xf0,0xdc],
	[0xfa,0xc8,0x00],
	[0x10,0xc8,0x40],
	[0x00,0xa0,0xc8],
	[0xd2,0x40,0x40],
	[0xa0,0x69,0x4b],
	[0x73,0x64,0x64],
	[0x10,0x18,0x20],
]

// https://lospec.com/palette-list/rkbv
palette["rkbv"] = [
	[0x15,0x19,0x1a],
	[0x8a,0x4c,0x58],
	[0xd9,0x62,0x75],
	[0xe6,0xb8,0xc1],
	[0x45,0x6b,0x73],
	[0x4b,0x97,0xa6],
	[0xa5,0xbd,0xc2],
	[0xff,0xf5,0xf7],
]

// -----------------------------------------------------------------------------
// -----------------------------------------------------------------------------
// -----------------------------------------------------------------------------

// https://lospec.com/palette-list/en4
palette["en4"] = [
	[0xfb,0xf7,0xf3],
	[0xe5,0xb0,0x83],
	[0x42,0x6e,0x5d],
	[0x20,0x28,0x3d],
]

// https://lospec.com/palette-list/arq4
palette["arq4"] = [
	[0xff,0xff,0xff],
	[0x67,0x72,0xa9],
	[0x3a,0x32,0x77],
	[0x00,0x00,0x00],
]

// https://lospec.com/palette-list/megaman-v-sgb
palette["megaman-v-sgb"] = [
	[0x10,0x25,0x33],
	[0x42,0x67,0x8e],
	[0x6f,0x9e,0xdf],
	[0xce,0xce,0xce],
]

// https://lospec.com/palette-list/cga-palette-1-high
palette["cga-palette-1-high"] = [
	[0x00,0x00,0x00],
	[0xff,0x55,0xff],
	[0x55,0xff,0xff],
	[0xff,0xff,0xff],
]

// TODO - move
function status(text) {
	out.innerHTML = text
}

// ---[ API ]-------------------------------------------------------------------

function color(c,a=1) {
	ctx.fillStyle = fc.pal.style[c]//.slice(0,-1)+`,${a})`
	ctx.strokeStyle = ctx.fillStyle
}

function cls(c) {
	color(c)
	rect(0,0,fc.w,fc.h)
}

function rect(x,y,w,h) {
	ctx.fillRect(x,y,w,h)
}

function circ(x,y,r) {
	ctx.beginPath()
	ctx.arc(x,y,r,0,2*Math.PI)
	ctx.fill()
}

function line(x,y,x2,y2,w=1) {
	ctx.beginPath()
	ctx.lineCap = "round"
	ctx.moveTo(x,y)
	ctx.lineTo(x2,y2)
	ctx.lineWidth = w
	ctx.stroke()
}

// ---[ TEXT ]------------------------------------------

function font(s) {
	ctx.font = s
}

function print(s,x,y) {
	ctx.fillText(s,x,y)
}

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

// ---[ OTHER ]--------------------------------------------

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
function _init() {}
function _main() {}
function _draw() {}
_before = []
_after = []

function __main() {
	for (var i in _before) {
		_before[i]()
	}
	_main()
	_draw()
	for (var i in _after) {
		_after[i]()
	}
}

fc.pal.load('pico8')
_init_screen()
//_init_bank(1,5,5,5,5,1)
_init_bank(0,5,5,5,5,
[[0,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1,1,1,1,0],[1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0],[1,1,0,1,1,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1],[1,1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1],[1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,0,1,0,1,1,0,1,1,1],[0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0],[0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0],[0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0],[1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,0,1,0,1,1,1,1,0,1],[1,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1],[1,1,1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,1],[0,1,1,1,0,1,0,0,1,1,1,0,1,0,1,1,1,0,0,1,0,1,1,1,0,0],[0,0,1,1,0,0,1,1,1,0,0,0,1,1,0,0,0,1,1,0,0,1,1,1,1],[0,1,1,1,0,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,1,1,1,0,1],[1,0,0,0,2,1,0,0,0,2,1,0,1,0,2,1,0,0,0,2,1,0,0,0,2],[2,0,0,0,1,2,0,0,0,1,2,0,1,0,1,2,0,0,0,1,2,0,0,0,1,0,1],[2,2,2,2,2,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1],[1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,2,2,2,2,2],[1,1,1,1,0,0,0,0,1,1,0,1,1,1,0,0,0,0,1,1,1,1,1,1,0],[1,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0],[0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,0,1,0,0,1,0,0,0,0,0,0,0],[1,1,1,1,0,1,0,0,1,0,1,0,1,1,1,1,1,1,0,1,0,0,1,1,1],[1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,1,1,0,1,1,1,1,0,1,1],[1,0,0,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1]]
)
_init_bank(1,3,5,7,9,
[[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1],[0,1,0,1,1,0,0,1,0,0,1,0,1,1,1],[1,1,1,0,0,1,1,1,1,1,0,0,1,1,1],[1,1,1,0,0,1,0,1,1,0,0,1,1,1,1],[1,0,1,1,0,1,1,1,1,0,0,1,0,0,1],[1,1,1,1,0,0,1,1,1,0,0,1,1,1,1],[1,1,1,1,0,0,1,1,1,1,0,1,1,1,1],[1,1,1,0,0,1,0,0,1,0,0,1,0,0,1],[1,1,1,1,0,1,1,1,1,1,0,1,1,1,1],[1,1,1,1,0,1,1,1,1,0,0,1,1,1,1],[1,1,1,1,0,1,1,1,1,1,0,1,1,0,1],[1,1,0,1,0,1,1,1,0,1,0,1,1,1,0],[0,1,1,1,0,0,1,0,0,1,0,0,0,1,1],[1,1,0,1,0,1,1,0,1,1,0,1,1,1,0],[1,1,1,1,0,0,1,1,0,1,0,0,1,1,1],[1,1,1,1,0,0,1,1,0,1,0,0,1,0,0],[1,1,1,1,0,0,1,0,1,1,0,1,1,1,1],[1,0,1,1,0,1,1,1,1,1,0,1,1,0,1],[1,1,1,0,1,0,0,1,0,0,1,0,1,1,1],[1,1,1,0,0,1,0,0,1,1,0,1,1,1,0],[1,0,1,1,0,1,1,1,0,1,0,1,1,0,1],[1,0,0,1,0,0,1,0,0,1,0,0,1,1,1],[1,1,1,1,1,1,1,0,1,1,0,1,1,0,1],[1,1,0,1,0,1,1,0,1,1,0,1,1,0,1],[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1],[1,1,1,1,0,1,1,1,1,1,0,0,1,0,0],[1,1,1,1,0,1,1,0,1,1,1,1,1,1,1],[1,1,1,1,0,1,1,1,0,1,0,1,1,0,1],[1,1,1,1,0,0,1,1,1,0,0,1,1,1,1],[1,1,1,0,1,0,0,1,0,0,1,0,0,1,0],[1,0,1,1,0,1,1,0,1,1,0,1,1,1,1],[1,0,1,1,0,1,1,0,1,1,0,1,0,1,0],[1,0,1,1,0,1,1,0,1,1,1,1,1,1,1],[1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],[1,0,1,1,0,1,1,1,1,0,1,0,0,1,0],[1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,0,0,1,0,0,1,0,0,0,0,0,1,0],[1,1,1,0,0,1,0,1,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0,1,0,1,0,0],[1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],[0,0,0,0,1,0,1,1,1,0,1,0,0,0,0],[0,0,0,1,1,1,0,0,0,1,1,1,0,0,0],[0,1,0,1,0,0,1,0,0,1,0,0,0,1,0],[0,1,0,0,0,1,0,0,1,0,0,1,0,1,0,0],[0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],[0,0,1,0,0,1,0,1,0,1,0,0,1,0,0],[0,1,0,0,1,0,0,1,0,0,1,0,0,1,0],[0,0,1,0,1,0,1,0,0,0,1,0,0,0,1],[1,0,0,0,1,0,0,0,1,0,1,0,1,0,0],[1,1,0,1,0,0,1,0,0,1,0,0,1,1,0],[0,1,1,0,0,1,0,0,1,0,0,1,0,1,1],[0,0,0,1,0,1,0,1,0,1,0,1,0,0,0],[0,0,0,0,1,0,0,0,0,0,1,0,1,0,0],[0,1,0,0,1,0,0,0,0,0,0,0,0,0,0],[1,0,1,1,1,1,1,0,1,1,1,1,1,0,1],[0,1,0,1,0,1,0,0,0,0,0,0,0,0,0],[0,1,1,0,1,0,1,1,0,0,1,0,0,1,1],[1,1,0,0,1,0,0,1,1,0,1,0,1,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],[0,1,0,0,0,1,0,0,0,0,0,0,0,0,0]]
)
bank(1)
cls(0)

window.onload = function(e) {
	_init()
	window.setInterval(__main,16.6)
}
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

function on_mouse_move(e) {
	var bcr = cnv.getBoundingClientRect()
	var bcr_left = bcr.left
	var bcr_top = bcr.top
	var bcr_w = bcr.width
	var bcr_h = bcr.height
	
	var ratio = bcr_h/fc.h
	var width = fc.w * ratio
	var bcr_left = 0.5*(bcr_w-width)
	
	MX = (e.clientX - bcr_left) / ratio
	MY = (e.clientY - bcr_top) / ratio
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
// ---[ API ]-------------------------------------------------------------------
// -----------------------------------------------------------------------------

function on_touch_start(e) {
	MX = e.touches[0].clientX
	MY = e.touches[0].clientY
	M1 = 3
}

function on_touch_end(e) {
	M1 = 0
}

function on_touch_move(e) {
	// TODO
}

function on_touch_cancel(e) {
	// TODO
}

cnv.addEventListener('touchstart',on_touch_start)
cnv.addEventListener('touchend',on_touch_end)
function on_key_press() {
	_fullscreen()
	console.log('test')
}

document.addEventListener('keypress',on_key_press)
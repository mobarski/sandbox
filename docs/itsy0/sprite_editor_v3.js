function _init() {
	new_bank(1,5,5,8,8,1)
	picker = new ColorPicker(10,10,40,20,1,2)
	viewer = new BankViewer(10,100,5,5,1)
	editor = new SpriteEditor(300,100,30,30,1)
}

function _main() {
	picker.main()
	viewer.main()
	editor.main()
}

// -----------------------------------------------------------------------------

function grid_click(btn,x,y,w,h,nx,ny=1) {
		var [s,mx,my] = mousebtn(btn)
		if (s==0 || mx<x || mx>x+w*nx || my<y || my>y+h*ny) return [0,-1,-1]
		var gx = floor((mx-x)/w)
		var gy = floor((my-y)/h)
		var n = gy*nx + gx
		return [s,n]
}

// -----------------------------------------------------------------------------

function SpriteEditor(x,y,sx,sy,m=0) {
	
	this.main = function() {
		this.react()
		this.draw()
	}
	
	this.draw = function() {
		var vs = viewer.selected
		var b = fc.bank2
		for (var row=0; row<b.sh; row++) {
			for (var col=0; col<b.sw; col++) {
				var c = sget(vs,col,row)
				rectfill(x+col*(sx+m), y+row*(sy+m),sx,sy,c)
			}
		}
		
	}
	
	this.react = function() {
		var vs = viewer.selected
		var c = picker.fg
		var b = fc.bank2
		var [s,n] = grid_click(1,x,y,sx+m,sy+m,b.sw,b.sh)
		if (s>=2) {
			var col = n % b.sw
			var row = floor(n/b.sw)
			sset(vs,col,row,c)
		}
	}
}

// -----------------------------------------------------------------------------

function BankViewer(x,y,sx,sy,m=0) {
	this.selected = 0
	
	this.main = function() {
		this.draw()
		this.react()
	}
	
	this.draw = function() {
		var col = 0
		var row = 0
		var b = fc.bank2
		for (var n in b.data) { // TODO api do pobrania tego
			rspr(n,x+row*b.sw*sx+m*row, y+col*b.sh*sy+m*col, 0,0, sx, sy)
			if (n%b.bw==b.bw-1) {
				row=0
				col++
			} else {
				row++
			}
		}
	}
	
	this.react = function() {
		var b = fc.bank2
		var [s,n] = grid_click(1,x,y,b.sw*sx+m,b.sh*sy+m,b.bw,b.bh)
		if (s==3) {
			this.selected = n
		}
	}
}

// -----------------------------------------------------------------------------

function ColorPicker(x,y,w,h,m=0,ny=1) {
	this.bg = 0
	this.fg = 1
	var per_row = floor(fc.pal.length/ny)
	
	this.main = function() {
		this.react()
		this.draw()
	}
	
	this.react = function() {
		var [s,n] = grid_click(1,x,y,w+m,h+m,per_row,ny)
		if (s==3) {
			this.fg = n
			console.log(`fg=${n}`)
		}
		var [s,n] = grid_click(2,x,y,w+m,h+m,per_row,ny)
		if (s==3) {
			this.bg = n
			console.log(`bg=${n}`)
		}
	}
	
	this.draw = function() {
		var col = 0
		var row = 0
		for (var c in fc.pal.rgb) { // TODO api do pobrania tego
			rectfill(x+row*(w+m),y+col*(h+m),w,h,c)
			if (c%per_row==per_row-1) {
				row=0
				col++
			} else {
				row++
			}
		}
	}
}


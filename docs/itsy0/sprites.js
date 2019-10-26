
function sscale(sx,sy) {
	fc.ssx = sx
	fc.ssy = sy
}

function rspr(n,x,y,flip_x=0,flip_y=0,sx=null,sy=null) {
	sx = sx || fc.ssx || 1
	sy = sy || fc.ssy || 1
	var sw = fc.bank2.sw
	var sh = fc.bank2.sh
	for (var i=0; i<sh; i++) {
		for (var j=0; j<sw; j++) {
			var _j = flip_x ? sw-1-j : j 
			var _i = flip_y ? sh-1-i : i
			var c = sget(n,_j,_i)
			rectfill(x+j*sx, y+i*sy, sx, sy, c)
			//console.log(x+j*sx, y+i*sy, sx, sy, c)
		}
	}
}


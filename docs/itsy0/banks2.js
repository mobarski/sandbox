fc.banks2 = {}
fc.bank2 = null
fc.b2 = null

// ---[ API ]-------------------------------------------------------------------

function new_bank(b,bw,bh,sw=8,sh=8,c=0) {
	var bank = {}
	bank.bw = bw
	bank.bh = bh
	bank.sw = sw
	bank.sh = sh
	if (Array.isArray(c)) {
		bank.data = c
	} else {
		bank.data = []
		for (var i=0; i<Math.floor(bh/sh); i++) {
			for (var j=0; j<Math.floor(bw/sw); j++) {
				var spr = Array(sw*sh).fill(c)
				bank.data.push(spr)
			}
		}
		
	}
	fc.banks2[b] = bank
}

function bank2(b=null) {
	console.log(`switching bank2 to ${b}`)
	var b_prev = fc.b2
	if (b!=null) {
		fc.b2 = b
	}
	fc.bank2 = fc.banks2[fc.b2]
	return b_prev
}

function sget(n,x,y) {
	return fc.bank2.data[n][x+y*fc.bank2.sw]
}

function sset(n,x,y,c) {
	var prev = fc.bank2.data[n][x+y*fc.bank2.sw]
	fc.bank2.data[n][x+y*fc.bank2.sw] = c
	return prev
}

// -----------------------------------------------------------------------------

function _spr_get(n) {
	return fc.bank2.data[n]
}

function _data_to_array(data,bw,bh,sw,sh) {
	var out = Array(bw*bh).fill(0)
	var bw_n = Math.floor(bw/sw)
	var bh_n = Math.floor(bh/sh)
	for (var i=0; i<bh_n; i++) {
		for (var j=0; j<bw_n; j++) {
			var n = j+i*bw_n
			var spr = data[n]
			for (var y=0; y<sh; y++) {
				for (var x=0; x<sw; x++) {
					var spr_i = x + y*sw
					var out_i = i*bw*sh + j*sw + x + y*bw
					out[out_i] = spr[spr_i]
					// console.log(`${i} ${j} ${y} ${x} -> ${spr[spr_i]} @ ${out_i}`)
				}
			}
		}
	}
	return out
}

function _array_to_data(ar,bw,bh,sw,sh) {
	var out = []
	var bw_n = Math.floor(bw/sw)
	var bh_n = Math.floor(bh/sh)
	for (var i=0; i<bh_n; i++) {
		for (var j=0; j<bw_n; j++) {
			var n = j+i*bw_n
			var spr = Array(sw*sh).fill(0)
			for (var y=0; y<sh; y++) {
				for (var x=0; x<sw; x++) {
					var spr_i = x + y*sw
					var ar_i = i*bw*sh + j*sw + x + y*bw
					spr[spr_i] = ar[ar_i]
				}
			}
			out.push(spr)
		}
	}
	return out
}

function _array_to_compact_imagedata(ar,w,h=null) {
	h = h || Math.ceil(ar.length / w / 4)
	var img = ctx.createImageData(w,h)
	for (var i=0; i<w*h*4; i++) {
		if (i<ar.length) {
			var v = ar[i]
			img.data[i] = v>0 ? 256-v : 0
		} else {
			img.data[i] = 1
		}
	}
	return img
}

function _compact_imagedate_to_array(img,n) {
	var ar = []
	for (var i=0; i<n; i++) {
		var v = img.data[i]
		ar.push(v>0 ? 256-v : 0)
	}
	return ar
}

function _array_to_packed_array(ar,max_v) {
	var out = []
	var n = 1
	var k = 0
	if (max_v==1) 				n=8
	if (max_v>1 && max_v<4) 	n=4
	if (max_v>3 && max_v<16) 	n=2
	
	var val = 0
	var j
	for (var i in ar) {
		j = i%n
		var v = max(0,min(ar[i],max_v))
		val |= v
		if (j==n-1) {
			out.push(val)
			val = 0
		} else {
			val <<= 8/n
		}
	}
	if (j != n-1) {
		out.push(val)
	}
	return out
}

function _packed_array_to_array(ar,max_v) {
	var out = []
	var m = 255
	var n = 1
	if (max_v==1) 				{n=8;m=1}
	if (max_v>1 && max_v<4) 	{n=4;m=3}
	if (max_v>3 && max_v<16) 	{n=2;m=15}

	for (var i in ar) {
		var batch = []
		var v = ar[i]
		for (var j=0; j<n; j++) {
			var val = v&m
			batch.unshift(val)
			v >>= 8/n
		}
		for (var j in batch) {
			out.push(batch[j])
		}
	}
	return out
}

// ---[ TEST ]---

if (0) {
	new_bank(1,4,4,2,2)
	bank2(1)
	sset(0,0,0,10)
	sset(0,1,0,11)
	sset(0,0,1,12)
	sset(0,1,1,13)
	sset(1,0,0,20)
	sset(1,1,0,21)
	sset(1,0,1,22)
	sset(1,1,1,23)
	sset(2,0,0,30)
	sset(2,1,0,31)
	sset(2,0,1,32)
	sset(2,1,1,33)
	sset(3,0,0,40)
	sset(3,1,0,41)
	sset(3,0,1,42)
	sset(3,1,1,43)
	d=fc.bank2.data
	a=_data_to_array(d,4,4,2,2)
	d2=_array_to_data(a,4,4,2,2)
	a2=_data_to_array(d2,4,4,2,2)
}
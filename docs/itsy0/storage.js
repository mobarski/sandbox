// TODO: jakis dodatkowy prefix

function save(key,value) {
	localStorage['itsy_'+key] = JSON.stringify(value)
}

function load(key,_default=null) {
	var val = localStorage['itsy_'+key]
	if (val) {
		return JSON.parse(val)
	} else {
		return _default
	}
}

// -----------------------------------------------------------------------------

const CODE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"
const RLCHAR = '.'

function _run_len_encode(data) {
	var out = ""
	for (var i=0; i<data.length;) {
		var x = data[i]
		var n = 1
		for (var j=1; j<CODE.length && i+j<=data.length && j<64; j++) {
			var x2 = data[i+j]
			if (x==x2 && n<63) {
				n++
			} else if (n>=4) {
				out += RLCHAR
				out += CODE[n]
				out += CODE[x]
				i+=n-1
				break
			} else {
				out += CODE[x]
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
		if (c==RLCHAR) {
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

// -----------------------------------------------------------------------------


function _array_to_packed_array(ar,max_v,n1=8,n2=4,n3=2,n4=2) {
	var out = []
	var n = 1
	var k = 0
	if (max_v==1) 				n=n1
	if (max_v>1 && max_v<4) 	n=n2
	if (max_v>3 && max_v<8) 	n=n3
	if (max_v>7 && max_v<16) 	n=n4
	
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

function _packed_array_to_array(ar,max_v,n1=8,n2=4,n3=2,n4=2) {
	var out = []
	var b = 8
	var m = 255
	var n = 1
	if (max_v==1) 				{b=1;n=n1;m=1}
	if (max_v>1 && max_v<4) 	{b=2;n=n2;m=3}
	if (max_v>3 && max_v<8) 	{b=3;n=n3;m=7}
	if (max_v>7 && max_v<16) 	{b=4;n=n4;m=15}

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

// -----------------------------------------------------------------------------

function _array_to_compact_imagedata(ar,w,h=null) {
	var h = h || Math.ceil(ar.length / w / 3)
	var img = ctx.createImageData(w,h)
	img.data.fill(0)
	var j = 0
	for (var i in ar) {
		var v = ar[i]
		img.data[j] = v>0 ? 256-v : 0
		j++
		if (i%3==2) {
			img.data[j] = 255
			j++
		}
	}
	return img
}


// MOVE TO STORAGE ???
function _compact_imagedate_to_array(data) {
	var ar = []
	for (var i in data) {
		if (i%4<3) {
			var v = data[i]
			ar.push(v>0 ? 256-v : 0)
		}
	}
	return ar
}

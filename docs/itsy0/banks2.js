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

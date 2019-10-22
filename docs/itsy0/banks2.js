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

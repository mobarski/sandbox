// TODO: jakis dodatkowy prefix

function save(key,value) {
	localStorage['itsy_'+key] = JSON.stringify(value)
}

function load(key) {
	return JSON.parse(localStorage['itsy_'+key])
}

function _run_len_encode(text) {
	const code = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	var out = ""
	for (var i=0; i<text.length;) {
		var c = text[i]
		var n = 1
		for (var j=1;j<code.length && i+j<=text.length;j++) {
			var c2 =text[i+j]
			//console.log(`i:${i} j:${j} c:${c} c2:${c2}`)
			if (c==c2) {
				n++
			} else if (n>=4) {
				out += '_'
				out += code[n]
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

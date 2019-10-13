// --- [ API ]------------------------------------------------------------------

function bank(b) {
	fc.b = b
	fc.bank = fc.banks[b]
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
	// const code = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
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
	// return out
}

function _loads_bank(b,raw) {
	var bank = {}
	const code = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
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

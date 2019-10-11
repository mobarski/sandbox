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
	bank.data = []
	for (var i=0; i<nx*ny; i++) {
		var a = new Array(w*h)
		for (j=0; j<w*h; j++) a[j]=c
		bank.data.push(a)
	}
	fc.banks[b] = bank
}

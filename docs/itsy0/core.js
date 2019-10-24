function _init() {}
function _main() {}
function _draw() {}

// TODO: rename: call_before_main, call_after_init OR schedule_after_init
_before = []
_after = []
_before_init = []
_after_init = []

function __init() {
	for (var i in _before_init) { _before_init[i]() }
	_init()
	for (var i in _after_init) { _after_init[i]() }
}

function __main() {
	var t0 = now()
	for (var i in _before) { _before[i]() }
	fc.t1 = now() - t0
	_main()
	fc.t2 = now() - t0
	_draw()
	fc.t3 = now() - t0
	for (var i in _after) { _after[i]() }
	fc.t4 = now() - t0
}

window.onload = function(e) {
	__init()
	__main()
	if (fc.freq && fc.freq>0) {
		window.setInterval(__main,1000.0/fc.freq)
	}
}

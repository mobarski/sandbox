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
	for (var i in _before) { _before[i]() }
	_main()
	_draw()
	for (var i in _after) { _after[i]() }
}

window.onload = function(e) {
	__init()
	window.setInterval(__main,1000.0/fc.freq)
}

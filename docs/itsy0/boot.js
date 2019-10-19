// function _init() {}
// function _main() {}
// function _draw() {}
// _before = []
// _after = []
// _before_init = []
// _after_init = []


// function __init() {
	// for (var i in _before_init) { _before_init[i]() }
	// _init()
	// for (var i in _after_init) { _after_init[i]() }
// }

// function __main() {
	// for (var i in _before) { _before[i]() }
	// _main()
	// _draw()
	// for (var i in _after) { _after[i]() }
// }

// --------------

fc.pal.load('pico8')
_init_screen()
//_init_bank(1,5,5,5,5,1)
_init_bank(0,5,5,5,5,
[[0,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1,1,1,1,0],[1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0],[1,1,0,1,1,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1],[1,1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1],[1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,0,1,0,1,1,0,1,1,1],[0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0],[0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0],[0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0],[1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,0,1,0,1,1,1,1,0,1],[1,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1],[1,1,1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,1],[0,1,1,1,0,1,0,0,1,1,1,0,1,0,1,1,1,0,0,1,0,1,1,1,0,0],[0,0,1,1,0,0,1,1,1,0,0,0,1,1,0,0,0,1,1,0,0,1,1,1,1],[0,1,1,1,0,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,1,1,1,0,1],[1,0,0,0,2,1,0,0,0,2,1,0,1,0,2,1,0,0,0,2,1,0,0,0,2],[2,0,0,0,1,2,0,0,0,1,2,0,1,0,1,2,0,0,0,1,2,0,0,0,1,0,1],[2,2,2,2,2,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1],[1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,2,2,2,2,2],[1,1,1,1,0,0,0,0,1,1,0,1,1,1,0,0,0,0,1,1,1,1,1,1,0],[1,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0],[0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,0,1,0,0,1,0,0,0,0,0,0,0],[1,1,1,1,0,1,0,0,1,0,1,0,1,1,1,1,1,1,0,1,0,0,1,1,1],[1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,1,1,0,1,1,1,1,0,1,1],[1,0,0,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1]]
)
_init_bank(1,3,5,7,9,
[[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1],[0,1,0,1,1,0,0,1,0,0,1,0,1,1,1],[1,1,1,0,0,1,1,1,1,1,0,0,1,1,1],[1,1,1,0,0,1,0,1,1,0,0,1,1,1,1],[1,0,1,1,0,1,1,1,1,0,0,1,0,0,1],[1,1,1,1,0,0,1,1,1,0,0,1,1,1,1],[1,1,1,1,0,0,1,1,1,1,0,1,1,1,1],[1,1,1,0,0,1,0,0,1,0,0,1,0,0,1],[1,1,1,1,0,1,1,1,1,1,0,1,1,1,1],[1,1,1,1,0,1,1,1,1,0,0,1,1,1,1],[1,1,1,1,0,1,1,1,1,1,0,1,1,0,1],[1,1,0,1,0,1,1,1,0,1,0,1,1,1,0],[0,1,1,1,0,0,1,0,0,1,0,0,0,1,1],[1,1,0,1,0,1,1,0,1,1,0,1,1,1,0],[1,1,1,1,0,0,1,1,0,1,0,0,1,1,1],[1,1,1,1,0,0,1,1,0,1,0,0,1,0,0],[1,1,1,1,0,0,1,0,1,1,0,1,1,1,1],[1,0,1,1,0,1,1,1,1,1,0,1,1,0,1],[1,1,1,0,1,0,0,1,0,0,1,0,1,1,1],[1,1,1,0,0,1,0,0,1,1,0,1,1,1,0],[1,0,1,1,0,1,1,1,0,1,0,1,1,0,1],[1,0,0,1,0,0,1,0,0,1,0,0,1,1,1],[1,1,1,1,1,1,1,0,1,1,0,1,1,0,1],[1,1,0,1,0,1,1,0,1,1,0,1,1,0,1],[1,1,1,1,0,1,1,0,1,1,0,1,1,1,1],[1,1,1,1,0,1,1,1,1,1,0,0,1,0,0],[1,1,1,1,0,1,1,0,1,1,1,1,1,1,1],[1,1,1,1,0,1,1,1,0,1,0,1,1,0,1],[1,1,1,1,0,0,1,1,1,0,0,1,1,1,1],[1,1,1,0,1,0,0,1,0,0,1,0,0,1,0],[1,0,1,1,0,1,1,0,1,1,0,1,1,1,1],[1,0,1,1,0,1,1,0,1,1,0,1,0,1,0],[1,0,1,1,0,1,1,0,1,1,1,1,1,1,1],[1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],[1,0,1,1,0,1,1,1,1,0,1,0,0,1,0],[1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,0,0,1,0,0,1,0,0,0,0,0,1,0],[1,1,1,0,0,1,0,1,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,0,1,0,1,0,0],[1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],[0,0,0,0,1,0,1,1,1,0,1,0,0,0,0],[0,0,0,1,1,1,0,0,0,1,1,1,0,0,0],[0,1,0,1,0,0,1,0,0,1,0,0,0,1,0],[0,1,0,0,0,1,0,0,1,0,0,1,0,1,0,0],[0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],[0,0,1,0,0,1,0,1,0,1,0,0,1,0,0],[0,1,0,0,1,0,0,1,0,0,1,0,0,1,0],[0,0,1,0,1,0,1,0,0,0,1,0,0,0,1],[1,0,0,0,1,0,0,0,1,0,1,0,1,0,0],[1,1,0,1,0,0,1,0,0,1,0,0,1,1,0],[0,1,1,0,0,1,0,0,1,0,0,1,0,1,1],[0,0,0,1,0,1,0,1,0,1,0,1,0,0,0],[0,0,0,0,1,0,0,0,0,0,1,0,1,0,0],[0,1,0,0,1,0,0,0,0,0,0,0,0,0,0],[1,0,1,1,1,1,1,0,1,1,1,1,1,0,1],[0,1,0,1,0,1,0,0,0,0,0,0,0,0,0],[0,1,1,0,1,0,1,1,0,0,1,0,0,1,1],[1,1,0,0,1,0,0,1,1,0,1,0,1,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],[0,1,0,0,0,1,0,0,0,0,0,0,0,0,0]]
)
bank(1)
cls(0)

// window.onload = function(e) {
	// __init()
	// window.setInterval(__main,16.6)
// }

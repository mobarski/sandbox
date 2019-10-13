function _init() {}
function _main() {}
_after = []

function __main() {
	_main()
	for (var i in _after) {
		_after[i]()
	}
}

fc.pal.load('pico8')
_init_screen()
//_init_bank(1,5,5,5,5,1)
_init_bank(0,5,5,5,5,
[[0,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1,1,1,1,0],[1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0],[1,1,0,1,1,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1],[1,1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1],[1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,0,1,0,1,1,0,1,1,1],[0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0],[0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0],[0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0],[1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,0,1,0,1,1,1,1,0,1],[1,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1],[1,1,1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,1],[0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,1,1,0,0,0,1],[1,0,0,0,2,1,0,0,0,2,1,0,1,0,2,1,0,0,0,2,1,0,0,0,2],[2,0,0,0,1,2,0,0,0,1,2,0,1,0,1,2,0,0,0,1,2,0,0,0,1,0,1],[2,2,2,2,2,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1],[1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,2,2,2,2,2],[0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,0,0,1,1,0,0,0,1,1],[1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1],[0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,0,1,0,0,1,0,0,0,0,0,0,0],[1,1,1,1,0,1,0,0,1,0,1,0,1,1,1,1,1,1,0,1,0,0,1,1,1],[1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,1,1,0,1,1,1,1,0,1,1],[1,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,1,0,1,0,0,1,1,1]]
)
_init_bank(1,5,5,5,5,
[[0,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1,1,1,1,0],[1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0],[1,1,0,1,1,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1],[1,1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1],[1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,0,1,0,1,1,0,1,1,1],[0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0],[0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0],[0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,1,1,1,0,0,0,1,0,0],[1,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,0,1,0,1,1,1,1,0,1],[1,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1],[1,1,1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,1],[0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,0,0,1,1,0,0,0,1],[1,0,0,0,2,1,0,0,0,2,1,0,1,0,2,1,0,0,0,2,1,0,0,0,2],[2,0,0,0,1,2,0,0,0,1,2,0,1,0,1,2,0,0,0,1,2,0,0,0,1,0,1],[2,2,2,2,2,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1],[1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,2,2,2,2,2],[0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,0,0,1,1,0,0,0,1,1],[1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1],[0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,0,1,0,0,1,0,0,0,0,0,0,0],[1,1,1,1,0,1,0,0,1,0,1,0,1,1,1,1,1,1,0,1,0,0,1,1,1],[1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,1,1,0,1,1,1,1,0,1,1],[1,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,1,0,1,0,0,1,1,1]]
)
bank(1)
cls(0)

window.onload = function(e) {
	_init()
	window.setInterval(__main,16.6)
}

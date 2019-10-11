// TODO: jakis dodatkowy prefix

function save(key,value) {
	localStorage['itsy_'+key] = JSON.stringify(value)
}

function load(key) {
	return JSON.parse(localStorage['itsy_'+key])
}

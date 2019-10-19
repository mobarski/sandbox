function font(s) {
	ctx.font = s
}

function print(s,x,y) {
	ctx.fillText(s,x,y)
}

// TODO: rename
function measure(s) {
	return ctx.measureText(s).width
}

function xprint(s,x,y,align='center',base='middle') {
	ctx.textAlign = align
	ctx.textBaseline = base
	ctx.fillText(s,x,y)
	ctx.textAlign = 'left'
	ctx.textBaseline = 'top'
}

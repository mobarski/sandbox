function INIT()
	screen(100,100,6)
end

function DRAW()
	local x,y
	cls()
	color(6)
	cursor(20,20)
	x,y = print('hello\nworld')
	rect(20,20,x-20,y-20,3)
end

function INIT()
	screen(320,200,4)
	print('ok')
end

function DRAW()
	cursor(8,8)
	print("hello")
	print('world',nil,16)
	print('to jest bardzo ^5dlugi^2 tekst ktory\npowinien\n^^zlamac\nlinie',100,100)
end


function POST()
	love.graphics.setColor(0,0,0,1)
	if false then for y = 4,scrh*scrs,4 do
		love.graphics.line(0,y,scrw*scrs,y)
	end end 
	if false then for x = 4,scrw*scrs,4 do
		love.graphics.line(x,0,x,scrh*scrs)
	end end
end

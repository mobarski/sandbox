function INIT()
	trace(love.filesystem.getSource())
	sfx = love.sound.newSoundData(8,8000,8,1)
	sfx:setSample(0,-1)
	sfx:setSample(1,-1)
	sfx:setSample(2,-0.5)
	sfx:setSample(3,-0.5)
	sfx:setSample(4,0)
	sfx:setSample(5,0)
	sfx:setSample(6,0.5)
	sfx:setSample(7,0.5)
	src = love.audio.newSource(sfx)
	--data = love.filesystem.newFileData('aAzA01Az','test.wav')
	--src2 = love.audio.newSource(data,'static')
	src3 = love.audio.newSource('pluck-pcm8.wav','static')
	src3:setPitch(3.0)
end

function DRAW()
	cls()
	if keyp('up') then
		cls(4)
		love.audio.play(src3)
	end
	if key('down') then
		cls(8)
		src:setPitch(3.0)
		love.audio.play(src)
	end
	if key('left') then
		cls(8)
		src:setPitch(0.5)
		love.audio.play(src)
	end
	if key('right') then
		cls(8)
		src:setPitch(5.0)
		love.audio.play(src)
	end	
end

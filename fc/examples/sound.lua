function INIT()
	trace(love.filesystem.getSource())
	sfx = love.sound.newSoundData(4,8192,8,1)
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
end

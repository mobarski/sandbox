-------------------------------------------------------------------------------

ITSY v0.1
Author: Maciej Obarski -- mobarski@gmail.com

-------------------------------------------------------------------------------

API
===

Program Structure
-----------------
		
	_init()
	
	_main()
	
	_draw()
	
	
Graphics
--------

	color  c [a]
		
		Sets the current color and alpha
	
	
	cls  [c] [a]
	
		Clears the screen
	
	
	rect  x y w h [c] [a]
	
		Draws a filled rectangle
		
	
	circ  x y r [c] [a]
	
		Draws a filled circle
		
	
	line  x y x2 y2 [width=1] [cap=round]
	
		Draws a line


	camera  x y [sx=1] [sy=1]
	
		Sets the screen offset and drawing scale
	
	
	fullscreen
	
		Starts the fullscreen mode
		
	
	shape  x y dots [c] [a]
	
		Draws a filled shape
	
	
	TODO mesh x y dots [width] [cap] [c] [a]
	
		...
		
	
	snapshot  [image=false] [x y] [w h]
	
		Returns ImageData or Image from the canvas or its fragment
	
	
	palette  p
	
		Change palette. Argument p can be palette slug from lospec.com or string of #rrggbb values
	
	
	pal  [c] [c2]
	
		Draw color c as c2.
		Without arguments: reset all remappings.
		With one argument: reset remapping for this color.
	
	
Text
----

	print str x y [c] [a]
	
		Prints a string
	
	
	measure str
	
		Return text width in pixels
	
	
	font x
	
		Sets the font


	TODO cursor  x y
	
		Sets the cursor position and carriage return margin


Math
----

	max  x y
	min  x y
	mid  x y z
	
	floor  x
	ceil   x
	sign   x
	
	sin  x
	cos  x
	
	atan2  x y
	
	abs  x
	rnd  x
	srnd  x -- TODO
	
	exp  x
	log  x
	pi


Time
----

	now
	
		Returns miliseconds since 1970-01-01
	
	
Network
-------

	api_get  url f
	
		Get JSON object from url and pass it to function f
	
	
	api_post  url data f
	
		Post data as JSON to url and pass the response to function f
		

Bank
----

	-- 16x10 spriteow 8x8 + metadane 1/2/3/4 pix na spr
   

Storage
-------

	save  key value
	
		Save value in local storage
		
	
	load  key

		Load value from local storage


	-- TODO storage to/from image


Mouse / Touch
-------------

	grid_click -- TODO
	
	
Keyboard
--------



Roadmap
=======

	0.2 - Banks & Sprites
	
		Banks
			+ encode
			+ decode
			- bank geometry
			- bank save
			- bank load
			- get single sprite
			- set single sprite
			- get multi-sprite
			- set multi-sprite
		
		Sprites
	
	0.3 - Sprite Editor & Fonts
		
		Sprite Editor
		
		Fonts
	
	0.4 - Map & Map editor
	
		Map
		
		Map Editor
		
	0.5 - GIF Recorder
	
	0.6 - Sound
		
	0.7 - Music
	
	Shader-like-effects
	
	Multitouch
	
	
	
-------------------------------------------------------------------------------

Reference
=========

	pico8 -- https://www.lexaloffle.com/pico-8.php?page=manual



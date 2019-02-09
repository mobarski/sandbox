# ITSY-8

## About

**ITSY-8** is a framework that you can use to make, play and share tiny retro-looking games and programs.

Its API is similar to the API of the most popular fantasy console - PICO-8

- TODO - something about focus on low cost of development
- TODO - something about fantasy consoles + changable resolution + sprite size
- TODO - something about smartphones
- TODO - something about learning / teaching

## Roadmap

- graphics API
- gif recorder
- map API
- input API
- sprite editor
- audio API [x]prototype
- map editor
- shell
- code editor
- sfx editor
- net API

## API

ITSY-8 is in the experimental phase. API may change at any time without notice.

### Program Structure

```
	_init
	
		Function called once on program startup.
	
	
	_update
	
		Main function that will be called at 60 fps.

	
	_draw

		Function called once per visible frame.

	
```

### Graphics
```
	screen w h [scale] [pal]
	
		Set screen resolution to width w and height h
		
		Options:
			scale - upscale factor
			pal - palete string with color definitions in the #rrggbb format
		

	spr s x y [w=1 h=1] [flip_x flip_y]

		Draw sprite number s at position x,y
		
		Options:
			w - width in tiles
			h - height in tiles
			flip_x - flip on x axis (swap left and right)
			flip_y - flip on y axis (swap up and down)
		

	sprite s x y [fx=0 fy=0] [rot=1 scale=1] [w=1 h=1]
	
		Draw sprite number s at position x,y and perform transformations.
		
		Options:
			fx - flip on x axis (swap left and right)
			fy - flip on y axis (swap up and down)
			rot - rotation (0.5: half rotation, 1.0: full rotation, etc)
			scale - upscale factor
			w - width in tiles
			h - height in tiles
			
		

	shadow s x y [w=1 h=1] [c] [b]
	
		Draw shadow of sprite s (width w and height h) at position x,y
		Every sprite color that is not transparent will be drawn as color c


	print text [x y] [c] {options} -> x2 y2

		Print text at x,y with color c
		Returns bottom right coordinates of last character
		
		Options:
			sx - scale x
			sy - scale y
			xmin - left margin (defaults to x)
			xmax - right margin (defaults to screen width)
			sim - don't print but calculate output values
			

	cursor [x y]
	
		Move text cursor to x,y (pixels)


	cls [c]

		Clear the screen, reset the clipping rectangle and text cursor


	color c
	
		Set the default color

	
	nocolor [c]
	
		Set the color that will be transparent
		nocolor() to disable transparency
			
	
	line x0 y0 x1 y1 [c]

		Draw line with color c


	rect x y w h [c]
	rectfill x y w h [c]
	
		Draw a rectangle or filled rectangle at x,y
		with width w, height h and color c


	circ x y r [c]
	circfill x y r [c]
	
		Draw a circle or filled circle at x,y
		with radius r and color c


	tri x0 y0 x1 y1 x2 y2 [c]
	trifill x0 y0 x1 y1 x2 y2 [c]
	
		Draw a triangle or filled triangle

	pset x y [c]
	
		...
		
		
	pget x y
		
		...
	
	fillp [pattern=0]
	
		...
		
	
	camera [x y]

		Set screen offset to x,y
		camera() to reset


	clip [x y w h]
		
		BUGS
		
		Limit drawing to given rectangular region
		clip() to reset
			

	pal c [r g b]
	
		Set color c to specific r,g,b values
		pal(c) returns r,g,b values for color c
		
```

### Map

```
	map x y [p] [remap=nil]
	
		Draw map page p at position x,y
		remap: function that will be 
			remap tile x y -> tile 
	

	mget mx my [r]
	
		Get map tile at position mx,my
			
			
	mset mx my v [r]
	
		Set map tile at cell mx,my to value v
	
	
	page p
	
		Set map page
	
```

### Input

```
	key name -> pressed
	
		Check if key is pressed in the current frame
	
	
	keyp name -> pressed
	
		Check if key is pressed and was not pressed in the previous frame
	
	
	mouse -> x,y,b1,b2,b3
	
		Return mouse x,y coordinates and mouse button states
	
	
	touch -> x1,y1,x2,y2,x3,y3,x4,y4
		
		...
		
	
	
```

### Assets

```
	import_bank b path
	
		Import bank b from png image
		
		
	export_bank b path
	
		Export bank b as png image
		
		
	bank_from_text  text chars values [w=128 h=128] [eol]
	
		...
		
		
	map_from_text  text chars values w h [eol]
	
		...
	
	
```

### Audio

```
```

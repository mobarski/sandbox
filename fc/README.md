# ITSY-8

## About

**ITSY-8** is a fantasy computer that you can use to make, play and share tiny retro-looking games and programs.

- TODO - something about changable resolution
- TODO - something about smartphones
- TODO - something about low cost of development
- TODO - something about children

## Roadmap

- graphics API
	- banks as greyscale -> [x]spr [x]map [ ]font
	- all banks are equal (font vs map/spr)
	- get/set pixel
	- shadow options
	- spr options
	- screen options (#colors,pal_from_str)
	- pal as in pico ?
	- print options
	- fillp
- map API
- input API
- sprite editor
- map editor
- shell
- gif recorder
- code editor
- audio API
- sfx editor
- net API

## API

ITSY-8 is in the experimental phase. API may change at any time without notice.

### Program Structure

```
	INIT
	
		Function called once on program startup.
	
	
	MAIN
	
		Main function that will be called at 60 fps.

	
	
	DRAW

		Function called once per visible frame.

	
```

### Graphics
```
	screen w h [scale] [colors=16]
	
		Set screen resolution to width w and height h
		then upscale by integer factor.
		Set number of colors.

	spr s x y [w=1 h=1] {transformations}

		Draw sprite number s (width w and height h) at position x,y
		
		Perform transformations:
			fx - flip x
			fy - flip y
			sx - scale x
			sy - scale y
			shx - shear x
			shy - shear y
			rot - rotate (1: 90 deg, 2: 180 deg, 3: 270 deg)

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
	
	
	camera [x y]

		Set screen offset to -x,-y
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
	
		Check key state in current frame
			
	
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

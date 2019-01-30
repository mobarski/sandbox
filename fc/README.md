# ITSY-8

## API

### Program Structure

```
	INIT
	
		...
	
	MAIN
	
		...
	
	
	DRAW
	
		...
	

```

### Graphics
```
	screen w h [scale]
	
		Set screen resolution to width w and height h
		then upscale by integer factor

	spr s x y [w=1 h=1] {transformations}

		Draw sprite number s (width w and height h) at position x,y
		and perform transformations
			fx - flip x
			fy - flip y
			sx - scale x
			sy - scale y
			shx - shear x
			shy - shear y
			rot - rotate (1: 90deg, 2: 180 deg, 3: 270 deg)

	print text [x y] [c] [sx=1 sy=1]

		Print text at x,y with color c
			

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
	key name
	
		Check key state in current frame
			
	
	mouse -> x,y,b1,b2,b3
	
		Return mouse x,y coordinates and mouse button states
	
	
```

### Audio

```
```

### Assets

```
```

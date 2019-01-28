# ITSY-8

## API

### Program Structure

```
	INIT
	
	MAIN
	
	DRAW
```

### Graphics
```
	screen w h [scale]
	
		Set screen resolution to width w and height h
		then upscale by integer factor

	spr s x y [w h] [flip_x] [flip_y]

		Draw sprite number s at position x,y
		width w and height h 


	print text [x y] [c]

		Print text at x,y with color c
			

	cls [c]

		Clear the screen and reset the clipping rectangle


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

		Set screen offset to x,y
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
	map x y p
	
		Draw map at position x,y
		
	
	mget mx my
	
		Get map tile at position mx,my
			
			
	mset mx my v
	
		Set map tile at cell mx,my to value v
	
	
	
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

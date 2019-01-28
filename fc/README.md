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
	spr s x y [w h] [flip_x] [flip_y]

			...


	print text [x y] [c]

			...
			

	cls [c]

			...


	color c
			...

	
	nocolor c
			...
			
			
	
	line x0 y0 x1 y1 [c]

			...


	rect x y w h [c]
	rectfill x y w h [c]
	
			Draw a rectangle or filled rectangle at x,y with width w and height h


	circ x y r [c]
	circfill x y r [c]
	
			Draw a circle or filled circle at x,y with radius r


	tri x0 y0 x1 y1 x2 y2 [c]
	trifill x0 y0 x1 y1 x2 y2 [c]
	
			...
	
	camera [x y]

			...


	clip [x y w h]

			...
			

	pal c [r g b]
	
			...
		
	
```

### Map

```
	map x y p
	
			...
		
	
	mget mx my
	
			...
			
			
	mset mx my v
	
			...
	
	
	
	
```

### Input

```
	key
	
			...
			
	
	keyp
	
			...
			
	
	mouse
	
			...
	
	

```

### Audio

```
```

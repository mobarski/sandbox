from util import *

m=model()
m.lift		= lambda m:	m.lift_coefficient*(0.5*m.density*m.velocity**2)*m.wing_surface
m.drag	= lambda m:	m.drag_coefficient*(0.5*m.density*m.velocity**2)*m.wing_surface
m.thrust	= lambda m:	0
m.weight	= lambda m:	0


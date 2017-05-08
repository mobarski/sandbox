from util import *

m=model()
m.lift_fun		= lambda m: m.lift_coefficient*(0.5*m.density*m.velocity**2)*m.wing_surface
m.drag_fun	= lambda m: m.drag_coefficient*(0.5*m.density*m.velocity**2)*m.wing_surface
m.thrust_fun	= lambda m: 0
m.weight_fun	= lambda m: 0


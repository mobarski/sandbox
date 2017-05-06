from util import *

m=model()
m.get_lift = lambda: m.lift_coefficient*(0.5*m.density*m.velocity**2)*m.wing_surface
m.get_drag = lambda: m.drag_coefficient*(0.5*m.density*m.velocity**2)*m.wing_surface
m.get_thrust = lambda: 0
m.get_weight = lambda: 0


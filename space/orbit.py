from util import *
from math import *
from const import *

m = model()
m.f_grav = lambda m:	m.GM * m.mass / m.distance**2
m.f_cent = lambda m:	m.velocity**2 / m.distance
m.e_pot = lambda m:	-m.GM * m.mass / m.distance
m.e_kin = lambda m:	m.mass * m.velocity**2 / 2

m.a_grav = lambda m:	m.GM / m.distance**2
m.velocity = lambda m:	(2*m.GM/m.distance - m.GM/m.a)**0.5
m.t_orb = lambda m:	2*pi*(m.a**3/m.GM)**0.5
m.a_doc = "semi-major axis [m]"
m.a = lambda m:		m.distance
m.n_doc = "mean motion"
m.n = lambda m:		(m.GM / m.a**3)**0.5

if __name__=="__main__":
	m.GM = GM.earth
	m.distance = R.earth + 200e3
	m.mass = 100
	print(m.velocity)

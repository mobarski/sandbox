from formula3 import formula
from const import *
from math import *

v_circ = formula("circular orbit velocity",
	v='({u}/{r})**0.5',
	u='{r}*{v}**2',
	r='{u}/{v}**2')

v_elip = formula("elipse orbit velocity",
	v='(2*{u}/{r}-{u}/{a})**0.5',
	u='{r}*{v}**2',
	r='{u}/{v}**2')

delta_v = formula("",
	dv='g*isp*log(mi/mf)')

f_grav= formula("gravitational force",
	fg="{u}*{m}/{r}**2")

f_c = formula("centrifugal force",
	fc="{v}**2/{r}")

e_pot = formula("",
	ep="-{u}*{m}/{r}"

e_kin = formula("",
	ek="v**2*m/2")

t = formula("orbital period",
	t="2*pi*({a}**3/{u})**0.5")

ecc = formula('eccentricity',
	e='({ra}-{rp})/({ra}+{rp})'

n = formula('mean motion',
	n="({u}/{a}**3)**0.5")

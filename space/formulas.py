from formula3 import formula
from const import *

v_circ = formula("circular orbit velocity",
	v='({u}/{r})**0.5',
	u='{r}*{v}**2',
	r='{u}/{v}**2')

v_elip = formula("elipse orbit velocity",
	v='(2*{u}/{r}-{u}/{a})**0.5',
	u='{r}*{v}**2',
	r='{u}/{v}**2')

print(v_elip.v.explain)

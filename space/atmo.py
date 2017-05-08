from math import *
from util import *

## CONST ############################################

#R=namespace('specific gas constant [J/(kg*K)]')
#R.air = 287.00

# EARTH ISA (International Standard Atmosphere)

# h=0m t=288.15K=15C rho=1.225 kg/m3 p=101325Pa

g = 9.80665
R = 287.00

## MODELS ###########################################

# 0c=273.15K
levels = [ # h[m] a[K/km] t[K] rho[kg/m3] p[N/m2]
[0,		-6.5,	288.15,	1.225,	101325],
[11e3,	0,		None,	None,	None],
[20e3,	+1.0,	None,	None,	None],
[32e3,	+2.8,	None,	None,	None],
[47e3,	0,		None,	None,	None],
[51e3,	-2.8,	None,	None,	None],
[71e3,	-2.0,	None,	None,	None],
[84852,	0,		None,	None,	None],
]

for i in range(1,len(levels)):
	b=levels[i-1]
	n=levels[i]
	dh=n[0]-b[0]
	dt=dh*b[1]/1000
	n[2]=b[2]+dt


for i in range(1,len(levels)):
	b=levels[i-1]
	n=levels[i]
	a=b[1]
	dh=n[0]-b[0]
	if a>0:
		t_ratio = n[2]/b[2]
		p_ratio = t_ratio ** (-g/a/R)
		rho_ratio = t_ratio ** (-g/a/R-1)
		n[3] = b[3] * rho_ratio
		n[4] = b[4] * p_ratio
	else:
		T=b[2]
		ratio = exp(-g/R/T*dh)
		n[3] = b[3] * ratio
		n[4] = b[4] * ratio
	print(n)


def get_t(h):
	for i in range(1,len(levels)):
		b=levels[i-1]
		n=levels[i]
		if h<n[0]:
			dh=h-b[0]
			dt=dh*b[1]/1000
			t=b[2]+dt
			return t

def get_p(h):
	for i in range(1,len(levels)):
		b=levels[i-1]
		n=levels[i]
		a=b[1]
		t=get_t(h)
		if h<n[0]:
			if a>0:
				t_ratio = t/b[2]
				p_ratio = t_ratio ** (-g/a/R)
				p = b[4]*p_ratio
			else:
				dh=h-b[0]
				ratio = exp(-g/R/T*dh)
				p = b[4]*ratio
			return p

def get_rho(h):
	for i in range(1,len(levels)):
		b=levels[i-1]
		n=levels[i]
		a=b[1]
		t=get_t(h)
		if h<n[0]:
			if a>0:
				t_ratio = t/b[2]
				rho_ratio = t_ratio ** (-g/a/R-1)
				rho = b[3]*rho_ratio
			else:
				dh=h-b[0]
				ratio = exp(-g/R/T*dh)
				rho = b[3]*ratio
			return rho

earth=m=model()
m.t_doc	= "temperature [K]"
m.t_fun	= lambda m:get_t(m.h)

m.tc_doc	= "temperature [C]"
m.tc_fun	= lambda m:get_t(m.h)-273.15

m.p_doc	= "pressure [Pa] [N/m2]"
m.p_fun	= lambda m:get_p(m.h)

m.rho_doc	= "density [kg/m3]"
m.rho_fun	= lambda m:get_rho(m.h)

m.c_doc	= "speed of sound [m/s]"
m.c_fun	= lambda m:331.3+0.606*m.tc
# TODO: http://hyperphysics.phy-astr.gsu.edu/hbase/Sound/souspe3.html#c1

earth.h=31333
a=earth
print(a.h, a.tc, a.t, a.p, a.rho, a.c)

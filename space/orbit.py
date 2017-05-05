from util import *
from math import *

## CONSTANTS #########################################

# gravitational constant
G = 6.673e-11

# gravitational acceleration at earth surface
g = 9.81

# stefan-boltzmann constant
sigma = 5.67e-8

GM=namespace('Gravitational constant times body mass [???]')
GM.sun = 1.327e20
GM.earth = 3.986e14
GM.moon = 4.903e12
GM.mercury = 2.094e13
GM.venus = 3.249e14
GM.mars = 4.269e13
GM.jupiter = 1.267e17
mu=GM

S=namespace('Solar irradiation constant [W/m2]')
S.earth = 1.361e3

M=namespace('Mass [kg]')
M.moon = 7.348e22
M.earth = 5.973e24
M.mars = 6.417e23

AU = 1.496e11

DAU=namespace('Distance to central body [AU]')
DAU.mercury = 0.387
DAU.venus = 0.723
DAU.earth = 1.0
DAU.mars = 1.524
DAU.jupiter = 5.204

D=namespace('Distance to central body [m]')
D.moon = 3.844e8
D.mercury = DAU.mercury * AU
D.venus = DAU.venus * AU
D.earth = AU
D.mars = DAU.mars * AU
D.jupiter = DAU.jupiter * AU

R=namespace('Radius (equatorial) [m]')
R.sun = 6.955e8
R.earth = 6.378e6
R.moon = 1.738e6
R.mars = 3.396e6

SRP=namespace('Sidereal Rotation Period [s]')
SRP.earth = to_seconds(23,56,4)
SRP.mars = to_seconds(24,37,22)

## FORMULAS #########################################

class formula:
	def __init__(self,hint,info='',**formulas):
		self.hint=hint
		self.info=info
		self.formula=formulas
	def copy(self):
		f = formula(self.hint,**self.formula)
		f.__dict__=self.__dict__.copy()
		return f
	def expand(self,x):
		f = self.formula[x]
		while '{' in f:
			f = f.replace('{','({').replace('}','})').format(**self.__dict__)
		return f
	def __getattr__(self,x):
		return eval(self.expand(x))
##
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

a_grav= formula("gravitational acceleration",
	a="{u}/{r}**2")

e_pot = formula("",
	ep="-{u}*{m}/{r}")

e_kin = formula("",
	ek="v**2*m/2")

t = formula("orbital period",
	t="2*pi*({a}**3/{u})**0.5")

ecc = formula('eccentricity',
	e='({ra}-{rp})/({ra}+{rp})')

n = formula('mean motion',
	n="({u}/{a}**3)**0.5")

# TODO conflict with equatorial radius
# R=namespace('specific gas constant [J/(kg*K)]')
# R.air = 287

if __name__=="__main__":
	a_grav.u='GM.earth'
	a_grav.r='R.earth+100e3'
	print(a_grav.a)
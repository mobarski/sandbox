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

D=namespace('Distance to central body [m]')
AU = 1.496e11
D.moon = 3.844e8
D.mercury = 0.387 * AU
D.venus = 0.723 * AU
D.earth = AU
D.mars = 1.524 * AU
D.jupiter = 5.204 * AU

R=namespace('Radius (equatorial) [m]')
R.sun = 6.955e8
R.earth = 6.378e6
R.moon = 1.738e6
R.mars = 3.396e6

SRP=namespace('Sidereal rotation period [s]')
SRP.earth = to_seconds(23,56,4)
SRP.mars = to_seconds(24,37,22)

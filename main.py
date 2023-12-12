# This is the main file where the main code is run.
import math
from column_buckling.column_buckling import column_buckling_crit_stress
from shell_buckling.shell_buckling import shell_buckling_crit_stress
from mass.mass import get_mass
from vessel_pressure.vessel_pressure import hoop_stress
from colorama import Fore, Style


L = 1.63  # m
R = 0.252  # m
t1 = 0.01  # m
t2 = 0.01  # m
V = 0.3906  # m^3
p = 100  # Pa


def compressive_stress(F, R, t1):
    return F / (math.pi * (2 * R + t1) * t1)


# Material properties
material = "Aluminium 6061-T6"
density = 2.7  # kg/m^3
yield_strength = 276 * 10**6  # Pa
tensile_strength = 310 * 10**6  # Pa
shear_strength = 207 * 10**6  # Pa
shear_modulus = 26 * 10**9  # Pa
bulk_modulus = 70 * 10**9  # Pa
Youngs_modulus = 23 * 10**9  # Pa
poisson = 0.33  # unitless

L = min(143, max(L, 2 * R))  # minimum length is 2R, maximum length is 143m

material_yield_strength = 30  # MPa

stress_applied = 40 * 10**6  # MPa

column_buckling_crit = column_buckling_crit_stress(Youngs_modulus, L, R, t1)
shell_buckling_crit = shell_buckling_crit_stress(p, R, t1, L, poisson, Youngs_modulus)

mass = get_mass(density, R, L, t1, t2)

hoop_stress = hoop_stress(p, t1, R)

fails = False

if hoop_stress > material_yield_strength:
    print("[" + Fore.RED + "-" + Style.RESET_ALL + "] Fails under hoop tension stress")
    fails = True
else:
    print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] Hoop stress succeeds.")

if stress_applied > column_buckling_crit:
    print("[" + Fore.RED + "-" + Style.RESET_ALL + "] Fails under column buckling")
    fails = True
else:
    print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] Column buckling succeeds.")

if stress_applied > shell_buckling_crit:
    print("[" + Fore.RED + "-" + Style.RESET_ALL + "] Fails under shell buckling")
    fails = True
else:
    print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] Shell buckling succeeds.")

print("Mass of the vessel is " + str(mass) + " kg")

if fails:
    print(Fore.RED + "Fuel tank calculations unsuccessful" + Style.RESET_ALL)
    exit()

print(Fore.GREEN + "Fuel tank calculations successful" + Style.RESET_ALL)

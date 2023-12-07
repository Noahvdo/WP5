# This is the main file where the main code is run.
import math
from column_buckling.functions import column_buckling_crit_stress
from shell_buckling.functions import shell_buckling_crit_stress
from mass.functions import get_mass
from vessel_pressure.functions import hoop_stress

E = 10  # GPa
poisson = 0.9  # -
L = 10  # m
R = 2  # m
t1 = 2  # m
p = 100  # Pa
density = 10  # kg/m^3

material_yield_strength = 30  # MPa

stress_applied = 40 * 10**6  # MPa

column_buckling_crit = column_buckling_crit_stress(E, L, R, t1)
shell_buckling_crit = shell_buckling_crit_stress(p, R, t1, L, poisson, E)

mass = get_mass(density, R, L, t1)

hoop_stress = hoop_stress(p, t1, R)

fails = False

if hoop_stress > material_yield_strength:
    print("[-] Fails under hoop tension stress")
    fails = True
else:
    print("[+] Hoop stress succeeds.")
if stress_applied > column_buckling_crit:
    print("[-] Fails under column buckling")
    fails = True
else:
    print("[+] Column buckling succeeds.")

if stress_applied > shell_buckling_crit:
    print("[-] Fails under shell buckling")
    fails = True
else:
    print("[+] Shell buckling succeeds.")

if fails:
    print("[-] Fuel tank calculations unsuccessful")
    exit()

print("[+] Fuel tank calculations successful")

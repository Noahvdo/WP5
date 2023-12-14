# This is the main file where the main code is run.
import math
from launch_loads.column_buckling.column_buckling import column_buckling_crit_stress
from launch_loads.shell_buckling.shell_buckling import shell_buckling_crit_stress
from launch_loads.mass.mass import get_mass, get_fuel_volume
from launch_loads.vessel_pressure.vessel_pressure import hoop_stress
from colorama import Fore, Style


L = 1.63  # m
R = 0.208  # m
L = min(1.63, max(L, 2 * R))  # minimum length is 2R, maximum length is 1.63 m
t1 = 0.01  # m
t2 = 0.01  # m
minimum_volume = 0.2024  # m^3
p = 22.8e5  # Pa

gravity = 9.81  # m / s^2
g_force = 8.5  # g
acceleration = g_force * gravity  # m/s^2
total_mass = 730.216  # kg


def compressive_stress(F, R, t1):
    area = math.pi * (2 * R - t1) * t1
    return F / area


# Material properties
material = "Aluminium 6061-T6"
density = 2.71  # kg/m^3
yield_strength = 276e6  # Pa
tensile_strength = 310e6  # Pa
shear_strength = 207e6  # Pa
shear_modulus = 26e9  # Pa
bulk_modulus = 70e9  # Pa
Youngs_modulus = 23e9  # Pa
poisson = 0.33  # unitless


# Get mass
mass = get_mass(density, R, L, t1, t2)
total_mass = mass + total_mass

# Get applied force / stress
applied_force = total_mass * acceleration  # N
applied_stress = compressive_stress(applied_force, R, t1)

# Get critical stresses
column_buckling_crit = column_buckling_crit_stress(Youngs_modulus, L, R, t1)
shell_buckling_crit = shell_buckling_crit_stress(p, R, t1, L, poisson, Youngs_modulus)

# Get hoop stress
hoop_stress = hoop_stress(p, t1, R)

# Get fuel volume
fuel_volume = get_fuel_volume(R, L, t1, t2)


def print_results():
    print("[!] Mass of the vessel is " + str(round(mass, 4)) + " kg")
    print("[!] Applied stress is " + str(round(applied_stress / 10**6, 4)) + " MPa\n")

    fails = False
    if hoop_stress > yield_strength:
        print(
            "[" + Fore.RED + "-" + Style.RESET_ALL + "] Fails under hoop tension stress"
        )
        fails = True
    else:
        print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] Hoop stress succeeds.")

    print("\tHoop stress is " + str(round(hoop_stress / 10**6, 3)) + " MPa")
    print(
        "\tMargin is "
        + str(round((yield_strength - hoop_stress) / hoop_stress * 100, 3))
        + "%\n"
    )

    if applied_stress > column_buckling_crit:
        print("[" + Fore.RED + "-" + Style.RESET_ALL + "] Fails under column buckling")
        fails = True
    else:
        print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] Column buckling succeeds. ")

    print(
        "\tCritical stress is " + str(round(column_buckling_crit / 10**6, 3)) + " MPa"
    )
    print(
        "\tMargin is "
        + str(round((column_buckling_crit - applied_stress) / applied_stress * 100, 3))
        + "%\n"
    )

    if applied_stress > shell_buckling_crit:
        print("[" + Fore.RED + "-" + Style.RESET_ALL + "] Fails under shell buckling")
        fails = True
    else:
        print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] Shell buckling succeeds.")

    print(
        "\tCritical stress is " + str(round(shell_buckling_crit / 10**6, 3)) + " MPa"
    )
    print(
        "\tMargin is "
        + str(round((shell_buckling_crit - applied_stress) / applied_stress * 100, 3))
        + "%\n"
    )

    if minimum_volume > fuel_volume:
        print("[" + Fore.RED + "-" + Style.RESET_ALL + "] Volume is too small.")
        fails = True
    else:
        print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] Volume is sufficient.")
    print("\tVolume is " + str(fuel_volume) + " m^3")
    print(
        "\tMargin is "
        + str(round((fuel_volume - minimum_volume) / minimum_volume * 100, 3))
        + "%\n"
    )
    if fails:
        print(Fore.RED + "\nFuel tank calculations unsuccessful" + Style.RESET_ALL)
        exit()

    print(Fore.GREEN + "\nFuel tank calculations successful" + Style.RESET_ALL)
    exit()


# Print results
print_results()

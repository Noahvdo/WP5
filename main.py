# This is the main file where the main code is run.
import math
from launch_loads.column_buckling.column_buckling import column_buckling_crit_stress
from launch_loads.shell_buckling.shell_buckling import shell_buckling_crit_stress
from launch_loads.mass.mass import get_mass, get_fuel_volume
from launch_loads.vessel_pressure.vessel_pressure import hoop_stress
from launch_loads.mass.mass import find_r_for_volume
from colorama import Fore, Style
import numpy as np

steps_L = 100
steps_t = 100

L_max = 1.63  # m
L_min = 0.5  # m
R = 0.001  # m
# L = min(1.63, max(L, 2 * R))  # minimum length is 2R, maximum length is 1.63 m
t = 0.01  # m
t_min = 0.001  # m
t_max = 0.03  # m


minimum_volume = 0.19286  # m^3
volume_margin = 0.05  # m^3
volume = minimum_volume + minimum_volume * volume_margin  # m^3
p = 24e5  # Pa

gravity = 9.81  # m / s^2
g_force = 8.5  # g
acceleration = g_force * gravity  # m/s^2
total_mass = 730.216  # kg


def compressive_stress(F, R, t1):
    area = math.pi * (2 * R - t1) * t1
    return F / area


# Material properties
material = "Aluminium 6061-T6"
density = 2710  # kg/m^3
yield_strength = 276e6  # Pa
tensile_strength = 310e6  # Pa
shear_strength = 207e6  # Pa
shear_modulus = 26e9  # Pa
bulk_modulus = 70e9  # Pa
Youngs_modulus = 23e9  # Pa
poisson = 0.33  # unitless

# Get applied force / stress
applied_force = total_mass * acceleration  # N


def calculate_failures(applied_force, R, t, L, p, poisson, Youngs_modulus, density):
    applied_stress = compressive_stress(applied_force, R, t)

    # Get critical stresses
    column_buckling_crit = column_buckling_crit_stress(Youngs_modulus, L, R, t)
    shell_buckling_crit = shell_buckling_crit_stress(
        p, R, t, L, poisson, Youngs_modulus
    )

    if column_buckling_crit < applied_stress:
        return False, 0, 0, 0, 0

    if shell_buckling_crit < applied_stress:
        return False, 0, 0, 0, 0

    # Get hoop stress
    hoop_stress_value = hoop_stress(p, t, R)

    if hoop_stress_value > yield_strength:
        return False, 0, 0, 0, 0

    return (
        True,
        applied_stress,
        hoop_stress_value,
        column_buckling_crit,
        shell_buckling_crit,
    )


final_R = 0
final_t = 0
final_L = 0
final_volume = 0
final_margin_volume = 0
previous_mass = 999999999
final_shell = 0
final_column = 0
final_hoop = 0
final_stress = 0


for L in np.linspace(L_min, L_max, 100):
    for t in np.linspace(t_min, t_max, 100):
        calculated_R, fuel_volume = find_r_for_volume(volume, L, t, R)
        success, stress, hoop_stresss, column, shell = calculate_failures(
            applied_force, calculated_R, t, L, p, poisson, Youngs_modulus, density
        )
        if not success:
            continue

        if fuel_volume < volume:
            continue

        margin_volume = (fuel_volume - minimum_volume) / minimum_volume
        # Get mass
        mass, tank_volume = get_mass(density, calculated_R, L, t)

        if 2 * calculated_R > L:
            continue

        if mass < previous_mass and mass > 0:
            previous_mass = mass
            final_R = calculated_R
            final_t = t
            final_L = L
            final_fuel_volume = fuel_volume
            final_margin_volume = margin_volume
            final_shell = shell
            final_column = column
            final_hoop = hoop_stresss
            final_stress = stress
            final_volume = tank_volume


def save_final_values():
    with open("final_values.txt", "w") as f:
        f.write(
            "R: "
            + str(final_R)
            + "\nt: "
            + str(final_t)
            + "\nL: "
            + str(final_L)
            + "\nVolume: "
            + str(final_volume)
            + "\nFuel Volume: "
            + str(final_fuel_volume)
            + "\nMargin Volume: "
            + str(final_margin_volume)
            + "\nMass: "
            + str(previous_mass)
            + "\nShell: "
            + str(final_shell)
            + "\nColumn: "
            + str(final_column)
            + "\nHoop: "
            + str(final_hoop)
            + "\nStress: "
            + str(final_stress)
        )


save_final_values()

# def print_results():
# print("[!] Mass of the vessel is " + str(round(mass, 4)) + " kg")
# print("[!] Applied stress is " + str(round(applied_stress / 10**6, 4)) + " MPa\n")

# fails = False
# if hoop_stress > yield_strength:
#     print(
#         "[" + Fore.RED + "-" + Style.RESET_ALL + "] Fails under hoop tension stress"
#     )
#     fails = True
# else:
#     print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] Hoop stress succeeds.")

# print("\tHoop stress is " + str(round(hoop_stress / 10**6, 3)) + " MPa")
# print(
#     "\tMargin is "
#     + str(round((yield_strength - hoop_stress) / hoop_stress * 100, 3))
#     + "%\n"
# )

# if applied_stress > column_buckling_crit:
#     print("[" + Fore.RED + "-" + Style.RESET_ALL + "] Fails under column buckling")
#     fails = True
# else:
#     print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] Column buckling succeeds. ")

# print(
#     "\tCritical stress is " + str(round(column_buckling_crit / 10**6, 3)) + " MPa"
# )
# print(
#     "\tMargin is "
#     + str(round((column_buckling_crit - applied_stress) / applied_stress * 100, 3))
#     + "%\n"
# )

# if applied_stress > shell_buckling_crit:
#     print("[" + Fore.RED + "-" + Style.RESET_ALL + "] Fails under shell buckling")
#     fails = True
# else:
#     print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] Shell buckling succeeds.")

# print(
#     "\tCritical stress is " + str(round(shell_buckling_crit / 10**6, 3)) + " MPa"
# )
# print(
#     "\tMargin is "
#     + str(round((shell_buckling_crit - applied_stress) / applied_stress * 100, 3))
#     + "%\n"
# )

# if minimum_volume > fuel_volume:
#     print("[" + Fore.RED + "-" + Style.RESET_ALL + "] Volume is too small.")
#     fails = True
# else:
#     print("[" + Fore.GREEN + "+" + Style.RESET_ALL + "] Volume is sufficient.")
# print("\tVolume is " + str(fuel_volume) + " m^3")
# print(
#     "\tMargin is "
#     + str(round((fuel_volume - minimum_volume) / minimum_volume * 100, 3))
#     + "%\n"
# )
# if fails:
#     print(Fore.RED + "\nFuel tank calculations unsuccessful" + Style.RESET_ALL)
#     exit()

# print(Fore.GREEN + "\nFuel tank calculations successful" + Style.RESET_ALL)
# exit()


# Print results
# print_results()

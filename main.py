# This is the main file where the main code is run.
import math
from launch_loads.column_buckling.column_buckling import column_buckling_crit_stress
from launch_loads.shell_buckling.shell_buckling import shell_buckling_crit_stress
from launch_loads.mass.mass import get_mass, get_fuel_volume
from launch_loads.vessel_pressure.vessel_pressure import hoop_stress
from launch_loads.mass.mass import find_r_for_volume
from materials.materials import materials
from attachments.attachments import (
    buckling_vertical,
    buckling_horizontal,
    get_mass_of_attachment_vertical,
    get_mass_of_attachment_horizontal,
)
from colorama import Fore, Style
import numpy as np


steps_L = 100
steps_t = 100

L_max = 1.63  # m
L_min = 0.5  # m
R = 0.001  # m
t_min = 0.0005  # m
t_max = 0.03  # m

safety_factor = 0.05  # unitless

# Attachments
t_attachment_vertical_min = 0.0005  # m
t_attachment_vertical_max = 0.01  # m
l_max = 0.5  # m
l_min = 0.01  # m
t_attachment_horizontal_min = 0.0005  # m
t_attachment_horizontal_max = 0.01  # m


minimum_volume = 0.19286  # m^3
volume_margin = 0.05  # m^3
volume = minimum_volume + minimum_volume * volume_margin  # m^3
p = 24e5  # Pa

gravity = 9.81  # m / s^2
g_force = 8.5  # g
acceleration = g_force * gravity  # m/s^2
total_mass = 744.216  # kg
attachment_mass = 6.7705  ### value
total_mass = total_mass


def compressive_stress(F, R, t1):
    area = math.pi * (2 * R - t1) * t1
    return F / area


# Get applied force / stress
applied_force = total_mass * acceleration  # N


def calculate_failures(
    applied_force, R, t, L, p, poisson, Youngs_modulus, yield_strength
):
    applied_stress = compressive_stress(applied_force, R, t)

    # Get critical stresses
    column_buckling_crit = column_buckling_crit_stress(Youngs_modulus, L, R, t)
    shell_buckling_crit = shell_buckling_crit_stress(
        p, R, t, L, poisson, Youngs_modulus
    )

    if column_buckling_crit < applied_stress * (safety_factor + 1):
        return False, 0, 0, 0, 0

    if shell_buckling_crit < applied_stress * (safety_factor + 1):
        return False, 0, 0, 0, 0

    # Get hoop stress
    hoop_stress_value = hoop_stress(p, t, R)

    if hoop_stress_value * (safety_factor + 1) > yield_strength:
        return False, 0, 0, 0, 0

    return (
        True,
        applied_stress,
        hoop_stress_value,
        column_buckling_crit,
        shell_buckling_crit,
    )


def round_all_values():
    global final_R
    global final_t
    global final_L
    global final_volume
    global final_margin_volume
    global previous_mass
    global final_shell
    global final_column
    global final_hoop
    global final_stress
    global final_shell_margin
    global final_column_margin
    global final_hoop_margin

    final_R = round(final_R, 4)
    final_t = round(final_t * 1000, 4)
    final_L = round(final_L, 4)
    final_volume = round(final_volume, 4)
    final_margin_volume = round(final_margin_volume, 4)
    previous_mass = round(previous_mass, 4)
    final_shell = round(final_shell, 4)
    final_column = round(final_column, 4)
    final_hoop = round(final_hoop, 4)
    final_stress = round(final_stress, 4)
    final_shell_margin = round(final_shell_margin, 4)
    final_column_margin = round(final_column_margin, 4)
    final_hoop_margin = round(final_hoop_margin, 4)


def save_final_values():
    with open("final_values_iteration.txt", "w") as f:
        f.write(
            "R: "
            + str(final_R)
            + " (m)\nt: "
            + str(final_t)
            + " (mm)\nL: "
            + str(final_L)
            + " (m)\nVolume: "
            + str(final_volume)
            + " (m^3)\nFuel Volume: "
            + str(final_fuel_volume)
            + " (m^3)\nMargin Volume: "
            + str(final_margin_volume)
            + " (%)\nMass: "
            + str(previous_mass)
            + " (kg)\nShell: "
            + str(final_shell)
            + " (Pa). Margin: "
            + str(final_shell_margin)
            + " (%)\nColumn stress: "
            + str(final_column)
            + " (Pa). Margin: "
            + str(final_column_margin)
            + " (%)\nHoop stress: "
            + str(final_hoop)
            + "(Pa). Margin: "
            + str(final_hoop_margin)
            + " (%)\nApplied stress: "
            + str(final_stress)
            + " (Pa)\nMaterial: "
            + str(best_material)
            + "\n\nAttachments:\nVertical attachment thickness: "
            + str(final_t_vertical)
            + " (m)\nHorizontal attachment thickness: "
            + str(final_t_horizontal)
            + " (m)\nHorizontal attachment length: "
            + str(final_l)
            + " (m)\nAttachment mass: "
            + str(final_attachment_mass)
            + " (kg)\nVertical attachment mass: "
            + str(final_vertical_attachment_mass)
            + " (kg)\nHorizontal attachment mass: "
            + str(final_horizontal_attachment_mass)
        )
    with open("final_values_iteration.csv", "w") as f:
        f.write(
            "R\t"
            + str(final_R)
            + "\nt\t"
            + str(final_t)
            + "\nL\t"
            + str(final_L)
            + "\nVolume\t"
            + str(final_volume)
            + "\nFuel Volume\t"
            + str(final_fuel_volume)
            + "\nMargin Volume\t"
            + str(final_margin_volume)
            + "\nMass\t"
            + str(previous_mass)
            + "\nShell\t"
            + str(final_shell)
            + "\tMargin\t"
            + str(final_shell_margin)
            + "\nColumn stress\t"
            + str(final_column)
            + "\tMargin\t"
            + str(final_column_margin)
            + "\nHoop stress\t"
            + str(final_hoop)
            + "\tMargin\t"
            + str(final_hoop_margin)
            + "\nApplied stress\t"
            + str(final_stress)
            + "\nMaterial\t"
            + str(best_material)
            + "\n\nAttachments:\nVertical attachment thickness\t"
            + str(final_t_vertical)
            + "\t(m)\nHorizontal attachment thickness\t"
            + str(final_t_horizontal)
            + "\t(m)\nHorizontal attachment length\t"
            + str(final_l)
            + "\t(m)\nAttachment mass\t"
            + str(final_attachment_mass)
            + "\t(kg)\nVertical attachment mass\t"
            + str(final_vertical_attachment_mass)
            + "\t(kg)\nHorizontal attachment mass\t"
            + str(final_horizontal_attachment_mass)
        )


Fx = 430.6  # N
Fx_margin = 0.05  # unitless
Fx = Fx * (1 + Fx_margin)
Fz = 1220  # N
Fz_margin = 0.05  # unitless
Fz = Fz * (1 + Fz_margin)


final_R = 0
final_t = 0
final_L = 0
final_volume = 0
final_fuel_volume = 0
final_margin_volume = 0
final_shell = 0
final_column = 0
final_hoop = 0
final_stress = 0
best_material = ""

final_t_vertical = 0
final_t_horizontal = 0
final_l = 0
final_attachment_mass = 0
final_vertical_attachment_mass = 0
final_horizontal_attachment_mass = 0


L_spacecraft = 1.63  # m


def iterate():
    global final_R
    global final_t
    global final_L
    global final_volume
    global final_fuel_volume
    global final_margin_volume
    global previous_mass
    global final_shell
    global final_column
    global final_hoop
    global final_stress
    global best_material
    global L_spacecraft

    previous_mass = 999999999
    for material, properties in materials.items():
        Youngs_modulus = materials[material]["E"]
        poisson = materials[material]["poisson"]
        yield_strength = materials[material]["yield_stress"]
        density = materials[material]["density"]
        for L in np.linspace(L_min, L_max, 100):
            for t in np.linspace(t_min, t_max, 100):
                calculated_R, fuel_volume = find_r_for_volume(volume, L, t, R)
                success, stress, hoop_stresss, column, shell = calculate_failures(
                    applied_force,
                    calculated_R,
                    t,
                    L,
                    p,
                    poisson,
                    Youngs_modulus,
                    yield_strength,
                )
                if not success:
                    continue

                if fuel_volume < volume:
                    continue

                # Get mass
                mass, tank_volume = get_mass(density, calculated_R, L, t)

                if 2 * calculated_R > L:
                    continue

                if mass < previous_mass and mass > 0:
                    previous_mass = mass
                    final_R = calculated_R
                    local_R = calculated_R
                    local_t = t
                    local_L = L
                    final_t = t
                    final_L = L
                    final_fuel_volume = fuel_volume
                    final_shell = shell
                    final_column = column
                    final_hoop = hoop_stresss
                    final_stress = stress
                    final_volume = tank_volume
                    best_material = material
    return [previous_mass, local_L, local_R, local_t]


def iterate_attachments():
    global final_R
    global final_L
    global L_spacecraft
    global Fz
    global Fx
    global final_shell
    global final_column
    global final_attachment_mass
    global final_horizontal_attachment_mass
    global final_vertical_attachment_mass
    global final_t_vertical
    global final_t_horizontal
    global final_l

    previous_mass_vertical = 999999999
    previous_mass_horizontal = 999999999

    mass_of_attachment_vertical = 0

    t_vertical_steps = np.linspace(
        t_attachment_vertical_min, t_attachment_vertical_max, 100
    )
    t_horizontal_steps = np.linspace(
        t_attachment_horizontal_min, t_attachment_horizontal_max, 100
    )

    for t_vertical in t_vertical_steps:
        max_buckling_vertical = buckling_vertical(Fz, final_R, t_vertical)
        if max_buckling_vertical > final_column or max_buckling_vertical > final_shell:
            continue

        if final_R / 2 <= t_vertical:
            continue

        mass_of_attachment_vertical = get_mass_of_attachment_vertical(
            L_spacecraft,
            final_L,
            final_R,
            t_vertical,
            materials["Ti6Al4V"]["density"],
        )

        if (
            mass_of_attachment_vertical < previous_mass_vertical
            and mass_of_attachment_vertical > 0
        ):
            previous_mass_vertical = mass_of_attachment_vertical
            final_t_vertical = t_vertical
            final_vertical_attachment_mass = mass_of_attachment_vertical
    for l in np.linspace(l_min, l_max, 100):
        for t_horizontal in t_horizontal_steps:
            max_buckling_horizontal = buckling_horizontal(t_horizontal, l)
            if (
                max_buckling_horizontal > final_column
                or max_buckling_horizontal > final_shell
            ):
                continue

            if l / 2 <= t_horizontal:
                continue

            mass_of_attachment_horizontal = get_mass_of_attachment_horizontal(
                materials["Ti6Al4V"]["density"], final_R, t_horizontal, l
            )

            if mass_of_attachment_horizontal < previous_mass_horizontal:
                previous_mass_horizontal = mass_of_attachment_horizontal
                final_t_horizontal = t_horizontal
                final_l = l
                final_horizontal_attachment_mass = mass_of_attachment_horizontal
    final_attachment_mass = (
        2 * final_vertical_attachment_mass + 4 * final_horizontal_attachment_mass
    )
    return [final_attachment_mass, final_t_vertical, final_t_horizontal, final_l]


# Iterate to find the best values
previous_values = [0, 0, 0, 0]
for i in range(5):
    total_mass_initial = 730.216  # kg
    # Initial iteration
    results = iterate()
    for value in results:
        round(value, 3)

    if results == previous_values:
        print("Broke the loop.")
        for i, value in enumerate(results):
            print("Now:" + str(value) + " Previous: " + str(previous_values[i]))
        break
    else:
        total_mass = total_mass - previous_values[0] + results[0]
    print("Results: " + str(results))
    print("total mass: " + str(total_mass) + " kg")
    # Iterate again with new values for mass
    applied_force = total_mass * acceleration  # N

    previous_values = results

# Iterate for the attachments
previous_values_attachments = [0, 0, 0, 0]
for i in range(5):
    results_attachments = iterate_attachments()
    total_mass = total_mass - previous_values_attachments[0] + results_attachments[0]
    applied_force = total_mass * acceleration  # N
    results = iterate()
    for value in results:
        round(value, 3)

    if results == previous_values:
        print("Broke the loop.")
        print("Results: " + str(results_attachments))
        break

    # Iterate again with new values for mass
    total_mass = total_mass - previous_values[0] + results[0]
    applied_force = total_mass * acceleration  # N

    results = iterate()
    previous_results = results
    previous_values_attachments = results_attachments


final_shell_margin = (final_shell - final_stress) / final_stress * 100
final_column_margin = (final_column - final_stress) / final_stress * 100
final_hoop_margin = (
    (materials["Ti6Al4V"]["yield_stress"] - final_hoop) / final_hoop * 100
)

final_margin_volume = (final_fuel_volume - minimum_volume) / minimum_volume * 100


print(
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
    + ". Margin: "
    + str(final_shell_margin)
    + "\nColumn stress: "
    + str(final_column)
    + ". Margin: "
    + str(final_column_margin)
    + "\nHoop stress: "
    + str(final_hoop)
    + ". Margin: "
    + str(final_hoop_margin)
    + "\nApplied stress: "
    + str(final_stress)
)
round_all_values()
save_final_values()


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

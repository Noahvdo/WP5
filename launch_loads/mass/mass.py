import math
from decimal import Decimal


def get_volume(R, L, t):
    return ((R) ** 2 - (R - t) ** 2) * math.pi * (L - 2 * R) + (
        (4 / 3) * math.pi * ((R) ** 3 - (R - t) ** 3)
    )


def get_fuel_volume(R, L, t):
    return round(
        ((R - t) ** 2) * math.pi * (L - 2 * R) + (4 / 3) * math.pi * ((R - t) ** 3), 5
    )


def find_r_for_volume(volume, L, t, R):
    found_value = False
    while not found_value:
        if 2 * R > L:
            return 0, 0
        fuel_volume = get_fuel_volume(R, L, t)
        if fuel_volume >= volume:
            found_value = True
        else:
            R += 0.001
    return R, fuel_volume


# Calculation of the mass of the vessel
def get_mass(density, R, L, t):
    volume = get_volume(R, L, t)
    return round(density * volume, 5), volume

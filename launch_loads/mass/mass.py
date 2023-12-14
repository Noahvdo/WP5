import math


def get_volume(R, L, t1, t2):
    return ((R) ** 2 - (R - t1) ** 2) * math.pi * (L - 2 * R) + (
        (4 / 3) * math.pi * ((R) ** 3 - (R - t2) ** 3)
    )


def get_fuel_volume(R, L, t1, t2):
    return round(((R) ** 2) * math.pi * (L - 2 * R) + (4 / 3) * math.pi * ((R) ** 3), 5)


# Calculation of the mass of the vessel
def get_mass(density, R, L, t1, t2):
    volume = get_volume(R, L, t1, t2)
    return round(density * volume, 5)

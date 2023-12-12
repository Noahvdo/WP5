import math


# Calculation of the mass of the vessel
def get_mass(density, R, L, t1, t2):
    return density * (
        ((R) ** 2 - (R - t1) ** 2) * math.pi * L
        + ((4 / 3) * math.pi * ((R) ** 3 - (R - t2) ** 3))
    )

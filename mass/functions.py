import math


def get_mass(density, R, L, t1):
    return (
        ((R + t1) ** 2 - R**2) * math.pi * L
        + ((4 / 3) * math.pi * ((R + t1) ** 3 - (R) ** 3))
    ) * density

import math
import numpy as np


def buckling_vertical(Fz, R, t):
    if 2 * R == t:
        return 0
    return Fz / (2 * math.pi * (t * 2 * R - t**2))


def buckling_horizontal(t, l):
    if t == l:
        return 0
    return 215.3 / (4 * t * l - 4 * t**2)


def get_mass_of_attachment_vertical(L_spacecraft, L_fueltank, R, t, density):
    return (
        ((L_spacecraft + 2 * R - L_fueltank) / 2)
        * math.pi
        * (t * 2 * R - t**2)
        * density
    )


def get_mass_of_attachment_horizontal(density, R, t, l):
    if R < l / 2:
        return 9999999999999999
    return density * (4 * t * l - 4 * t**2) * (0.815 - np.sqrt(R**2 - (l / 2) ** 2))

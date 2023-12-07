### Column critical buckling

import math


def column_buckling_crit_stress(E, L, R, t1):
    return (math.pi**2 * E * R * t1) / ((L - 2 * R) ** 2)

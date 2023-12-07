### Column critical buckling
import math


def column_buckling_crit_stress(E, L, r, t1):
    return (math.pi**2 * E * r * t1) / ((L - 2 * r)**2)



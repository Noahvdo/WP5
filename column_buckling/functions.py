### Column critical buckling
import math


def column_buckling_crit_stress(E, I, A, L):
    return (math.pi**2 * E * I) / A * L**2

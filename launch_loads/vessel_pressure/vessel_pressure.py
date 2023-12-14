import math


def hoop_stress(p, t, R):
    return p * R / t


def axial_stress(p, t, R):
    return p * R / (2 * t)

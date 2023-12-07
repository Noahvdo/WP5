import math


# Dependent on material:
# poisson and E_modulus
# Dependent on number of half-waves:
# _lambda


def calculate_Q(p, E, R, t1):
    return p * (R / t1) ** 2 / E


def calculate_k(L, R, t1, poisson):
    return math.sqrt(
        12 * L**4 * (1 - poisson**2) / (math.pi**4 * R**2 * t1**2)
    ) + 12 * L**4 * (1 - poisson**2) / (
        math.pi**4
        * R**2
        * t1**2
        * math.sqrt(
            12 * L**4 * (1 - poisson**2) / (math.pi**4 * R**2 * t1**2)
        )
    )


def shell_buckling_crit_stress(Q, k, E, t1, L, poisson):
    return (
        (1.983 - 0.983 * math.exp(-23.14 * Q))
        * k
        * math.pi**2
        * E
        * (t1 / L) ** 2
        / (12 * (1 - poisson**2))
    )

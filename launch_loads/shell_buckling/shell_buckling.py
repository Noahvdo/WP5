import math


def calculate_Q(p, E, R, t1):
    return p * (R / t1) ** 2 / E


# We calculated lambda based on the partial derivative of k with respect to lambda.
# This was: sqrt(12 * L**4 * (1 - poisson**2) / (pi**4 * R**2 * t1**2))


def calculate_k(L, R, t1, poisson):
    L = L - 2 * R
    if (R**2 * t1**2) == 0:
        return 0
    return math.sqrt(
        12 * L**4 * (1 - poisson**2) / ((math.pi**4) * R**2 * t1**2)
    ) + 12 * L**4 * (1 - poisson**2) / (
        (math.pi**4)
        * R**2
        * t1**2
        * math.sqrt(
            12 * L**4 * (1 - poisson**2) / ((math.pi**4) * R**2 * t1**2)
        )
    )


def shell_buckling_crit_stress(p, R, t1, L, poisson, E):
    L = L - 2 * R
    return (
        (1.983 - 0.983 * math.exp(-23.14 * calculate_Q(p, E, R, t1)))
        * calculate_k(L=L, R=R, t1=t1, poisson=poisson)
        * math.pi**2
        * E
        * (t1 / L) ** 2
        / (12 * (1 - poisson**2))
    )

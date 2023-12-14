import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from launch_loads.main import applied_force


Fy = 1219.98  # N
Fz = 430.56  # N
Fx = 430.56  # N

magnitude = np.sqrt(Fx**2 + Fy**2 + Fz**2)

compressive_load = applied_force
print(compressive_load)

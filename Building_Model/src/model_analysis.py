# =================================================================
# Importing Libraries
# =================================================================

import openseespy.opensees as ops
import numpy as np

from model_bare import *


# =================================================================
# Eigen Value Analysis
# =================================================================

numModes = 5
lambdas = ops.eigen(numModes)
print('The eigen values are: ', lambdas)

omega = []
frequencies = []
periods = []

for lam in lambdas:
    sqrt_lam = lam ** 0.5
    omega.append(sqrt_lam)
    frequencies.append(sqrt_lam / (2 * np.pi))
    periods.append((2 * np.pi) / sqrt_lam)

print('Initial Time Periods:')
for p in periods:
    print(f"{p:.10f}")
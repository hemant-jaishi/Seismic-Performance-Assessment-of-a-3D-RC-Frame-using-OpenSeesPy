# =================================================================
# Importing Libraries
# =================================================================

import openseespy.opensees as ops
import numpy as np


# =================================================================
# Material Definition
# =================================================================

gamma_conc = 2.5e-5           # N/mm^3 (for concrete: 25 kN/m^3 )
gamma_masonry = 2.0e-5        # N/mm^3 (for concrete: 25 kN/m^3 )
g = 9.81e3                    # mm/sec^2

unconfined_concrete_tag = 1       # unconfined concrete for cover
confined_concrete_tag = 2         # confined concrete for core
steel_tag = 3                     # reinforcement

# Nominal concrete compressive stength
fc = -20                 # Concrete compressive strength (+Tension, -Compression)
Ec = 5000 * (-fc)**0.5   # Elastic modulus of steel
Kfc = 1.2                # ratio of confined to unconfined concrete strength
Kres = 0.1               # ratio of residual/ultimate to maximum stress
lamda_u = 0.1            # ratio of unloading slope $esp2 to initial slope $Ec

# Unconfined concrete (U): compressive stress-strain properties
fc1U = fc              # (todeschini parabolic model), maximum compressive stress
eps1U = -0.002         # strain at maximum compressive stress
fc2U = Kres * fc1U     # ultimate compressive stress
eps2U = -0.02          # strain at ultimate compressive stress

# Confined concrete (C): compressive stress-strain properties
fc1C = Kfc * fc1U                             # (Mander model), maximum compressive stress
eps1C = max(eps1U * (1+5*(Kfc-1)), -0.006)    # strain at maximum compressive stress
fc2C = Kres * fc1C                            # ultimate compressive stress
eps2C = 10 * eps1C                            # strain at ultimat compressive stress

# Tensile stress-strain properties
ftC = -0.1 * fc1C    # tensile strength +tension
ftU = -0.1 * fc1U    # tensile strength +tension
Ets = ftU / 0.002    # strain-hardening ratio

# Steel parameter for Steel02
Fy_steel = 415                      # Yield strength of steel
E0_steel = 2.0e5                    # Elastic modulus of steel
Bs = 0.01                           # Strain hardening ratio
params_steel = [20, 0.925, 0.15]    # control the transition from elastic to plastic branches

# ops.uniaxialMaterial('Concrete02', matTag, fpc, eps0, fpcu, epsu, lamda, ft, Ets)
ops.uniaxialMaterial('Concrete02', unconfined_concrete_tag, fc1U, eps1U, fc2U, eps2U, lamda_u, ftU, Ets)  # unconfined concrete for cover
ops.uniaxialMaterial('Concrete02', confined_concrete_tag, fc1C, eps1C, fc2C, eps2C, lamda_u, ftC, Ets)    # confined concrete for core
ops.uniaxialMaterial('Steel02', steel_tag, Fy_steel, E0_steel, Bs, *params_steel)            
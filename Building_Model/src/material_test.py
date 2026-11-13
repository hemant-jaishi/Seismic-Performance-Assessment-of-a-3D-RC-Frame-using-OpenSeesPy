# =================================================================
# Importing Libraries
# =================================================================

import openseespy.opensees as ops
import opsvis as opsv
import numpy as np
import matplotlib.pyplot as plt

ops.wipe()
from material import *

# ===============================================================
# Steel02 Material Testing - Cyclic Stress-Strain Behaviour
# ===============================================================

# 1. Set graph appearance
plt.rcParams['font.family'] = 'Times New Roman'

# 2. Clear previous model
#ops.wipe()

# 3. Import steel material definition
# from Material import *

# 4. Initialize material testing
ops.testUniaxialMaterial(steel_tag)

# 5. Define cyclic strain history
strain_history = np.concatenate([

    #np.linspace(start_point, stop_point, number of points)

    np.linspace(0.000, 0.010, 100),   # Initial tensile loading
    np.linspace(0.010, -0.001, 200),  # Unloading and reversal

    np.linspace(-0.001, 0.020, 200),  # Increased tensile loading
    np.linspace(0.020, -0.001, 200),  # Unloading and reversal

    np.linspace(-0.001, 0.030, 300),  # Increased tensile loading
    np.linspace(0.030, -0.001, 300),  # Unloading and reversal

    np.linspace(-0.001, 0.040, 400),  # Increased tensile loading
    np.linspace(0.040, -0.001, 400),  # Unloading and reversal

    np.linspace(-0.001, 0.060, 400)   # Final tensile loading

])

# 6. Create empty lists to store results
strain_steel = []
stress_steel = []

# 7. Apply strain and record corresponding stress
for eps in strain_history:
    ops.setStrain(eps)
    stress = ops.getStress()
    strain = ops.getStrain()
    stress_steel.append(stress)
    strain_steel.append(strain)

# 8. Plot stress-strain relationship
plt.figure(figsize=(8, 5))

plt.plot(strain_steel, stress_steel, color='green', linewidth=1.5, label='Steel02 Material')

# Graph labels and title
plt.title('Cyclic Stress-Strain Behaviour of Steel02')
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')

# Graph formatting
plt.axhline(y=0, color='black', linewidth=0.7)
plt.axvline(x=0, color='black', linewidth=0.7)
plt.grid(True, alpha=0.5)
plt.tick_params(direction='in', top=True, right=True)
plt.xlim(-0.01, 0.06)
plt.legend()
plt.tight_layout()
plt.show()

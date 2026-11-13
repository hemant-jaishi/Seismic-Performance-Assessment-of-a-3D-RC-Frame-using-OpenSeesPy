# =================================================================
# Importing Libraries
# =================================================================

import openseespy.opensees as ops
import matplotlib.pyplot as plt
import opsvis as opsv

from model_analysis import *


# =================================================================
# Gravity Analysis
# =================================================================

# Clear previous analysis objects (retain the structural model)
ops.wipeAnalysis()

if rigidDiaphragm == 1:
    ops.constraints('Transformation')
else:
    ops.constraints('Plain')

ops.numberer('RCM')
ops.system('BandGen')
ops.test('NormDispIncr', 1e-8, 10)
ops.algorithm('Newton')
ops.integrator('LoadControl', 1)
ops.analysis('Static')

# Perform gravity analysis
ok = ops.analyze(1)

if ok == 0:
    print("\nGravity analysis successful")

    # Hold existing gravity loads constant
    ops.loadConst('-time', 0.0)

else:
    print("Gravity analysis failed")


# =================================================================
# Plotting Mode Shapes and Deformed Shape
# =================================================================

def ModeShapesPlot():

    # Plot gravity deformed shape
    opsv.plot_defo()
    plt.title("Gravity Deformed Shape")

    # Plot mode shapes
    for i in range(1, numModes + 1):
        opsv.plot_mode_shape(i)
        plt.title(f"Mode {i}")

    plt.show()

ModeShapesPlot()

print("--------------------------------")
print("Gravity Analysis Completed.")
print("--------------------------------")
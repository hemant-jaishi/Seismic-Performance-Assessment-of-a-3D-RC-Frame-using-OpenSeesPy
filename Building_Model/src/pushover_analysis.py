# ==================================================================
# Importing Libraries
# ==================================================================

import openseespy.opensees as ops
import matplotlib.pyplot as plt
import csv
import os
from pathlib import Path
from gravity_analysis import *


# ==========================================================
# NONLINEAR STATIC PUSHOVER ANALYSIS - IN X DIRECTION
# ==========================================================


# ----------------------------------------------------------
# 1. OUTPUT DIRECTORY
# ----------------------------------------------------------
os.chdir(Path(__file__).resolve().parent)
output_dir = "../../Output/"
os.makedirs(output_dir, exist_ok=True)

# ----------------------------------------------------------
# 2. PUSHOVER PARAMETERS
# ----------------------------------------------------------

push_direction = 2         # 1 = X direction, 2 = Y direction

control_node = 3           # Roof diaphragm master node
refLoad = 1000.0           # Reference lateral load (N)

building_height = 6000.0   # Building height (mm)
target_drift = 0.04        # Target drift ratio = 4%

maxDisp = target_drift * building_height

dU = 0.05                   # Displacement increment (mm)

# Unique tags for lateral load pattern
timeSeriesTag = 11
patternTag = 11

# ----------------------------------------------------------
# 3. SELECT PUSHOVER DIRECTION
# ----------------------------------------------------------

if push_direction == 1:
    control_DOF = 1
    direction_name = "X"
elif push_direction == 2:
    control_DOF = 2
    direction_name = "Y"
else:
    raise ValueError("Invalid pushover direction. Choose 1 or 2.")

print(f"Starting Pushover Analysis in {direction_name} Direction")

# ----------------------------------------------------------
# 4. HOLD GRAVITY LOADS CONSTANT
# ----------------------------------------------------------

# Assumes gravity analysis has completed successfully.
ops.loadConst('-time', 0.0)

# Clear previous analysis objects without deleting the model.
ops.wipeAnalysis()

# ----------------------------------------------------------
# 5. DEFINE LATERAL LOAD PATTERN
# ----------------------------------------------------------

ops.timeSeries('Linear', timeSeriesTag)
ops.pattern('Plain', patternTag, timeSeriesTag)

# Equal reference force at each master node.
# This is an equal-force distribution, not a triangular distribution.

for tag in master_nodes:
    if push_direction == 1:
        ops.load(tag, refLoad, 0.0, 0.0, 0.0, 0.0, 0.0)
    else:
        ops.load(tag, 0.0, refLoad, 0.0, 0.0, 0.0, 0.0)

# ----------------------------------------------------------
# 6. DEFINE ANALYSIS CONFIGURATION
# ----------------------------------------------------------

if rigidDiaphragm == 1:
    ops.constraints('Transformation')
else:
    ops.constraints('Plain')

ops.numberer('RCM')
ops.system('BandGen')
ops.test('NormDispIncr', 1.0e-6, 1000)
ops.algorithm('Newton')

#integrator('DisplacementControl', nodeTag, dof, incr, numIter=1, dUmin=incr, dUmax=incr)
ops.integrator('DisplacementControl', control_node, control_DOF, dU, 1, dU, dU)

ops.analysis('Static')

# ----------------------------------------------------------
# 7. INITIALIZE RESULT ARRAYS
# ----------------------------------------------------------

controlNode_disp = []
base_shear = []
drift = []

currentDisp = 0.0
ok = 0
step = 0

# ----------------------------------------------------------
# 8. PUSHOVER ANALYSIS
# ----------------------------------------------------------

while ok == 0 and abs(currentDisp) < maxDisp:
    step += 1
    # Try Newton-Raphson first
    ok = ops.analyze(1)

    # ------------------------------------------------------
    # Try alternative algorithms if Newton fails
    # ------------------------------------------------------

    if ok != 0:
        print(f"Convergence issue at step {step}. Trying alternatives...")
        algorithms = [
            ('ModifiedNewton', ['-initial']),
            ('NewtonLineSearch', []),
            ('KrylovNewton', []),
            ('BFGS', [])
        ]

        for alg, args in algorithms:
            ops.algorithm(alg, *args)
            if ops.analyze(1) == 0:
                print(f"Converged using {alg} at step {step}")
                ok = 0
                break

        # Restore Newton algorithm
        ops.algorithm('Newton')

    # ------------------------------------------------------
    # Stop if all algorithms fail
    # ------------------------------------------------------
    if ok != 0:
        print(f"Pushover analysis failed at step {step}.")
        break

    # ------------------------------------------------------
    # Record control node displacement
    # ------------------------------------------------------
    currentDisp = ops.nodeDisp(control_node, control_DOF)
    controlNode_disp.append(currentDisp)

    # ------------------------------------------------------
    # Calculate base shear from support reactions
    # ------------------------------------------------------
    ops.reactions()
    bShear = 0.0

    for node in floor_1_nodes:
        reaction = ops.nodeReaction(node, control_DOF)
        bShear += reaction

    # Convert N to kN
    bShear = abs(bShear) / 1.0e3
    base_shear.append(bShear)

    # ------------------------------------------------------
    # Calculate storey-height-based drift ratio
    # ------------------------------------------------------
    current_drift = (abs(currentDisp) / building_height) * 100
    drift.append(current_drift)

    # ------------------------------------------------------
    # Display progress
    # ------------------------------------------------------
    if step % 20 == 0:
        print(
            f"Step: {step} | "
            f"Displacement: {currentDisp:.3f} mm | "
            f"Base Shear: {bShear:.3f} kN | "
            f"Drift: {current_drift:.3f} %"
        )

# ----------------------------------------------------------
# 9. ANALYSIS SUMMARY
# ----------------------------------------------------------

if len(base_shear) == 0:
    raise RuntimeError("No converged pushover steps. " "Check model, loading and convergence settings.")

max_base_shear = max(base_shear)
max_index = base_shear.index(max_base_shear)
disp_at_max_base_shear = controlNode_disp[max_index]
drift_at_max_base_shear = drift[max_index]

print("\n================================")
print("PUSHOVER ANALYSIS RESULTS")
print("================================")

print(f"Pushover Direction: {direction_name}")
print(f"Maximum Base Shear: {max_base_shear:.2f} kN")
print( f"Displacement at Maximum Base Shear: " f"{disp_at_max_base_shear:.2f} mm")
print(f"Drift at Maximum Base Shear: " f"{drift_at_max_base_shear:.3f} %")
print(f"Total Converged Steps: {len(base_shear)}")

if ok != 0:
    print("WARNING: Analysis terminated before reaching target displacement.")
else:
    print("Target displacement reached.")

# ----------------------------------------------------------
# 10. EXPORT RESULTS TO CSV
# ----------------------------------------------------------

csv_filename = os.path.join(output_dir, f"pushover_results_{direction_name}.csv")

with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        "Roof Displacement (mm)",
        "Drift (%)",
        "Base Shear (kN)"
    ])

    for disp, d, bs in zip(controlNode_disp, drift, base_shear):
        writer.writerow([disp, d, bs])

print(f"\nResults saved to: {csv_filename}")

# ----------------------------------------------------------
# 11. PLOT PUSHOVER CAPACITY CURVE
# ----------------------------------------------------------

plt.figure(figsize=(8, 6))
plt.plot(drift, base_shear, linewidth=1.5, label=f"Pushover - {direction_name} Direction")
plt.scatter(drift_at_max_base_shear, max_base_shear, marker='o', label='Maximum Base Shear')
plt.title(f"Pushover Capacity Curve ({direction_name} Direction)")
plt.xlabel("Roof Drift (%)")
plt.ylabel("Base Shear (kN)")
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.tick_params(direction='in', top=True, right=True)
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()
# ==================================================================
# Importing Libraries
# ==================================================================

import matplotlib
matplotlib.use("Agg")                 # no plot windows, so the run never stops and waits

import openseespy.opensees as ops
import numpy as np, matplotlib.pyplot as plt
import os
import sys
import csv
import math
import opsvis as opsv
from pathlib import Path

# Work from the folder that contains this file (src), same as in the notebook
os.chdir(Path(__file__).resolve().parent)

from gravity_analysis import *


# ==================================================================
# Incremental Dynamic Analysis (IDA)
# ==================================================================
# One run = one ground motion at one PGA level (fresh model every run)
#
#   python IDA.py <RSN> <direction> <PGA>      e.g.  python IDA.py 334 2 0.5
#
# Without inputs it uses the default values written in Section 2.
# run_ida.py calls this file again and again for every RSN and PGA level.


# ------------------------------------------------------------------
# 1. OUTPUT DIRECTORY
# ------------------------------------------------------------------
output_dir = "../../Output/"
os.makedirs(output_dir, exist_ok=True)
GM_DIR = "../../GM_data/D/"


# ------------------------------------------------------------------
# 2. GROUND MOTION SELECTION
# ------------------------------------------------------------------

GM_RSN = int(sys.argv[1]) if len(sys.argv) > 1 else 334                # Ground motion RSN
direction = int(sys.argv[2]) if len(sys.argv) > 2 else 2               # 1 = Earthquake in X-direction, 2 = Earthquake in Y-direction
target_PGA = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5          # Target PGA in g

original_pga_data = {
    5676: 0.36297,
    5259: 0.34798,
    4199: 0.29655,
    3282: 0.32222,
    2510: 0.33066,
    2476: 0.36627,
    334:  0.28209
}

if GM_RSN not in original_pga_data:
    raise ValueError(f"Original PGA not available for RSN {GM_RSN}.")

if direction not in (1, 2):
    raise ValueError("Direction must be 1 (Earthquake in X-direction) or 2 (Earthquake in Y-direction).")

Original_PGA = original_pga_data[GM_RSN]

GM_inputfile = os.path.join(GM_DIR, f"RSN_{GM_RSN}.txt")

if not os.path.isfile(GM_inputfile):
    raise FileNotFoundError(f"Ground motion file not found: {GM_inputfile}")

print("=" * 65)
print("NONLINEAR TIME HISTORY ANALYSIS")
print("=" * 65)

print(f"Ground Motion: RSN {GM_RSN}")
print(f"Direction: {'X' if direction == 1 else 'Y'}")
print(f"Target PGA: {target_PGA:.3f} g")


# ------------------------------------------------------------------
# 3. READING AND PROCESSING GROUND MOTION
# ------------------------------------------------------------------

load_factors = []
dt = None

# Read GM file
with open(GM_inputfile, "r") as file:
    lines = file.readlines()

# Extract time step
for line in lines:
    if 'Time Step' in line:
        dt = float(line.strip().split(":")[1].split()[0])
        break

if dt is None or dt <= 0:
    raise ValueError("Invalid or missing ground motion time step.")

# Locate the beginning of acceleration data
data_start_index = next((i+1 for i, line in enumerate(lines) if "Time(sec)" in line), None)

if data_start_index is None:
    raise ValueError("Ground motion data header not found.")

for line in lines[data_start_index:]:
    if not line.strip():
        continue
    parts = line.strip().split()
    if len(parts) >= 2:
        load_factors.append(float(parts[1]))

if len(load_factors) < 2:
    raise ValueError('Insufficient ground motion data.')

# Duration between the first and last acceleration point
tFinal = dt * (len(load_factors) - 1)

# Extra time after the ground motion ends (free vibration, zero ground motion)
free_vibration_time = 5.0
tAnalysis = tFinal + free_vibration_time

print("-" * 65)
print(f"Original PGA       : {Original_PGA:.5f} g")
print(f"Time Step          : {dt:.5f} sec")
print(f"Number of Points   : {len(load_factors)}")
print(f"Ground Motion Time : {tFinal:.5f} sec")
print("-" * 65)


# ------------------------------------------------------------------
# 4. GRAVITY ANALYSIS
# ------------------------------------------------------------------

# Structural model and gravity analysis are imported from gravity_analysis.py
# Every run starts a new Python process, so the model is always fresh


# ------------------------------------------------------------------
# 5. EIGENVALUE ANALYSIS
# ------------------------------------------------------------------

def EigenValues(nmodes):
    lambdas = ops.eigen(nmodes)

    omega = []
    frequencies = []
    periods = []

    for lam in lambdas:
        sqrt_lam = lam ** 0.5
        omega.append(sqrt_lam)
        frequencies.append(sqrt_lam / (2 * np.pi))
        periods.append((2 * np.pi) / sqrt_lam)

    return periods


# ------------------------------------------------------------------
# Sections 6 to 14 are written inside one function
# ------------------------------------------------------------------

def run_nltha(target_PGA):

    # ------------------------------------------------------------------
    # 6. RAYLEIGH DAMPING (D = αM*M + βKcurr*Kcurrent + βKcomm*KlastCommit + βKinit*Kinitial)
    # ------------------------------------------------------------------

    damping_ratio = 0.05

    # Damping Contribution Switches
    MpropSwtich = 1.0
    KcurrSwitch = 0.0
    KcommSwitch = 1.0
    KinitSwitch = 0.0

    # Modes selected for Rayleigh Damping
    # X-direction: modes 1 and 4 (X-modes), Y-direction: modes 2 and 5 (Y-modes)
    # Mode 3 is the torsional mode, so it is not used
    if direction == 1:
        nEigenI = 1   # mode i
        nEigenJ = 4   # mode j
    else:
        nEigenI = 2   # mode i
        nEigenJ = 5   # mode j

    # Eigenvalue analysis
    lambdaN = ops.eigen(nEigenJ)

    lambdaI = lambdaN[nEigenI - 1]
    lambdaJ = lambdaN[nEigenJ - 1]

    # Natural circular frequencies
    omegaI = lambdaI ** 0.5
    omegaJ = lambdaJ ** 0.5

    # Rayleigh damping coefficients
    alphaM = (MpropSwtich * damping_ratio * (2.0 * omegaI * omegaJ) / (omegaI + omegaJ))
    betaKcurr = (KcurrSwitch * 2.0 * damping_ratio / (omegaI + omegaJ))
    betaKcomm = (KcommSwitch * 2.0 * damping_ratio / (omegaI + omegaJ))
    betaKinit = (KinitSwitch * 2.0 * damping_ratio / (omegaI + omegaJ))

    print("\nRayleigh Damping Coefficients:")
    print(f"alphaM    : {alphaM:.6f}")
    print(f"betaKcurr : {betaKcurr:.6f}")
    print(f"betaKcomm : {betaKcomm:.6f}")
    print(f"betaKinit : {betaKinit:.6f}\n")


    # ------------------------------------------------------------------
    # 7. TRANSIENT ANALYSIS CONFIGURATION
    # ------------------------------------------------------------------

    # Ground motion scaling factor
    # Assumes acceleration values in input file are in g
    scaling_factor = (target_PGA * 9810) / Original_PGA

    print(f"Target PGA     : {target_PGA:.3f} g")
    print(f"Scaling Factor : {scaling_factor:.5f}")

    ops.wipeAnalysis()

    # Rayleigh Damping
    ops.rayleigh(alphaM, betaKcurr, betaKinit, betaKcomm)

    # Analysis time step (NBC 105:2020: <= record dt, <= T1/100, <= 0.01 s)
    T1 = (2 * np.pi) / omegaI       # fundamental period in shaking direction
    max_dt = min(dt, T1/100, 0.01)
    n_sub = math.ceil(dt / max_dt)
    dt_analysis = dt / n_sub
    print(f"Analysis Time Step : {dt_analysis:.5f} sec")

    # Ground motion time series
    ops.timeSeries('Path', 200, '-dt', dt, '-values', *load_factors, '-factor', scaling_factor)

    # Uniform earthquake excitation
    ops.pattern('UniformExcitation', 200, direction, '-accel', 200)

    # Analysis configuration
    ops.constraints('Transformation')
    ops.test('EnergyIncr', 5.0e-4, 50)
    ops.algorithm('Newton')
    ops.numberer('RCM')
    ops.system('BandGen')
    ops.integrator('Newmark', 0.5, 0.25)
    ops.analysis('Transient')


    # ------------------------------------------------------------------
    # 8. RESPONSE MONITORING PARAMETERS
    # ------------------------------------------------------------------

    Control_node = 3
    NBayZ = 2
    storey_height = 3000.0      # Storey height in mm

    nodes_for_IDR = [101, 201, 301]

    if len(nodes_for_IDR) < NBayZ + 1:
        raise ValueError("IDR node list must contain NBayZ + 1 nodes.")

    # Collapse criteria
    collapse_drift = 0.05      # 5% interstorey drift = collapse
    collapsed = False

    # Response history list
    time = []
    baseshear = []
    control_node_disp = []

    # One drift history list for each storey
    drift_all_floors = [[] for _ in range(NBayZ)]


    # ------------------------------------------------------------------
    # 9. NON-LINEAR TIME HISTORY ANALYSIS (NLTHA) LOOP
    # ------------------------------------------------------------------

    def analyze_step():

        """
        Attempts one transient analysis step using different solution algorithms if convergence is not achieved.
        """
        algorithms = [
             'Newton',
             'ModifiedNewton',
             'Broyden',
             'NewtonLineSearch',
             'KrylovNewton'
             ]
        for algorithm in algorithms:
            # Use original convergence test for Newton
            if algorithm == 'Newton':
                ops.test('EnergyIncr', 5.0e-4, 50)
            else:
                ops.test('NormDispIncr', 5.0e-4, 100, 0)

            ops.algorithm(algorithm)
            ok = ops.analyze(1, dt_analysis)

            if ok == 0:
                # Restore the default analysis settings
                ops.algorithm('Newton')
                ops.test('EnergyIncr', 5.0e-4, 50)
                return 0

        # Last try: divide the step into 10 smaller steps
        ops.test('NormDispIncr', 5.0e-4, 100, 0)
        ops.algorithm('ModifiedNewton')
        ok = ops.analyze(10, dt_analysis/10)

        # Restore the default settings
        ops.algorithm('Newton')
        ops.test('EnergyIncr', 5.0e-4, 50)

        return ok

    # Initial analysis time
    tCurrent = ops.getTime()

    ok = 0

    print("\nStarting Transient Analysis...")
    print("-" * 65)

    while tCurrent < tAnalysis - 1.0e-10:
        # Perform one analysis step
        ok = analyze_step()

        # Stop if convergence is not achieved
        if ok != 0:
            print(f"Analysis failed at time : {tCurrent:.5f} sec")
            break

        # Update analysis time
        tCurrent = ops.getTime()

        # -------------------------------------------------------
        # Record Base Shear
        # -------------------------------------------------------
        ops.reactions()
        baserec = sum(ops.nodeReaction(node, direction) for node in floor_1_nodes)
        baseshear.append(baserec / 1.0e3)

        # -------------------------------------------------------
        # Record Control Node Displacement
        # -------------------------------------------------------
        displacement = ops.nodeDisp(Control_node, direction)
        control_node_disp.append(displacement)

        # -------------------------------------------------------
        # Calculate Inter-Storey Drift Ratio
        # -------------------------------------------------------
        for floor in range(NBayZ):
            base_node = nodes_for_IDR[floor]
            top_node = nodes_for_IDR[floor + 1]
            base_disp = ops.nodeDisp(base_node, direction)
            top_disp = ops.nodeDisp(top_node, direction)
            drift = abs(top_disp - base_disp) / storey_height
            drift_all_floors[floor].append(drift)

        # Store current time
        time.append(tCurrent)

        # -------------------------------------------------------
        # Collapse check: drift larger than collapse drift
        # -------------------------------------------------------
        if max(d[-1] for d in drift_all_floors) > collapse_drift:
            collapsed = True
            print(f"Drift exceeded {collapse_drift * 100:.1f} % at time = {tCurrent:.5f} sec")
            break


    # ------------------------------------------------------------------
    # 10. ANALYSIS COMPLETION CHECK
    # ------------------------------------------------------------------

    # Analysis not converged = collapse
    if ok != 0 or not time:
        collapsed = True

    print("-" * 65)
    print(f"Transient Analysis Ended at: {tCurrent:.5f} sec   |   Collapsed: {collapsed}")


    # ------------------------------------------------------------------
    # 11. POST-EARTHQUAKE EIGENVALUE ANALYSIS
    # ------------------------------------------------------------------

    if collapsed:
        Final_TimePeriods = [0.0, 0.0, 0.0]         # not calculated after collapse
    else:
        Final_TimePeriods = EigenValues(3)

    print("\nFinal Time Periods:")

    for i, period in enumerate(Final_TimePeriods):
        print(f"Mode {i + 1}: {period:.5f} sec")


    # ------------------------------------------------------------------
    # 12. MAXIMUM STRUCTURAL RESPONSE
    # ------------------------------------------------------------------

    # Maximum absolute base shear
    max_base_shear = max(np.abs(baseshear)) if baseshear else 0.0

    print(f"\nMaximum Induced Base Shear = " f"{max_base_shear:.4f} kN")

    # Maximum absolute control node displacement
    max_control_node_disp = max(np.abs(control_node_disp)) if control_node_disp else 0.0

    print(f"Maximum Top Displacement = " f"{max_control_node_disp:.4f} mm")


    # ------------------------------------------------------------------
    # 13. MAXIMUM INTER-STOREY DRIFT RATIO (MIDR)
    # ------------------------------------------------------------------

    # Maximum drift of each floor
    MIDRs = [max(drifts) if drifts else 0.0 for drifts in drift_all_floors]

    # Individual floor MIDRs
    MIDR_1st_floor = MIDRs[0]
    MIDR_2nd_floor = MIDRs[1]

    print("\nMaximum Interstory Drift Ratios:")

    for i, midr in enumerate(MIDRs):
        print(f"Floor {i + 1}: {midr * 100:.5f} %")

    # Maximum MIDR of the building
    MIDRall = max(MIDRs)

    print(f"\nMaximum Building MIDR = " f"{MIDRall * 100:.5f} %")


    # ------------------------------------------------------------------
    # 14. SAVE RESULT TO CSV
    # ------------------------------------------------------------------

    csv_filename = os.path.join(output_dir, f"IDA_Results_{direction}.csv")

    # Check if file exists, if not write the header
    file_exists = os.path.isfile(csv_filename)

    with open(csv_filename, 'a', newline='') as file:
        writer = csv.writer(file)

        # Write column headers only once
        if not file_exists:
            writer.writerow([
                'GM_RSN',
                'PGA (g)',
                'Maximum Base Shear (kN)',
                'Maximum Top Displacement (mm)',
                'Mode 1 Period (sec)',
                'Mode 2 Period (sec)',
                'Mode 3 Period (sec)',
                'MIDR 1st Floor (%)',
                'MIDR 2nd Floor (%)',
                'MIDR ALL (%)',
                'Collapsed'
            ])

        # Write current analysis results
        writer.writerow([
            GM_RSN,
            target_PGA,
            f"{max_base_shear:.5f}",
            f"{max_control_node_disp:.5f}", *[f"{period:.5f}" for period in Final_TimePeriods],
            f"{MIDR_1st_floor * 100:.5f}",
            f"{MIDR_2nd_floor * 100:.5f}",
            f"{MIDRall * 100:.5f}",
            collapsed
        ])

    print("\nResults successfully saved to:")
    print(csv_filename)

    return collapsed


# ------------------------------------------------------------------
# 15. RUN ANALYSIS
# ------------------------------------------------------------------

collapsed = run_nltha(target_PGA)

print("=" * 65)
print(f"FINISHED: RSN {GM_RSN} | PGA {target_PGA:.3f} g | Collapsed: {collapsed}")
print("=" * 65)

# Exit code 2 = collapsed (run_ida.py uses it to go to the next ground motion)
sys.exit(2 if collapsed else 0)
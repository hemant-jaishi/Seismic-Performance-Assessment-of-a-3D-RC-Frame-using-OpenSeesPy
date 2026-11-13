import os
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Times New Roman'
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)
output_dir = "../../Plots/"
os.makedirs(output_dir, exist_ok=True)
output_filename = os.path.join(output_dir, "Pushover_curves.png")

files = [
    "../../Output/pushover_results_X.csv",
    "../../Output/pushover_results_Y.csv"
]

plt.figure(figsize=(8,6))

for file in files:
    df = pd.read_csv(file)
    if file.endswith('pushover_results_X.csv'):
        label = 'Pushover in X-direction'
        text_shift = (40, -50)
    else:
        label = 'Pushover in Y-direction' 
        text_shift = (-90, -80)
    x = df["Drift (%)"]
    y = df["Base Shear (kN)"]
    line, = plt.plot(x, y, label=label)

    # Find the maximum base shear, its drift and its displacement
    max_index = y.idxmax()
    max_shear = y[max_index]
    max_drift = x[max_index]
    max_disp = df["Roof Displacement (mm)"][max_index]

    # Mark the maximum point and write its values on the graph
    plt.plot(max_drift, max_shear, 'o', color=line.get_color())
    plt.annotate(f"Max = {max_shear:.1f} kN\nat drift = {max_drift:.2f} %\nat displacement = {max_disp:.1f} mm", xy=(max_drift, max_shear), xytext=text_shift, textcoords='offset points', color=line.get_color(), arrowprops=dict(arrowstyle='->', color=line.get_color()))

plt.xlabel("Roof Drift (%)")
plt.ylabel("Base Shear (kN)")
plt.title("Pushover Curves")
plt.legend(loc='lower right')
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.tick_params(direction='in', top=True, right=True)
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig(output_filename, dpi=1200)
plt.show()

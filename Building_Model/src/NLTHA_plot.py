import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path
plt.rcParams['font.family'] = 'Times New Roman'


# ------------------------------------------------------------
# 1. FILE PATHS AND OUTPUT DIRECTORY
# ------------------------------------------------------------
os.chdir(Path(__file__).resolve().parent)
output_dir_1 = "../../Output/"
output_dir = "../../Plots/"
os.makedirs(output_dir, exist_ok=True)

files = [
    "../../Output/NLTHA_Results_1.csv",
    "../../Output/NLTHA_Results_2.csv"
]


# ------------------------------------------------------------
# 2. READ NLTHA RESULT FILES
# ------------------------------------------------------------

data = {}
for file in files:
    df = pd.read_csv(file)
    if file.endswith("_1.csv"):
        label = "NLTHA in X-direction"
    else:
        label = "NLTHA in Y-direction"
    data[label] = df

drift_columns = ["MIDR 1st Floor (%)", "MIDR 2nd Floor (%)"]
floor_height = [3000, 6000]

# ------------------------------------------------------------
# 3. GENERATE SUMMARY TABLE
# ------------------------------------------------------------

# Select required columns
columns = ["GM_RSN", "Maximum Base Shear (kN)", "Maximum Top Displacement (mm)", "MIDR ALL (%)"]

# Combine X and Y results using ground motion ID
table = pd.merge(data["NLTHA in X-direction"][columns], data["NLTHA in Y-direction"][columns], on="GM_RSN", suffixes=("_X", "_Y"))

# Calculate mean and maximum values
mean_row = table.mean(numeric_only=True)
max_row = table.max(numeric_only=True)

# Add summary rows
table.loc[len(table)] = mean_row
table.loc[len(table)] = max_row

# Label summary rows
table["GM_RSN"] = table["GM_RSN"].astype(str)
table.loc[len(table) - 2, "GM_RSN"] = "Mean"
table.loc[len(table) - 1, "GM_RSN"] = "Maximum"

# Round values
table = table.round(3)

# Display summary table
print("\nNLTHA SUMMARY TABLE")
print(table.to_string(index=False))

# Save summary table
table.to_csv(os.path.join(output_dir_1, "NLTHA_Summary.csv"), index=False)


# ------------------------------------------------------------
# 4. PLOT NLTHA RESULTS
# ------------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharex=True, sharey=True)

for ax, (label, df) in zip(axes, data.items()):
    # Plot individual ground motions
    for _, row in df.iterrows():
        drift = [row[col] for col in drift_columns]
        ax.plot(drift, floor_height, marker="o", alpha=0.5, linewidth=1, label=f"RSN {row['GM_RSN']}")
    # Calculate mean drift at each floor
    mean_drift = df[drift_columns].mean()
    ax.plot(mean_drift, floor_height, color="black", marker="s", linewidth=1.5, label="Mean")

    ax.axvline(1.0, color="brown", linestyle="--", linewidth=1)
    ax.text(1.0, floor_height[-1], " IO", color="brown", va="top")

    # Formatting
    ax.set_title(label)
    ax.set_xlabel("Maximum Interstory Drift Ratio (%)")
    ax.set_ylabel("Floor Height (mm)")
    ax.set_yticks(floor_height)
    ax.set_xlim(left=0)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(fontsize=7)

axes[0].set_ylabel("Floor Height (mm)")
axes[1].legend(fontsize=7)

fig.suptitle("Maximum Interstory Drift Profile")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "MIDR_Profile.png"), dpi=1200, bbox_inches="tight")
plt.savefig(os.path.join(output_dir, "MIDR_Profile.pdf"), bbox_inches="tight")
plt.show()

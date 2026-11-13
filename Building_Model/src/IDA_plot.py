import pandas as pd
import matplotlib.pyplot as plt
import os 
from pathlib import Path
plt.rcParams['font.family'] = 'Times New Roman'


# -------------------------------------------------------
# FILE PATH & DIRECTORY
# -------------------------------------------------------
os.chdir(Path(__file__).resolve().parent)
output_dir = "../../Plots/"
os.makedirs(output_dir, exist_ok=True)
output_filename = os.path.join(output_dir, "IDA_curves.png")

files = [
    "../../Output/IDA_Results_1.csv",
    "../../Output/IDA_Results_2.csv"
]


# -------------------------------------------------------
# READ IDA FILES 
# -------------------------------------------------------

data = {}
for file in files:
    df = pd.read_csv(file)
    if file.endswith("_1.csv"):
        label = "X-direction"
    elif file.endswith("_2.csv"):
        label = "Y-direction"
    else:
        raise ValueError(f"Unknown result file : {file}")
    data[label] = df
    #print(df.head())
    print(df.columns.tolist())
    #print(df["GM_RSN"]).unique()
    #print(df["Collapsed"].value_counts())

style = {
        "X-direction": {"color": "blue"},
        "Y-direction": {"color": "tab:orange"}
    }


# -------------------------------------------------------
# PLOT IDA RESULTS
# -------------------------------------------------------

fig, ax = plt.subplots(figsize=(10,7))
for label, df in data.items():
    # one thin line per record
    for rsn, group in df.groupby("GM_RSN"):
        group = group.sort_values("PGA (g)")
        x = group["PGA (g)"]
        y = group["MIDR ALL (%)"]
        ax.plot(x, y, color=style[label]["color"], linewidth=1, alpha=0.5)

    # median curve (once per direction)
    median = df.groupby("PGA (g)")["MIDR ALL (%)"].median()
    x1 = median.index
    y1 = median.values
    ax.plot(x1, y1, color=style[label]["color"], linestyle='--', linewidth=2.5, label=f"{label} median")

    collapsed = df[df["Collapsed"] == True]
    ax.scatter(collapsed["PGA (g)"], collapsed["MIDR ALL (%)"], marker="x", color='red', s=40, label="Collapsed" if label == "X-direction" else None)

limits = {1: "IO", 2: "LS", 4: "CP"}
for y_lim, name in limits.items():
    ax.axhline(y_lim, color="brown", linestyle="--")
    ax.text(0.99, y_lim + 0.05, name, transform=ax.get_yaxis_transform(), ha="right", va="bottom")

ax.axvline(0.35, color="tab:red", linestyle="--")

ax.set_xlabel('PGA (g)')
ax.set_ylabel('MIDR (%)')
ax.set_title('Incremental Dynamic Analysis (IDA)')
ax.legend(loc='upper left')
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)
ax.tick_params(direction='in', top=True, right=True)
ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig(output_filename, dpi=1200)
plt.show()
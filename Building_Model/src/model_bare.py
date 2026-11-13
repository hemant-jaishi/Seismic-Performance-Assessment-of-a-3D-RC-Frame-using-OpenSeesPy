# =================================================================
# Importing Libraries
# =================================================================

import openseespy.opensees as ops
import opsvis as opsv
import numpy as np
import matplotlib.pyplot as plt

from nodal_mass_and_udl import *


# =================================================
# model_bare
# =================================================

UDL_applier()

def Plotter():
    opsv.plot_model(node_labels = 0, element_labels = 0)    # 1 to see, 0 to hide
    plt.title('3D Model')

    opsv.plot_load(nep = 10, sfac = 100, node_supports = True)
    plt.title('UDL Applied')

    # format all the text labels to decimal places
    for text in plt.gca().texts:
        try:
            value = float(text.get_text())
            text.set_text(f"{value:0.2f}")
        except ValueError:
            pass   

    plt.show()

# Fix opsv
ops.getNDM = lambda: [3]
ops.getFixedNodes = lambda: [] 
Plotter()
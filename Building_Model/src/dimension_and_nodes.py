# =================================================================
# Importing Libraries
# =================================================================

import openseespy.opensees as ops
import opsvis as opsv
import numpy as np
import matplotlib.pyplot as plt

ops.wipe()                                       # clear any old nodes, models, etc.
ops.model('basic', '-ndm', 3, '-ndf', 6)         # create a 3D model with 6 DOF per node


# ======================================================================================
# Dimension and Nodes 
# ======================================================================================

# ----------------------------------------------------------------------------------
# Geometry & Unit System Definition (mm, sec, N), Global axes X, Y, Z(vertical)
# ----------------------------------------------------------------------------------

inch = 25.4 
ft = 12 * inch
rigidDiaphragm = 1


# -----------------------------------------------------------------------------------
# Nodes Definition : ops.node(nodeTag, x, y, z)
# -----------------------------------------------------------------------------------

# Floor 1st node -------------------------------------------

ops.node(101, 0, 0, 0)
ops.node(102, 2000, 0, 0)
ops.node(103, 4000, 0, 0)
ops.node(104, 0, 2000, 0)
ops.node(105, 2000, 2000, 0)
ops.node(106, 4000, 2000, 0)
ops.node(107, 0, 4000, 0)
ops.node(108, 2000, 4000, 0)
ops.node(109, 4000, 4000, 0)

# ops.fix(nodeTag, Ux, Uy, Uz, Rx, Ry, Rz)
ops.fix(101, 1, 1, 1, 1, 1, 1)
ops.fix(102, 1, 1, 1, 1, 1, 1)
ops.fix(103, 1, 1, 1, 1, 1, 1)
ops.fix(104, 1, 1, 1, 1, 1, 1)
ops.fix(105, 1, 1, 1, 1, 1, 1)
ops.fix(106, 1, 1, 1, 1, 1, 1)
ops.fix(107, 1, 1, 1, 1, 1, 1)
ops.fix(108, 1, 1, 1, 1, 1, 1)
ops.fix(109, 1, 1, 1, 1, 1, 1)

floor_1_nodes = [101, 102, 103, 104, 105, 106, 107, 108, 109]

# 2nd Floor nodes -----------------------------------

ops.node(201, 0, 0, 3000)
ops.node(202, 2000, 0, 3000)
ops.node(203, 4000, 0, 3000)
ops.node(204, 0, 2000, 3000)
ops.node(205, 2000, 2000, 3000)
ops.node(206, 4000, 2000, 3000)
ops.node(207, 0, 4000, 3000)
ops.node(208, 2000, 4000, 3000)
ops.node(209, 4000, 4000, 3000)

floor_2_nodes = [201, 202, 203, 204, 205, 206, 207, 208, 209]

# 3rd Floor nodes --------------------------------------------------

ops.node(301, 0, 0, 6000)
ops.node(302, 2000, 0, 6000)
ops.node(303, 4000, 0, 6000)
ops.node(304, 0, 2000, 6000)
ops.node(305, 2000, 2000, 6000)
ops.node(306, 4000, 2000, 6000)
ops.node(307, 0, 4000, 6000)
ops.node(308, 2000, 4000, 6000)
ops.node(309, 4000, 4000, 6000)

floor_3_nodes = [301, 302, 303, 304, 305, 306, 307, 308, 309]

# Master node ------------------------------------------------------

print('Rigid Diaphragm ON')
ops.constraints('Transformation')
per_direction = 3

master_nodes = [1, 2, 3]

# ops.node(nodeTag, X, Y, Z)
ops.node(1, 2000, 2000, 0)        # Master node for floor 1
ops.node(2, 2000, 2000, 3000)     # Master node for floor 2
ops.node(3, 2000, 2000, 6000)     # Master node for floor 3

# osp.rigidDiaphragm(per_direction, master_nodeTag, *SlavenodeTag)
ops.rigidDiaphragm(per_direction, 1, *floor_1_nodes)
ops.rigidDiaphragm(per_direction, 2, *floor_2_nodes)
ops.rigidDiaphragm(per_direction, 3, *floor_3_nodes)

# ops.fix(master_nodeTag, Ux, Uy, Uz, Mx, My, Mz)
ops.fix(1, 1, 1, 1, 1, 1, 1)
ops.fix(2, 0, 0, 1, 1, 1, 0)
ops.fix(3, 0, 0, 1, 1, 1, 0)
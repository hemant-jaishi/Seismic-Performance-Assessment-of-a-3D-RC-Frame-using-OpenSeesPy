# =================================================================
# Importing Libraries
# =================================================================

import openseespy.opensees as ops
import opsvis as opsv
import numpy as np
import matplotlib.pyplot as plt

from beam_col_section import *


# =================================================
# beam and Column element
# =================================================

Beam_mpul = 230 * 230 * gamma_conc / g
Col_mpul = 300 * 300 * gamma_conc / g

# --------------------------------------------------
# Elements 
# --------------------------------------------------


# Geometric Transformation ------------------------

Beam_X_TransfTag = 1
Beam_Y_TransfTag = 2
Col_TransfTag = 3

# geomTransf(transfType, transfTag, *transfArgs)
ops.geomTransf('Linear', Beam_X_TransfTag, 1, -1, 0)
ops.geomTransf('Linear', Beam_Y_TransfTag, 1, 1, 0)
ops.geomTransf('PDelta', Col_TransfTag, -1, 0, 1)
# ops.geomTransf('PDelta', Col_TransfTag, -1, 0, 1)


# Integration Setup ------------------------------------

Beam_IntTag = 1
Col_IntTag = 2

numIntPts_Beam = 5
numIntPts_Col = 5

# ops.integration('Lobatto', tag, secTag, N)
ops.beamIntegration('Lobatto', Beam_IntTag, Beam_secTag, numIntPts_Beam)
ops.beamIntegration('Lobatto', Col_IntTag, Col_secTag, numIntPts_Col)


# -------------------------------------------------------------------------
# Element Setup
# -------------------------------------------------------------------------

# Beam element
# ops.element('forcebeamcolumn', eleTag, iNode, jNode, transfTag, integrationTag, '-iter', maxIter = 10, tol = 1e-12, '-mass', mass = 0.0)

# Floor 2nd beam --------------------
# Paralled to X-axis
ops.element('forceBeamColumn', 201202, 201, 202, Beam_X_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 202203, 202, 203, Beam_X_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 204205, 204, 205, Beam_X_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 205206, 205, 206, Beam_X_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 207208, 207, 208, Beam_X_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 208209, 208, 209, Beam_X_TransfTag, Beam_IntTag, '-mass', Beam_mpul)

# Paralled to Y-axis
ops.element('forceBeamColumn', 201204, 201, 204, Beam_Y_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 204207, 204, 207, Beam_Y_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 202205, 202, 205, Beam_Y_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 205208, 205, 208, Beam_Y_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 203206, 203, 206, Beam_Y_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 206209, 206, 209, Beam_Y_TransfTag, Beam_IntTag, '-mass', Beam_mpul)

# Floor 3rd
# Parallel to X-axis
ops.element('forceBeamColumn', 301302, 301, 302, Beam_X_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 302303, 302, 303, Beam_X_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 304305, 304, 305, Beam_X_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 305306, 305, 306, Beam_X_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 307308, 307, 308, Beam_X_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 308309, 308, 309, Beam_X_TransfTag, Beam_IntTag, '-mass', Beam_mpul)

# Parallel to Y-axis
ops.element('forceBeamColumn', 301304, 301, 304, Beam_Y_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 304307, 304, 307, Beam_Y_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 302305, 302, 305, Beam_Y_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 305308, 305, 308, Beam_Y_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 303306, 303, 306, Beam_Y_TransfTag, Beam_IntTag, '-mass', Beam_mpul)
ops.element('forceBeamColumn', 306309, 306, 309, Beam_Y_TransfTag, Beam_IntTag, '-mass', Beam_mpul)


# All beam elements in X-direction
X_beams = [
    # Floor 2
    201202, 202203, 204205, 205206, 207208, 208209,
    # Floor 3
    301302, 302303, 304305, 305306, 307308, 308309
]

# All beam elements in Y-direction  
Y_beams = [
    # Floor 2
    201204, 204207, 202205, 205208, 203206, 206209,
    # Floor 3
    301304, 304307, 302305, 305308, 303306, 306309
]

# beams with slab on one side only i.e., edge beam
beams_with_one_P1 = [
    201202, 202203, 207208, 208209, 201204, 204207, 203206, 206209, 301302, 302303, 307308, 308309, 301304, 304307, 303306, 306309
]

# beams with slab on both sides i.e., interior beam
beams_with_two_P1 = [
    204205, 205206, 202205, 205208, 304305, 305306, 302305, 305308
]

# All beam elements combined
all_beams = X_beams + Y_beams


# Column Elements

# Floor 1
ops.element('forceBeamColumn', 101201, 101, 201, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 102202, 102, 202, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 103203, 103, 203, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 104204, 104, 204, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 105205, 105, 205, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 106206, 106, 206, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 107207, 107, 207, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 108208, 108, 208, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 109209, 109, 209, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# Floor 2
ops.element('forceBeamColumn', 201301, 201, 301, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 202302, 202, 302, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 203303, 203, 303, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 204304, 204, 304, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 205305, 205, 305, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 206306, 206, 306, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 207307, 207, 307, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 208308, 208, 308, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)
ops.element('forceBeamColumn', 209309, 209, 309, Col_TransfTag, Col_IntTag, '-mass', Col_mpul)

# 1st Floor all column
Floor_1_col = [
    101201, 102202, 103203, 104204, 105205, 106206, 107207, 108208, 109209
]

# 2nd Floor all column
Floor_2_col = [
    201301, 202302, 203303, 204304, 205305, 206306, 207307, 208308, 209309
]

# All column elements
all_cols = Floor_1_col + Floor_2_col
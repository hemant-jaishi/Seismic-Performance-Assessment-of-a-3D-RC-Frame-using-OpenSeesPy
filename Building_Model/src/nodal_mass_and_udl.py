# =================================================================
# Importing Libraries
# =================================================================

import openseespy.opensees as ops

from beam_col_element import *


# ======================================
# nodal_mass_&_udl
# ======================================

# --------------------------------------
# Gravity Load
# --------------------------------------
slab_thickness = 150.0                      # mm
wall_thickness = 115.0                      # mm
wall_height = 2770.0                        # mm, 3000.0 - 230.0 = 2770.0 , storey height - beam depth
W_floorfinish = 1.0e-3                      # N/mm2, floor finish = 1 kN/m2
LL = 0.3 * 1.0e-3                           # N/mm2, live load = 1 kN/m2, for NLTHA 30% is considered

W_slab = gamma_conc * slab_thickness        # N/mm2, weight per unit area 
TL = W_slab + W_floorfinish + LL

P11 = (1/2) * 2000.0 * 1000.0 * TL          # N, Triangular load on one beam side
P1 = P11 / 2000.0                           # N/mm, equivalent udl

Beam_self_weight = Beam_mpul * g                            # N/mm
Col_self_weight = Col_mpul * g                              # N/mm
wall_load = wall_thickness * wall_height * gamma_masonry    # N/mm, on all beams

# --------------------------------------------------------------------------------
# Nodal Mass Distribution; mass(nodeTag, *massValues)
# --------------------------------------------------------------------------------
bay_witdh_x = bay_width_y = 2000.0
NBayX = 2
NBayY = 2

def lumped_nodal_mass():

    TL_mass = TL * bay_witdh_x * bay_width_y * NBayX * NBayY / g
    half_wall_mass = (wall_load/2) * (bay_witdh_x * NBayX * (NBayY + 1) + bay_width_y * NBayY * (NBayX + 1)) / g
    full_wall_mass = half_wall_mass * 2

    for node in master_nodes:
        if node == master_nodes[0] or node == master_nodes[-1]:
            ops.mass(node,TL_mass + half_wall_mass, TL_mass + half_wall_mass, 0.0, 0.0, 0.0, 0.0 )
        else:
            ops.mass(node,TL_mass + full_wall_mass, TL_mass + full_wall_mass, 0.0, 0.0, 0.0, 0.0 )

lumped_nodal_mass()

# --------------------------------------------------------------------------------
# Application Of UDL in local coordinate axes 
# --------------------------------------------------------------------------------
ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)

# eleLoad('-ele', *eleTags, '-range', eleTag1, eleTag2, '-type', '-beamUniform', Wy, <Wz>, Wx=0.0, '-beamPoint', Py, <Pz>, xL, Px=0.0, '-beamThermal', *tempPts)
def UDL_applier():
    # UDL Application on Beams
    ops.eleLoad('-ele', *beams_with_one_P1, '-type', '-beamUniform', -P1, 0.0, 0.0)
    ops.eleLoad('-ele', *beams_with_two_P1, '-type', '-beamUniform', -(2*P1), 0.0, 0.0)
    ops.eleLoad('-ele', *all_beams, '-type', '-beamUniform', -(Beam_self_weight + wall_load), 0.0, 0.0)
    # UDL Application on Columns
    ops.eleLoad('-ele', *all_cols, '-type', '-beamUniform', 0.0, 0.0, -Col_self_weight)
    
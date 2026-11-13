# =================================================================
# Importing Libraries
# =================================================================

import openseespy.opensees as ops
import opsvis as opsv
import numpy as np
import matplotlib.pyplot as plt

from dimension_and_nodes import *
from material import *


# =================================================
# beam and Column section
# =================================================

# Beam and column dimension -------------------------------
# beam = 230 x 230
# column = 300 x 300
# beam cover = 25 mm
# column cover = 40 mm
# beam rebar = 12 mm dia.
# beam stirrups = 8 mm dia. 
# column rebar = 16 mm dia.
# column stirrups = 8 mm dia.

def area(diameter):
    return (np.pi * diameter ** 2) / 4

Beam_secTag = 1
Col_secTag = 2

beamcolors = ['tab:orange', 'skyblue', 'w', 'w']
columncolors = ['tab:green', 'yellow', 'w', 'w']


# Beam ----------------------------------------------------

fiber_section_beam = [

    ['section', 'fiber', Beam_secTag, '-GJ', 1.0e06],
    ['patch', 'rect', confined_concrete_tag, 6, 6, *[-90, -90], *[90, 90]],  # core
    
    ['patch', 'quad', unconfined_concrete_tag, 2, 6, *[90, -90], *[115, -115], *[115, 115], *[90, 90]],      # right side cover
    ['patch', 'quad', unconfined_concrete_tag, 2, 6, *[-115, -115], *[-90, -90], *[-90, 90], *[-115, 115]],  # left side cover
    ['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-90, 90], *[90, 90], *[115, 115], *[-115, 115]],      # top side cover
    ['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-115, -115], *[115, -115], *[90, -90], *[-90, -90]],   # bottom side cover

    ['layer', 'straight', steel_tag, 2, area(12), *[90, 90], *[90, -90]],   # right layer
    ['layer', 'straight', steel_tag, 2, area(12), *[-90, 90], *[-90, -90]]  # left layer 

]

opsv.fib_sec_list_to_cmds(fiber_section_beam)

opsv.plot_fiber_section(fiber_section_beam, matcolor=beamcolors)
plt.title("Beam section")
plt.axis('equal')
plt.show()


# Column section ------------------------------------------

fiber_section_col = [

    ['section', 'fiber', Col_secTag, '-GJ', 1.0e06],
    ['patch', 'rect', confined_concrete_tag, 6, 6, *[-110, -110], *[110, 110]],   # core concrete

    ['patch', 'quad', unconfined_concrete_tag, 2, 6, *[110, -110], *[150, -150], *[150, 150], *[110, 110]],       # right side cover
    ['patch', 'quad', unconfined_concrete_tag, 2, 6, *[-150, -150], *[-110, -110], *[-110, 110], *[-150, 150]],   # left side cover
    ['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-110, 110], *[110, 110], *[150, 150], *[-150, 150]],       # top cover
    ['patch', 'quad', unconfined_concrete_tag, 6, 2, *[-150, -150], *[150, -150], *[110, -110], *[-110, -110]],   # bottom cover

    ['layer', 'straight', steel_tag, 3, area(16), *[110, 110], *[110, -110]],   # right layer
    ['layer', 'straight', steel_tag, 3, area(16), *[-110, 110], *[-110, -110]]  # left layer

]

opsv.fib_sec_list_to_cmds(fiber_section_col)

opsv.plot_fiber_section(fiber_section_col, matcolor=columncolors)
plt.title("Column Section")
plt.axis('equal')
plt.show()
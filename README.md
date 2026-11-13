# Seismic-Performance-Assessment-of-a-3D-RC-Frame-using-OpenSeesPy

A 3D reinforced concrete frame modelled in OpenSeesPy and analysed with modal, pushover, nonlinear time history (NLTHA) and incremental dynamic analysis (IDA). The project demonstrates a systematic workflow for structural modelling, nonlinear analysis, result extraction, and seismic performance assessment using Python and OpenSeesPy.

> Note: The building geometry and layout are assumed to represent a typical RC frame. The results demonstrate the analysis methodology and are not intended to represent an assessment of an actual building.  

## Model

| Item | Value |
|---|---|
| Storeys | 2 storeys, 3000 mm each (6000 mm total) |
| Plan | 2 × 2 bays, 2000 mm each |
| Beams / columns | 230 × 230 mm / 300 × 300 mm |
| Concrete | Concrete02, f'c = 20 MPa (confined core and unconfined cover) |
| Reinforcement | Steel02, fy = 415 MPa, E = 200 GPa, b = 0.01 |
| Elements | Force-based beam-column elements, fibre sections, Lobatto integration (5 points) |
| Floors | Rigid diaphragm, mass lumped at floor nodes |
| Loads | Self weight, slab 150.0 mm, floor finish 1.0 kN/m², live load 1.0 kN/m² (30% for mass), masonry walls 115.0 mm thick |
| Damping | Rayleigh, 5% (modes 1 and 4 for X, modes 2 and 5 for Y) |
| Periods | T1 = 0.3315034215 sec, T2 = 0.3253704570 sec, T3 = 0.1685643346 sec (torsional) |

## Analyses

1. **Modal analysis**: natural periods and mode shapes.
2. **Pushover**: equal lateral force at each floor, displacement control up to 4% roof drift.
3. **NLTHA**: 7 ground motions (RSN 5676, 5259, 4199, 3282, 2510, 2476, 334) scaled to PGA = 0.35 g, in the X and Y directions.
4. **IDA**: the same records scaled from 0.05 g up to 2.0 g. A run counts as collapse if it does not converge or the storey drift exceeds 5%.

Performance limits used for the discussion: IO = 1%, LS = 2%, CP = 4% maximum inter-storey drift ratio (MIDR).

## Results

![Pushover curves](Plots/Pushover_curves.png)
![MIDR profile](Plots/MIDR_Profile.png)
![IDA curves](Plots/IDA_curves.png)

| NLTHA Result at PGA = 0.35 g (mean of 7 records) | X-direction | Y-direction |
|---|---|---|
| Maximum base shear (kN) | 319.858 | 322.252 |
| Maximum top displacement (mm) | 65.658 | 59.535 |
| Maximum MIDR (%) | 1.139 | 1.024 |


## How to run

1. Install the packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Download the ground motions from the PEER NGA-West2 database and place them in `GM_data/D/` as `RSN_<number>.txt` (see `GM_data/D/README.txt`).
3. Run the scripts from `Building_Model/src/`:
   - Single IDA run: `python IDA.py 334 2 0.5` (RSN, direction: 1 = X / 2 = Y, PGA in g)
   - Full IDA: `python run_ida.py`
   - Pushover: `python pushover_analysis.py`
4. Results are written to `Output/`. The source files in `Building_Model/src/` make the plots, which are saved in `Plots/`.

## Repository structure

```
Building_Model/
├─src/          dimension_and_nodes, material, material_test, beam_col_section, beam_col_element, nodal_mass_and_udl, model_bare, model_analysis, gravity_analysis, pushover, NLTHA, IDA, run_IDA

GM_data/D/        ground motion files for the soil type D is included in folder D along with raw/original data
Output/           result CSV files
Plots/            figures
```

## Limitations

- Assumed building geometry and loads.
- Bare frame: masonry walls are included as load and mass only, with no stiffness.
- The IDA uses [7] ground motions; [fragility curves are not included yet].
- Collapse is judged by non-convergence or 5% storey drift.

## Future work

- Extend the IDA and derive fragility curves for IO, LS and CP.
- Add infill walls or retrofit options and compare the results.

## Author

Hemant Jaishi, Civil Engineering Student  
078bce060.hemant@pcampus.edu.np | https://linkedin.com/in/hemantjaishi

## License

MIT License, see `LICENSE`.

#!/bin/sh

python3 gmi_create_tesseroid_model.py
python3 gmi_calculate_effect_of_each_tesseroid.py
python3 gmi_create_design_matrix.py
python3 gmi_invert.py

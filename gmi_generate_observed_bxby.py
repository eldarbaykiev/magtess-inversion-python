CRED = '\033[91m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'

CEND = '\033[0m'



import gmi_misc

gmi_misc.print_header()
print("script_plot_observed")

USE_GRD = False

#read parameters from file



import gmi_config
gmi_config.read_config()



import matplotlib.pyplot as plt
import pyshtools

import numpy as np
from scipy.interpolate import griddata

COMPONENT = 'By'
OBSERVED_DATA = 'LCS1/LCS_' + COMPONENT + '.xyz'
SUBTRACT_DATA = 'hemant-remanence-model_fixed/hemant_vim_remanence_fixed.magtess_result_' + COMPONENT + '_filt.xyz'

try:
	raw_grid = gmi_misc.read_global_grid_from_xyz_file(OBSERVED_DATA)
except IOError as err:
	print("CAN NOT OPEN OBSERVED DATAFILE: {0}".format(err))
	exit(-1)

try:
	#raw_subtract_grid = gmi_misc.read_tess_output_global_grid_from_file(gmi_config.SUBTRACT_DATA)
	raw_subtract_grid = gmi_misc.read_global_grid_from_xyz_file(SUBTRACT_DATA)
except IOError as err:
	print("WARNING: CAN NOT OPEN SUBTRACTEBLE DATAFILE: {0}".format(err))
	raw_subtract_grid = raw_grid*0.0

raw_grid = raw_grid - raw_subtract_grid

shtools_inp_grid = pyshtools.SHGrid.from_array(raw_grid)

#get SH coefficients
shtools_coeff = shtools_inp_grid.expand(normalization='schmidt')
shtools_coeff_filt = gmi_misc.remove_lw_sh_coeff(shtools_coeff, gmi_config.N_MIN_CUTOFF)
shtools_coeff_filt.to_file('observed_' + COMPONENT + '_filt.coeff')

d_sh = gmi_misc.read_coeffs_from_text_file('observed_' + COMPONENT + '_filt.coeff', gmi_config.N_MIN_CUTOFF)
n_coeff = len(d_sh)


shtools_grd_filt  = shtools_coeff_filt.expand(grid='DH2')


import gmi_spectral_tools

import convert_shtools_grids
shtools_grd_filt.to_file('observed_' + COMPONENT + '.dat')
convert_shtools_grids.conv_grid('observed_' + COMPONENT + '.dat')

shtools_grd = shtools_coeff.expand(grid='DH2')
shtools_grd.to_file('observed_ufilt_' + COMPONENT + '.dat')
convert_shtools_grids.conv_grid('observed_ufilt_' + COMPONENT + '.dat')

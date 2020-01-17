import matplotlib.pyplot as plt
import pyshtools

import numpy as np

import sys

import gmi_misc
import convert_shtools_grids

try:
	#raw_grid = gmi_misc.read_tess_output_global_grid_from_file(sys.argv[1])
	raw_grid = gmi_misc.read_global_grid_from_xyz_file(sys.argv[1])
except IOError as err:
	print("CAN NOT OPEN OBSERVED DATAFILE: {0}".format(err))
	exit(-1)

shtools_inp_grid = pyshtools.SHGrid.from_array(raw_grid)

#get SH coefficients
shtools_coeff = shtools_inp_grid.expand(normalization='schmidt')
shtools_coeff_filt = gmi_misc.remove_lw_sh_coeff(shtools_coeff, 16)
shtools_grd_filt  = shtools_coeff_filt.expand(grid='DH2')


shtools_grd_filt.to_file(sys.argv[1][0:len(sys.argv[1])-4]+'_filt.dat')
convert_shtools_grids.conv_grid(sys.argv[1][0:len(sys.argv[1])-4]+'_filt.dat')

import gmi_misc
#**************** PRINT HEADER ***************************#
gmi_misc.print_header()
print("Grid reading test")
#**************** ------------ ***************************#

#**************** GET WORKING DIRECTORY ******************#
import os
old_cwd = os.getcwd()
gmi_misc.info('Current directory: '+ old_cwd)

WORKING_DIR = ''
import sys
if len(sys.argv) == 1:
    WORKING_DIR = ''

WORKING_DIR = sys.argv[1]

try:
    os.chdir(WORKING_DIR)
except:
    gmi_misc.error('CAN NOT OPEN WORKING DIRECTORY '+ WORKING_DIR + ', ABORTING...')

gmi_misc.info('WORKING DIRECTORY: '+ os.getcwd())
#**************** --------------------- ******************#


#**************** read parameters from file **************#
import gmi_config
gmi_config.read_config()
#**************** ------------------------- **************#


#BODY*****************************************************#
import matplotlib.pyplot as plt
import pyshtools

import numpy as np
from scipy.interpolate import griddata

#read design matrices
try:
	A_sh = np.load('design_matrix_shcoeff.npy')
	A_sh = np.transpose(A_sh)
	
	A_ufilt_sh = np.load('design_matrix_ufilt_shcoeff.npy')
	A_ufilt_sh = np.transpose(A_ufilt_sh)
except:
	print("CAN NOT OPEN SH COEFF DESIGN MATRIX")
	exit(-1)
	
#read initial solution
sus_grid = gmi_misc.read_sus_grid(gmi_config.INIT_SOLUTION)
dm1, dm2, x0 = gmi_misc.convert_surf_grid_to_xyz(sus_grid)

d_matmul_sh = np.matmul(A_sh, x0)
	
#read PRECALCULATED observed grid
try:
	raw_grid = gmi_misc.read_tess_output_global_grid_from_file(gmi_config.OBSERVED_DATA)
	#raw_grid = gmi_misc.read_global_grid_from_xyz_file(gmi_config.OBSERVED_DATA)
except IOError as err:
	print("CAN NOT OPEN OBSERVED DATAFILE: {0}".format(err))
	exit(-1)
	
#get SH coefficients
shtools_coeff = shtools_inp_grid.expand(normalization='schmidt')
shtools_coeff_filt = gmi_misc.remove_lw_sh_coeff(shtools_coeff, gmi_config.N_MIN_CUTOFF)
shtools_coeff_filt.to_file("observed_filt.coeff")

d_sh = gmi_misc.read_coeffs_from_text_file("observed_filt.coeff", gmi_config.N_MIN_CUTOFF)
print (d_matmul_sh - d_sh)



#*********************************************************#


#**************** RETURN BACK TO INITIAL PATH ***#
os.chdir(old_cwd)
#**************** --------------------------- ***#

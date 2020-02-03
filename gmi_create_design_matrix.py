import gmi_misc

gmi_misc.print_header()
print ("Script no. 3: Creation of design matrices")

#read parameters from file

import gmi_config
gmi_config.read_config()

TRUNCATE = True

USE_GRD = False


import os

import glob

os.chdir('model')
coefflist = glob.glob("*.coeff")
os.chdir('..')


n_tess = len(coefflist)
if n_tess == 0:
	print ("NO CALCULATED SH MODELS OF EACH TESSEROID'S MAGNETIC FIELD")
	exit(-1)


print("NOTE: SUSCEPTIBILITY OF EACH TESSEROID IS MULTIPLIED BY ", str(gmi_config.MULTIPLICATOR))

import pyshtools
import numpy as np

coeff_filename = 'model/tess_n' + str(0) + '.coeff'

b = gmi_misc.read_coeffs_from_text_file(coeff_filename, gmi_config.N_MIN_CUTOFF)
n_vals = len(b)
#print (str(n_vals))

if USE_GRD:
	current_coeff = pyshtools.SHCoeffs.from_file(coeff_filename)
	if TRUNCATE == True:
		current_coeff_filt = gmi_misc.remove_lw_sh_coeff(current_coeff, gmi_config.N_MIN_CUTOFF)
	else:
		current_coeff_filt = current_coeff
	current_grid_filt = current_coeff_filt.expand(grid='DH2')
	c = current_grid_filt.to_array()
	d = c.flatten()
	n_gridvals = d.size
	print (str(n_gridvals))


print ('Assemblying the design matrices...')
from tqdm import tqdm
A = np.zeros((n_tess, n_vals))
A_ufilt = np.zeros((n_tess, n_vals))

if USE_GRD:
	B = np.zeros((n_tess, n_gridvals))

for i in tqdm(range(n_tess)):
	coeff_filename = 'model/tess_n' + str(i) + '.coeff'

	b = gmi_misc.read_coeffs_from_text_file(coeff_filename, gmi_config.N_MIN_CUTOFF)
	b_ufilt = gmi_misc.read_coeffs_from_text_file(coeff_filename, 0)
	A[i, :] = b[:]
	A_ufilt[i, :] = b_ufilt[:]

	if USE_GRD:
		current_coeff = pyshtools.SHCoeffs.from_file(coeff_filename)
		if TRUNCATE == True:
			current_coeff_filt = gmi_misc.remove_lw_sh_coeff(current_coeff, gmi_config.N_MIN_CUTOFF )
		else:
			current_coeff_filt = current_coeff
		current_grid_filt = current_coeff_filt.expand(grid='DH2')
		c = current_grid_filt.to_array()
		d = c.flatten()
		B[i, :] = d[:]
		#print b

print ('...done')

np.save('design_matrix_shcoeff', A)
np.save('design_matrix_ufilt_shcoeff', A_ufilt)
if USE_GRD:
	np.save('design_matrix_grd', B)
#np.savetxt('design_matrix_test.txt', A)

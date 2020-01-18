CRED = '\033[91m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'

CEND = '\033[0m'



import gmi_misc

gmi_misc.print_header()
print("Script no. 4: Inversion")

USE_GRD = False

#read parameters from file
import gmi_config
gmi_config.read_config()

import matplotlib.pyplot as plt
import pyshtools

import numpy as np
from scipy.interpolate import griddata

try:
	raw_grid = gmi_misc.read_tess_output_global_grid_from_file(gmi_config.OBSERVED_DATA)
	#raw_grid = gmi_misc.read_global_grid_from_xyz_file(gmi_config.OBSERVED_DATA)
except IOError as err:
	print("CAN NOT OPEN OBSERVED DATAFILE: {0}".format(err))
	exit(-1)

try:
	#raw_subtract_grid = gmi_misc.read_tess_output_global_grid_from_file(gmi_config.SUBTRACT_DATA)
	raw_subtract_grid = gmi_misc.read_global_grid_from_xyz_file(gmi_config.SUBTRACT_DATA)
except IOError as err:
	print("WARNING: CAN NOT OPEN SUBTRACTEBLE DATAFILE: {0}".format(err))
	raw_subtract_grid = raw_grid*0.0

raw_grid = raw_grid - raw_subtract_grid

shtools_inp_grid = pyshtools.SHGrid.from_array(raw_grid)

#get SH coefficients
shtools_coeff = shtools_inp_grid.expand(normalization='schmidt')
shtools_coeff_filt = gmi_misc.remove_lw_sh_coeff(shtools_coeff, gmi_config.N_MIN_CUTOFF)
shtools_coeff_filt.to_file("observed_filt.coeff")

d_sh = gmi_misc.read_coeffs_from_text_file("observed_filt.coeff", gmi_config.N_MIN_CUTOFF)
n_coeff = len(d_sh)

try:
	A_sh = np.load('design_matrix_shcoeff.npy')
	A_ufilt_sh = np.load('design_matrix_ufilt_shcoeff.npy')
except:
	print("CAN NOT OPEN SH COEFF DESIGN MATRIX")
	exit(-1)

import scipy.io
#scipy.io.savemat("design_matrix_shcoeff.mat", {'A_sh_fromfile': A_sh, 'd_sh': d_sh})
A_sh = np.transpose(A_sh)
A_ufilt_sh = np.transpose(A_ufilt_sh)


shtools_grd_filt  = shtools_coeff_filt.expand(grid='DH2')
a_grd = shtools_grd_filt.to_array()
d_grd = a_grd.flatten()
n_gridvals = len(d_grd)

if USE_GRD:
	try:
		A_grd = np.load('design_matrix_grd.npy')
	except:
		print("CAN NOT OPEN GRID DESIGN MATRIX")
		exit(-1)
	A_grd = np.transpose(A_grd)


n_tess = len(A_sh[0, :])
#print(str(n_tess))


#SOLVING
import gmi_inv_methods

#apriori susceptibility
try:
	x0 = np.loadtxt(gmi_config.INIT_SOLUTION)
except IOError as err:
	print("WARNING: CAN NOT OPEN INITIAL SOLUTION FILE: {0}".format(err))
	exit()
#	try:
#		x0 = np.loadtxt('apriori_VIM/' + gmi_config.PROJECT_NAME + '.x0')
#	except IOError as err:
#		print("WARNING: CAN NOT OPEN INITIAL SOLUTION FILE: {0}".format(err))
#		print("SETTING UP STANDART INITIAL SOLUTION: 0.02 SI for continental crust, 0.05 SI for oceanic crust")

#		land_mask = gmi_misc.read_suscept_global_grid_from_file('land_mask_float.xyz')
#		x0 = land_mask*0.0
#		for i in range(len(x0)):
#			if land_mask[i] < 0.5:
#				x0[i] = 0.02
#			else:
#				x0[i] = 0.05



print(str(x0))
print(str(len(x0)))
np.savetxt('x0_apriori.dat', x0, delimiter=' ')

import gmi_spectral_tools
approx_lw_spec, deg_observed_lw = gmi_spectral_tools.Estimate_LW_Power_Spectrum_Curve(raw_grid)
spec_result_lw, deg_result_lw = gmi_spectral_tools.Estimate_LW_Power_Spectrum_of_curr_solution(A_ufilt_sh, x0)

h_sh = gmi_inv_methods.Projected_Gradient(A_sh, d_sh, x0)

sh_result_coeffs = np.matmul(A_sh, h_sh)
sh_result_coeffs_shtools = gmi_misc.convert_result_into_shtools_format(sh_result_coeffs, 'result.coeff')
#sh_result_coeffs_shtools = pyshtools.SHCoeffs.from_file('result.coeff', normalization='schmidt')
sh_result_grid = sh_result_coeffs_shtools.expand(grid='DH2')


sh_result_ufilt_coeffs = np.matmul(A_ufilt_sh, h_sh)
sh_result_ufilt_coeffs_shtools = gmi_misc.convert_result_into_shtools_format(sh_result_ufilt_coeffs, 'result_ufilt.coeff')
#sh_result_ufilt_coeffs_shtools = pyshtools.SHCoeffs.from_file('result_ufilt.coeff', normalization='schmidt')
sh_result_ufilt_grid = sh_result_ufilt_coeffs_shtools.expand(grid='DH2')

import convert_shtools_grids
shtools_grd_filt.to_file('observed_shtools.dat')
convert_shtools_grids.conv_grid('observed_shtools.dat')
sh_result_grid.to_file('result_shtools.dat')
convert_shtools_grids.conv_grid('result_shtools.dat')

sh_result_ufilt_grid.to_file('result_ufilt_shtools.dat')
convert_shtools_grids.conv_grid('result_ufilt_shtools.dat')


shtools_grd = shtools_coeff.expand(grid='DH2')
shtools_grd.to_file('observed_ufilt_shtools.dat')
convert_shtools_grids.conv_grid('observed_ufilt_shtools.dat')


import os
os.system('./plot_grid_diff.sh observed_shtools result_shtools diff_shtools 0')
os.system('./plot_grid_diff.sh observed_ufilt_shtools result_ufilt_shtools diff_ufilt_shtools 1')

#plt.show()

sh_result_grid = sh_result_grid.to_array()
observed_grd = shtools_grd_filt.to_array()
sh_misfit = np.linalg.norm(np.subtract(observed_grd, sh_result_grid))**2


sh_result_ufilt_grid = sh_result_ufilt_grid.to_array()
observed_ufilt_grd = shtools_grd.to_array()
sh_ufilt_misfit = np.linalg.norm(np.subtract(observed_ufilt_grd, sh_result_ufilt_grid ))**2

print("Misfit (grids): " + str(sh_misfit))
print('\n')

spec_H, deg_H = gmi_spectral_tools.Estimate_LW_Power_Spectrum_of_curr_solution(A_ufilt_sh, h_sh)
spec_misfit = np.linalg.norm(np.subtract(approx_lw_spec, spec_H))**2

print("Misfit (LW): " + str(spec_misfit))
print('\n')


with open('output.txt', 'w') as foutput:
	foutput.write('MAX SH DEGREE: ' + str(shtools_coeff.lmax) + '\n')
	foutput.write('Misfit^2 (grids): ' + str(sh_misfit) + '\n')
	foutput.write('Misfit ufilt^2 (grids): ' + str(sh_ufilt_misfit) + '\n')
	foutput.write('Misfit^2 (spec): ' + str(spec_misfit) + '\n')

if USE_GRD:
	h_grd = L2_minimization(A_grd, d_grd, 0.25)

	grd_result_grid = np.matmul(A_grd, h_grd)
	grd_misfit = np.linalg.norm(np.subtract(d_grd, grd_result_grid))**2
	print("Misfit: " + str(grd_misfit))
	print('\n')

######################

#output grid
min_lon = gmi_config.LON_MIN
max_lon = gmi_config.LON_MAX
min_lat = gmi_config.LAT_MIN
max_lat = gmi_config.LAT_MAX
step = gmi_config.WIDTH

#NUMBER OF TESSEROIDS
n_lon = int(abs(max_lon - step/2.0 - (min_lon + step/2.0)) / step + 1)
n_lat = int(abs(max_lat - step/2.0 - (min_lat + step/2.0)) / step + 1)

lons = np.linspace(min_lon+ step/2.0, max_lon-step/2.0, n_lon)
lats = np.linspace(min_lat+ step/2.0, max_lat-step/2.0, n_lat)

X,Y = np.meshgrid(lons, lats)


ind = 0
with open('model_reslt_sh.xyz', 'w') as tessfile:
	for i in range(n_lat-1, -1, -1):
		for j in range(n_lon):
			k = h_sh
			string = str(X[i, j]) + ' ' + str(Y[i, j]) + ' ' + str(k[ind])
			#print string
			tessfile.write(string + '\n')
			ind = ind+1

os.system('./plot_result.sh ' + 'model_reslt_sh')

ind = 0
with open('x0_apriori.xyz', 'w') as apriorifile:
	for i in range(n_lat-1, -1, -1):
		for j in range(n_lon):
			k = h_sh
			string = str(X[i, j]) + ' ' + str(Y[i, j]) + ' ' + str(x0[ind])
			#print string
			apriorifile.write(string + '\n')
			ind = ind+1

os.system('./plot_result.sh ' + 'x0_apriori')
os.system('./plot_sus_diff.sh')



if (os.path.isfile('model_reslt_sh.xyz') == True) and (os.path.isfile('model.magtess') == True):
	os.system('tail -n +5 model.magtess > dummy')
	os.system("awk '{print $9,$10,$11}' dummy > magfield")
	os.system("awk '{print $1,$2,$3,$4,$5,$6,$7}' dummy > tessrd")
	os.system("awk '{print $3}' model_reslt_sh.xyz > sus")
	os.system('paste tessrd sus > tessrdsus')
	os.system('paste tessrdsus magfield > result_model.magtess')

	os.system('rm dummy')
	os.system('rm magfield')
	os.system('rm tessrd')
	os.system('rm sus')
	os.system('rm tessrdsus')

if USE_GRD:
	ind = 0
	with open('model_reslt_grd.xyz', 'w') as tessfile:
		for i in range(n_lat-1, -1, -1):
			for j in range(n_lon):
				k = h_grd
				string = str(X[i, j]) + ' ' + str(Y[i, j]) + ' ' + str(k[ind])
				#print string
				tessfile.write(string + '\n')
				ind = ind+1

if len(gmi_config.PROJECT_NAME) > 0:
	foldername = gmi_config.PROJECT_NAME
else:
	from datetime import datetime
	now = datetime.now()
	foldername = now.strftime("%Y_%m_%d_%H_%M_%S")

foldername = 'result_' + foldername


os.mkdir(foldername)
import shutil
shutil.copyfile('input.txt', './' + foldername + '/' + 'input.txt')
shutil.copyfile('output.txt', './' + foldername + '/' + 'output.txt')
shutil.copyfile('x0_apriori.dat', './' + foldername + '/' + 'x0_apriori.dat')
shutil.copyfile('x0_apriori.jpg', './' + foldername + '/' + 'x0_apriori.jpg')
shutil.copyfile('x0_apriori.xyz', './' + foldername + '/' + 'x0_apriori.xyz')
shutil.copyfile('model_reslt_sh.xyz', './' + foldername+ '/' + 'model_reslt_sh.xyz')
shutil.copyfile('model_reslt_sh.jpg', './' + foldername+ '/' + 'model_reslt_sh.jpg')
shutil.copyfile('result.coeff', './' + foldername+ '/' + 'result.coeff')
shutil.copyfile('observed_filt.coeff', './' + foldername+ '/' + 'observed_filt.coeff')
shutil.copyfile('result_shtools.jpg', './' + foldername+ '/' + 'result_shtools.jpg')
shutil.copyfile('result_shtools.xyz', './' + foldername+ '/' + 'result_shtools.xyz')
shutil.copyfile('result_ufilt_shtools.jpg', './' + foldername+ '/' + 'result_ufilt_shtools.jpg')
shutil.copyfile('result_ufilt_shtools.xyz', './' + foldername+ '/' + 'result_ufilt_shtools.xyz')
shutil.copyfile('observed_shtools.jpg', './' + foldername+ '/' + 'observed_shtools.jpg')
shutil.copyfile('observed_shtools.xyz', './' + foldername+ '/' + 'observed_shtools.xyz')
shutil.copyfile('observed_ufilt_shtools.jpg', './' + foldername+ '/' + 'observed_ufilt_shtools.jpg')
shutil.copyfile('observed_ufilt_shtools.xyz', './' + foldername+ '/' + 'observed_ufilt_shtools.xyz')
shutil.copyfile('diff_shtools.jpg', './' + foldername+ '/' + 'diff_shtools.jpg')
shutil.copyfile('diff_ufilt_shtools.jpg', './' + foldername+ '/' + 'diff_ufilt_shtools.jpg')
shutil.copyfile('sus_difference.jpg', './' + foldername+ '/' + 'sus_difference.jpg')
shutil.copyfile('result_model.magtess', './' + foldername+ '/' + 'result_model.magtess')



shutil.copyfile('nlssubprob.dat', './' + foldername+ '/' + 'nlssubprob.dat')

converg = np.loadtxt(foldername+ '/' + 'nlssubprob.dat')

import matplotlib.pyplot as plt



fig, ax = plt.subplots()
ax.plot(converg[:, 0], converg[:, 1])

ax.set(xlabel='Iteration', ylabel='Projected Gradient',
       title='Convergence')
ax.grid()

fig.savefig(foldername+ '/' + "nlssubprob.png")
plt.show()

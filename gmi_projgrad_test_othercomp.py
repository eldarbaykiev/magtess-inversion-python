
import gmi_misc

gmi_misc.print_header()
print "Othercomp"

#read parameters from file

import gmi_config
gmi_config.read_config()



import matplotlib.pyplot as plt
import pyshtools

import numpy as np
from scipy.interpolate import griddata


def show_tess_output_filt_grid(filename):
	print filename
	try:
		raw_grid = gmi_misc.read_tess_output_global_grid_from_file(filename)  #fix this later
	except IOError as err:
		print "CAN NOT OPEN OBSERVED DATAFILE: {0}".format(err)
		exit(-1)

	shtools_inp_grid = pyshtools.SHGrid.from_array(-raw_grid)

	#get SH coefficients
	shtools_coeff = shtools_inp_grid.expand(normalization='schmidt')
	shtools_coeff_filt = gmi_misc.remove_lw_sh_coeff(shtools_coeff, gmi_config.N_MIN_CUTOFF)
	shtools_grid_filt = shtools_coeff_filt.expand(grid='DH2')

	#shtools_grid_filt.plot()
	
	return shtools_grid_filt

	

result_grid = show_tess_output_filt_grid('ProjectedGradient/resultmodel.magtess_By')
observed_grid = show_tess_output_filt_grid('hemant_vis_global_crust1.0/result.magtess_By.txt')

misfit_grid = observed_grid - result_grid

step = gmi_config.GRID_STEP#abs(LON[1] - LON[0])

min_lon = 0
max_lon = 360
min_lat = -90
max_lat = 90

n_lat = len(np.arange(min_lat, max_lat, step))
n_lon = len(np.arange(min_lon, max_lon, step))

lats = np.linspace(max_lat, min_lat, n_lat)
lons = np.linspace(min_lon, max_lon, n_lon)

X,Y = np.meshgrid(lons, lats)




arr = result_grid.to_array()
with open('filt_result_grid_by.xyz', 'w') as fle:
	for i in range(n_lat):
		for j in range(n_lon):
			fle.write(str(X[i, j]) + ' ' + str(Y[i, j]) + ' ' + str(arr[i, j] ) + '\n')

arr = observed_grid.to_array()	
with open('filt_observed_grid_by.xyz', 'w') as fle:
	for i in range(n_lat):
		for j in range(n_lon):
			fle.write(str(X[i, j]) + ' ' + str(Y[i, j]) + ' ' + str(arr[i, j] ) + '\n')
			
arr = misfit_grid.to_array()	
with open('misfit_grid_by.xyz', 'w') as fle:
	for i in range(n_lat):
		for j in range(n_lon):
			fle.write(str(X[i, j]) + ' ' + str(Y[i, j]) + ' ' + str(arr[i, j] ) + '\n')
			
			
	
		
		
#observed_grid.to_file('Bz_filtered_observed_grid')
#misfit_grid.to_file('Bz_misfit_grid')


#plt.show()
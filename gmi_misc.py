def print_header():
	print "**********************************"
	print "*   GLOBAL MAGNETIC INVERSION    *"
	print "*     Eldar Baykiev, 2019        *"
	print "*                                *"
	print "**********************************"
	print ""
	print ""


def read_tess_output_global_grid_from_file(filename):
	import numpy as np
	from scipy.interpolate import griddata

	import gmi_config
	gmi_config.read_config()

	data = np.loadtxt(filename, delimiter=" ")
	LON = data[:, 0]
	LAT = data[:, 1]
	ALT = data[:, 2]
	VAL = data[:, 3]

	step = gmi_config.GRID_STEP#abs(LON[1] - LON[0])

	#flip coord system to fit SHTOOLS convention
	for i in range(1, len(LON), 1):
		if LON[i]<0:
			LON[i] = 360+LON[i]

	min_lon = 0
	max_lon = 360
	min_lat = -90
	max_lat = 90

	n_lat = len(np.arange(min_lat, max_lat, step))
	n_lon = len(np.arange(min_lon, max_lon, step))

	lats = np.linspace(max_lat, min_lat, n_lat)
	lons = np.linspace(min_lon, max_lon, n_lon)

	X,Y = np.meshgrid(lons, lats) 

	#in SHTOOLS format
	raw_grid = griddata((LON, LAT), -VAL, (X,Y), method='nearest')

	return raw_grid


def remove_lw_sh_coeff(sh_coff, n_cutoff):
	import pyshtools
	shtools_zero_coeff = pyshtools.SHCoeffs.from_zeros(len(sh_coff.degrees())-1)
	shtools_zero_coeff = shtools_zero_coeff.convert('schmidt')
	shtools_zero_coeff.coeffs[:, n_cutoff:, :] = sh_coff.coeffs[:, n_cutoff:, :] 
	return shtools_zero_coeff


def read_coeffs_from_text_file(shc_filename, n_cutoff):
	import numpy as np
	data = np.loadtxt(shc_filename, delimiter=",")
	
	#print data[:, 0]
	ind = np.where(data[:, 0] < n_cutoff)
	data[ind, 2] = np.zeros(len(ind))
	data[ind, 3] = np.zeros(len(ind))

	out = np.concatenate((data[:, 2], data[:, 3]))
	return out
	
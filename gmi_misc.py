import numpy as np
from scipy.interpolate import griddata

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	CBEIGE  = '\33[36m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	CEND = '\033[0m'

def print_header():
	from datetime import date
	today = date.today()

	print (bcolors.HEADER + "**********************************" + bcolors.ENDC)
	print (bcolors.HEADER + "*   GLOBAL MAGNETIC INVERSION    *" + bcolors.ENDC)
	print (bcolors.HEADER + "*      Eldar Baykiev, 2019       *" + bcolors.ENDC)
	print (bcolors.HEADER + "*         Python  3.8.1          *" + bcolors.ENDC)
	print (bcolors.HEADER + "*                                *" + bcolors.ENDC)
	print (bcolors.HEADER + "*           " + today.strftime("%d/%m/%Y") + "           *" + bcolors.ENDC)
	print (bcolors.HEADER + "**********************************" + bcolors.ENDC)
	print ("")
	print ("")

def create_tess_cpoint_grid():
	import numpy as np

	import gmi_config
	gmi_config.read_config()

	n_lon = int(abs(gmi_config.LON_MAX - gmi_config.WIDTH/2.0 - (gmi_config.LON_MIN + gmi_config.WIDTH/2.0)) / gmi_config.WIDTH + 1)
	n_lat = int(abs(gmi_config.LAT_MAX - gmi_config.WIDTH/2.0 - (gmi_config.LAT_MIN + gmi_config.WIDTH/2.0)) / gmi_config.WIDTH + 1)

	lons = np.linspace(gmi_config.LON_MIN+ gmi_config.WIDTH/2.0, gmi_config.LON_MAX-gmi_config.WIDTH/2.0, n_lon)
	lats = np.linspace(gmi_config.LAT_MIN+ gmi_config.WIDTH/2.0, gmi_config.LAT_MAX-gmi_config.WIDTH/2.0, n_lat)

	X,Y = np.meshgrid(lons, lats)

	return n_lon, n_lat, X, Y

def read_surf_grid(fname):

	n_lon, n_lat, X, Y = create_tess_cpoint_grid()
	try:
		grid_surf = np.loadtxt(fname, delimiter=" ")
	except IOError as err:
		error("ERROR: CAN NOT OPEN SURFACE FILE: {0}".format(err))

	grid = griddata((grid_surf[:,0], grid_surf[:,1]), grid_surf[:,2], (X,Y), method='nearest')
	return grid

def warning(str):
	print (bcolors.WARNING + str + bcolors.ENDC)

def error(str):
	print (bcolors.FAIL + str + bcolors.ENDC)
	exit(-1)

def debug(str):
	print (bcolors.CBEIGE + str + bcolors.ENDC)

def info(str):
	print (bcolors.OKBLUE + str + bcolors.ENDC)


def pause():
    programPause = input("Press the <ENTER> key to continue...")

def ok(str):
    print (bcolors.OKGREEN + str + bcolors.ENDC)

def ask():
	ans = input('(Y/N) << ').lower()
	if ans in ['yes', 'y']:
		return True
	if ans in ['no', 'n']:
		return False

def read_data_grid(filename):
	import numpy as np
	from scipy.interpolate import griddata

	import gmi_config
	gmi_config.read_config()

	try:
		data = np.loadtxt(filename, delimiter=" ")

		LON = data[:, 0]
		LAT = data[:, 1]
		ALT = data[:, 2]
		VAL = data[:, 3] * -1.0

		warning('magtess grid')
	except:
		try:
			data = np.loadtxt(filename, delimiter=" ")
			LON = data[:, 0]
			LAT = data[:, 1]
			VAL = data[:, 2]

			warning('XYZ grid')
		except:
			error("CAN NOT READ " + filename)
			exit(-1)



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
	raw_grid = griddata((LON, LAT), VAL, (X,Y), method='nearest')

	return raw_grid


def subtract_tess_output_global_grids(filename1, filename2, output_filename):
	#NOT TESTED
	import numpy as np
	from scipy.interpolate import griddata

	import gmi_config
	gmi_config.read_config()

	data1 = np.loadtxt(filename1, delimiter=" ")
	LON = data1[:, 0]
	LAT = data1[:, 1]
	ALT = data1[:, 2]
	VAL1 = data1[:, 3]

	data2 = np.loadtxt(filename2, delimiter=" ")
	VAL2 = data2[:, 3]

	VAL = VAL1 - VAL2

	with open(output_filename, 'w') as ofile:
		for i in range(len(LON)):
			ofile.write(str(LON[i]) + ' ' + str(LAT[i]) + ' ' + str(ALT[i]) + ' ' + str(VAL[i]) + '\n')

	return




def read_suscept_global_grid_from_file(filename):
	import numpy as np
	from scipy.interpolate import griddata

	import gmi_config
	gmi_config.read_config()

	try:
		data = np.loadtxt(filename, delimiter="\t")
	except ValueError:
		print('WARNING! ' + str(filename) + ' is suspected not to have a tabular delimiter, trying with a space delimiter')

		try:
			data = np.loadtxt(filename, delimiter=" ")

		except:
			print('CON NOT READ ' + str(filename) + ' with space delimiter, abort!')
			exit(-1)


	LON = data[:, 0]
	LAT = data[:, 1]
	VAL = data[:, 2]

	n_lon, n_lat, X, Y = create_tess_cpoint_grid()

	#in SHTOOLS format
	sus_grid = griddata((LON, LAT), VAL, (X,Y), method='nearest')

	x_0 = np.zeros(n_lon*n_lat)
	ind = 0
	for i in range(n_lat-1, -1, -1):
		for j in range(n_lon):
			x_0[ind] = sus_grid[i, j]
			ind = ind+1

	return x_0


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

def convert_result_into_shtools_format(vect, fname):
	import numpy as np

	try:
		shdata = np.loadtxt('model/tess_n0.coeff', delimiter=",")
	except:
		print ("CAN NOT OPEN model/tess_n0.coeff")
		exit(-1)

	half = len(shdata[:, 2])
	shdata[:, 2] = vect[0:half]
	shdata[:, 3] = vect[half:]

	with open(fname, 'w') as fresult:
		for i in range(half):
			fresult.write(str(int(shdata[i, 0])) + ', ' + str(int(shdata[i, 1])) + ', ' + str(float(shdata[i, 2])) + ', ' + str(float(shdata[i, 3])) + '\n')

	import pyshtools
	shtools_result_coeff = pyshtools.SHCoeffs.from_file(fname, normalization='schmidt')
	return shtools_result_coeff


def write_sus_grid_to_file(sus, fname):
	import numpy as np

	import gmi_config
	gmi_config.read_config()

	n_lon, n_lat, X, Y = create_tess_cpoint_grid()

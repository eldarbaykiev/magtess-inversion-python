import gmi_misc

gmi_misc.print_header()
print ("Script no. 2: Calculation of the magnetic field of each tesseroid in the model")

#read parameters from file

import gmi_config
gmi_config.read_config()

import numpy as np


#check if previous stages were launched
try:
	read_dictionary = np.load('checksums.npy',allow_pickle='TRUE').item()
except:
	print("RUN Script no. 1 first! ABORTING...")
	exit(-1)

if len(read_dictionary['stage1']) == 0:
	print("RUN Script no. 1 first! ABORTING...")
	exit(-1)

import hashlib
file_name = 'model.magtess'
with open(file_name, 'r') as file_to_check:
    # read contents of the file
    data = file_to_check.read()
    # pipe contents of the file through
    md5_stage1 = hashlib.md5(data.encode('utf-8')).hexdigest()

if md5_stage1 != read_dictionary['stage1']:
	print(file_name + ' was changed after the run of Script 1, restart Script no. 1 first! ABORTING...')
	exit(-1)
else:
	pass

from scipy.interpolate import griddata

grid_n_lon = int(abs(gmi_config.GRID_LON_MAX - (gmi_config.GRID_LON_MIN)) / gmi_config.GRID_STEP + 1)
grid_n_lat = int(abs(gmi_config.GRID_LAT_MAX - (gmi_config.GRID_LAT_MIN)) / gmi_config.GRID_STEP + 1)

grid_lons = np.linspace(gmi_config.GRID_LON_MIN, gmi_config.GRID_LON_MAX, grid_n_lon)
grid_lats = np.linspace(gmi_config.GRID_LAT_MIN, gmi_config.GRID_LAT_MAX, grid_n_lat)

grid_X,grid_Y = np.meshgrid(grid_lons, grid_lats)

with open('grid.txt', 'w') as tessfile:
	for i in range(grid_n_lat):
		for j in range(grid_n_lon):
			string = str(grid_X[i, j]) + ' ' + str(grid_Y[i, j]) + ' ' + str(gmi_config.GRID_ALT) + ' '
			#print string
			tessfile.write(string + '\n')

try:
	mag_tesseroids = np.loadtxt('model.magtess', delimiter=" ")
except IOError as err:
	print ("CAN NOT OPEN TESSEROID MODEL: {0}".format(err))
	exit(-1)
#print mag_tesseroids
n_tess = len(mag_tesseroids)
print ('Number of tesseroids in the model: ' + str(n_tess))



import gmi_misc


from tqdm import tqdm

import pyshtools
coeff_info = pyshtools.SHCoeffs.from_zeros(1)


import os
try:
	os.mkdir('model')
except:
	print ("model folder already exists!")


import platform
oper_system = platform.system()

tessbz_filename = 'tessbz'
if oper_system == 'Linux':
	tessbz_filename = 'tessbz_linux'


print("NOTE: SUSCEPTIBILITY OF EACH TESSEROID IS MULTIPLIED BY ", str(gmi_config.MULTIPLICATOR))


if os.path.isfile(tessbz_filename) == False:
	print ("CAN NOT FIND " + tessbz_filename + " IN THE CURRENT DIRECTORY")
	exit(-1)

print ('Calculating effects of each tesseroid...')
for i in tqdm(range(n_tess)):
	tessfile = open('dummy.magtess', 'w')
	string = str(mag_tesseroids[i, 0]) + ' ' + str(mag_tesseroids[i, 1]) + ' ' + str(mag_tesseroids[i, 2]) + ' ' + str(mag_tesseroids[i, 3]) + ' ' + str(mag_tesseroids[i, 4]) + ' ' + str(mag_tesseroids[i, 5]) + ' ' + str(mag_tesseroids[i, 6]) + ' ' + str(mag_tesseroids[i, 7]) + ' ' + str(mag_tesseroids[i, 8]) + ' ' + str(mag_tesseroids[i, 9]) + ' ' + str(mag_tesseroids[i, 10])
	tessfile.write(string + '\n')
	tessfile.close()

	command_bz = "./" + tessbz_filename + " dummy.magtess < grid.txt > " + "out_Bz.txt"
	command = command_bz + '\n'
	os.system(command)

	raw_grid = gmi_misc.read_tess_output_global_grid_from_file("out_Bz.txt")
	shtools_inp_grid = pyshtools.SHGrid.from_array(raw_grid)

	#get SH coefficients
	shtools_coeff = shtools_inp_grid.expand(normalization='schmidt')
	coeff_info = shtools_coeff

	shtools_coeff.to_file('model/tess_n' + str(i) + '.coeff')

	os.remove("out_Bz.txt")
	os.remove("dummy.magtess")


print ('...done')

print ('Properties of SHCoeffs:')
print (coeff_info.info())
print ("Max degree: " + str(coeff_info.lmax))


#os.chdir('model')


def calculate_checksum(filenames):
    hash = hashlib.md5()
    for fn in filenames:
        if os.path.isfile(fn):
            hash.update(open(fn, "rb").read())
    return hash.digest()

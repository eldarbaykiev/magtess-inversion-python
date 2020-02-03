import gmi_misc
#**************** PRINT HEADER ***************************#
gmi_misc.print_header()
print ("Script no. 2: Calculation of the magnetic field of each tesseroid in the model")
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


#************ check if previous stages were launched *****#
import gmi_hash
stages = [0,0,0]
stages, dictionary = gmi_hash.read_dict('checksums.npy')

err = 0
if stages[0] == -1:
	gmi_misc.warning('model.magtess was changed after the run of Script 1, restart Script no. 1 first! ABORTING...')
elif stages[0] == 0:
	gmi_misc.warning('model.magtess was changed after the run of Script 1, restart Script no. 1 first! ABORTING...')
else:
	pass
	
if err > 0:
	gmi_misc.error('CHECKSUM FAILED, ABORTING!')
	
#**************** --------------------- ******************#


#**************** CREATE CALCULATION GRID ****************#
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
			
#**************** --------------------- ******************#


#**************** OPEN TESSEROID MODEL *******************#
try:
	mag_tesseroids = np.loadtxt('model.magtess', delimiter=" ")
except IOError as err:
	gmi_misc.error("CAN NOT OPEN TESSEROID MODEL: {0}".format(err))
	exit(-1)
#print mag_tesseroids
n_tess = len(mag_tesseroids)
print ('Number of tesseroids in the model: ' + str(n_tess))
#**************** --------------------- ******************#


from tqdm import tqdm

import pyshtools
coeff_info = pyshtools.SHCoeffs.from_zeros(1)

import os


if os.path.exists('model'):
	if len(os.listdir('model') ) > 0: 
		gmi_misc.warning("MODEL FOLDER ALREADY EXIST! DO YOU WANT TO RECALCULATE?")
		if gmi_misc.ask() == True:
			pass
		else:
			gmi_misc.error("MODEL FOLDER WAS NOT OVERWRITEN, ABORTING!")
		
else:
	os.mkdir('model')
	
	
gmi_misc.warning("NOTE: SUSCEPTIBILITY OF EACH TESSEROID IS MULTIPLIED BY " + str(gmi_config.MULTIPLICATOR))

n_cpu = 7 #os.cpu_count()
gmi_misc.info('Number of processors: '+ str(n_cpu))


gmi_misc.info('Calculating effects of each tesseroid...')


bar = tqdm(range(n_tess))
i = 0
while i < n_tess:

	curr_max_j = 0
	for j in range(0, n_cpu, 1):
		if (i+j) < n_tess:
			with open('dummy_' + str(j) + '.magtess', 'w') as tessfile:
				string = str(mag_tesseroids[i+j, 0]) + ' ' + str(mag_tesseroids[i+j, 1]) + ' ' + str(mag_tesseroids[i+j, 2]) + ' ' + str(mag_tesseroids[i+j, 3]) + ' ' + str(mag_tesseroids[i+j, 4]) + ' ' + str(mag_tesseroids[i+j, 5]) + ' ' + str(mag_tesseroids[i+j, 6]) + ' ' + str(mag_tesseroids[i+j, 7]) + ' ' + str(mag_tesseroids[i+j, 8]) + ' ' + str(mag_tesseroids[i+j, 9]) + ' ' + str(mag_tesseroids[i+j, 10])
				tessfile.write(string + '\n')
			curr_max_j = curr_max_j + 1


	command_bz = "" + gmi_config.TESSBZ_FILENAME + " dummy_" + str(0) + ".magtess < grid.txt > " + "out_" + str(0) + "_Bz.txt"
	for j in range(1, n_cpu, 1):
		if (i+j) < n_tess:
			command_bz = command_bz + ' | '
			command_bz = command_bz + "" + gmi_config.TESSBZ_FILENAME + " dummy_" + str(j) + ".magtess < grid.txt > " + "out_" + str(j) + "_Bz.txt"
	

	command = command_bz + '\n'
	os.system(command)
	
	for j in range(0, n_cpu, 1):
		if (i+j) < n_tess:

			raw_grid = gmi_misc.read_tess_output_global_grid_from_file("out_" + str(j) + "_Bz.txt")
			shtools_inp_grid = pyshtools.SHGrid.from_array(raw_grid)

			#get SH coefficients
			shtools_coeff = shtools_inp_grid.expand(normalization='schmidt')
			coeff_info = shtools_coeff

			shtools_coeff.to_file('model/tess_n' + str(i) + '.coeff')

			os.remove("out_" + str(j) + "_Bz.txt")
			os.remove('dummy_' + str(j) + '.magtess')
			
			i = i + 1
		
	bar.update(curr_max_j)




gmi_misc.ok('...done')

gmi_misc.info('Properties of SHCoeffs:')
gmi_misc.info(str(coeff_info.info()))
gmi_misc.info("Max degree: " + str(coeff_info.lmax))


#**************** WRITE MD5 PARAMS **************#
dictionary['stage2'] = gmi_hash._gethashofdirs('model', verbose=1)
dictionary['stage3'] = ''
dictionary['stage4'] = ''
np.save('checksums.npy', dictionary)
#**************** ---------------- **************#


#**************** RETURN BACK TO INITIAL PATH ***#
os.chdir(old_cwd)
#**************** --------------------------- ***#
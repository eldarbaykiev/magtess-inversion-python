#**************** TESTING PARAMS (WOULD BE REMOVED)*******#
CREATE_VIM_MODEL = True
#**************** ---------------------------------*******#







import gmi_misc
#**************** PRINT HEADER ***************************#
gmi_misc.print_header()
print ("Script no. 1: Creation of global tesseroid model")
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



import numpy as np
from scipy.interpolate import griddata

n_lon, n_lat, X, Y = gmi_misc.create_tess_cpoint_grid()

def _create_tess_model_file(fname, suscept, x_grid, y_grid, z_topg, z_botg):
	nlat, nlon = x_grid.shape
	
	with open(fname + '.tess', 'w') as tessfile:
		k = 0
		for i in range(nlat-1, -1, -1):
			for j in range(nlon):
				if isinstance(suscept, np.ndarray):
					sus_curr = suscept[k]
				elif isinstance(suscept, float):
					sus_curr = suscept
				else:
					pass
					
				string = str(x_grid[i, j]-gmi_config.WIDTH/2.0) + ' ' + str(x_grid[i, j]+gmi_config.WIDTH/2.0) + ' ' + str(y_grid[i, j]-gmi_config.WIDTH/2.0) + ' ' + str(y_grid[i, j]+gmi_config.WIDTH/2.0) + ' ' + str(z_topg[i, j]) + ' ' +  str(z_botg[i, j]) + ' 1.0 ' + str(sus_curr)
				tessfile.write(string + '\n')
				k = k + 1
				
	os.system(gmi_config.TESSUTIL_MAGNETIZE_MODEL_FILENAME + ' ' + gmi_config.IGRF_COEFF_FILENAME + ' ' + fname + '.tess ' + str(gmi_config.IGRF_DAY) + ' ' + str(gmi_config.IGRF_MONTH) + ' ' + str(gmi_config.IGRF_YEAR) + ' ' + fname + '.magtess')
			
try:
	grid_bot = np.loadtxt(gmi_config.BOT_SURFACE, delimiter=" ")
	grid_top = np.loadtxt(gmi_config.TOP_SURFACE, delimiter=" ")
except IOError as err:
	gmi_misc.error("ERROR: CAN NOT OPEN SURFACE FILE: {0}".format(err))

Z_bot = griddata((grid_bot[:,0], grid_bot[:,1]), grid_bot[:,2], (X,Y), method='nearest')
Z_top = griddata((grid_top[:,0], grid_top[:,1]), grid_top[:,2], (X,Y), method='nearest')

gmi_misc.warning("NOTE: SUSCEPTIBILITY OF EACH TESSEROID IS MULTIPLIED BY "+ str(gmi_config.MULTIPLICATOR))

_create_tess_model_file('model', 1.0*gmi_config.MULTIPLICATOR, X, Y, Z_bot, Z_top)

if CREATE_VIM_MODEL:
	vim_distribution = gmi_misc.read_suscept_global_grid_from_file('apriori_VIM/hemant_VIS.vim')
	sus = np.zeros(len(vim_distribution))
	_create_tess_model_file('apriori_VIM/hemant_VIS', 1.0*gmi_config.MULTIPLICATOR, X, Y, Z_bot, Z_top)

	np.savetxt('apriori_VIM/' + gmi_config.PROJECT_NAME + '.x0', sus*gmi_config.MULTIPLICATOR)

gmi_misc.ok("Magnetic tesseroid model \"model.magtess\" is created")


#**************** WRITE MD5 PARAMS **************#

import hashlib
file_name = 'model.magtess'
with open(file_name, 'r') as file_to_check:
    # read contents of the file
    data = file_to_check.read()
    # pipe contents of the file through
    md5_returned = hashlib.md5(data.encode('utf-8')).hexdigest()

#Save
dictionary = {'stage1':md5_returned,
	'stage2':'',
	'stage3':'',
	'stage4':'',
}
np.save('checksums.npy', dictionary)


#**************** RETURN BACK TO INITIAL PATH ***#
os.chdir(old_cwd)

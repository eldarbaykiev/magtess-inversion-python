import gmi_misc

gmi_misc.print_header()
print "Script no. 1: Creation of global tesseroid model"


#read parameters from file
import gmi_config
gmi_config.read_config()

import numpy as np
from scipy.interpolate import griddata

n_lon = int(abs(gmi_config.LON_MAX - gmi_config.WIDTH/2.0 - (gmi_config.LON_MIN + gmi_config.WIDTH/2.0)) / gmi_config.WIDTH + 1)
n_lat = int(abs(gmi_config.LAT_MAX - gmi_config.WIDTH/2.0 - (gmi_config.LAT_MIN + gmi_config.WIDTH/2.0)) / gmi_config.WIDTH + 1)

lons = np.linspace(gmi_config.LON_MIN+ gmi_config.WIDTH/2.0, gmi_config.LON_MAX-gmi_config.WIDTH/2.0, n_lon)
lats = np.linspace(gmi_config.LAT_MIN+ gmi_config.WIDTH/2.0, gmi_config.LAT_MAX-gmi_config.WIDTH/2.0, n_lat)

X,Y = np.meshgrid(lons, lats)

try:
	grid_bot = np.loadtxt(gmi_config.TOP_SURFACE, delimiter=" ")
	grid_top = np.loadtxt(gmi_config.BOT_SURFACE, delimiter=" ")
except IOError as err:
	print ("CAN NOT OPEN SURFACE FILE: {0}".format(err))

Z_bot = griddata((grid_bot[:,0], grid_bot[:,1]), grid_bot[:,2], (X,Y), method='nearest')
Z_top = griddata((grid_top[:,0], grid_top[:,1]), grid_top[:,2], (X,Y), method='nearest')

k = 0
with open('model.tess', 'w') as tessfile:
	#keeping order as in reference CRUST1.0 file
	for i in range(n_lat-1, -1, -1):
		for j in range(n_lon):
			string = str(X[i, j]-gmi_config.WIDTH/2.0) + ' ' + str(X[i, j]+gmi_config.WIDTH/2.0) + ' ' + str(Y[i, j]-gmi_config.WIDTH/2.0) + ' ' + str(Y[i, j]+gmi_config.WIDTH/2.0) + ' ' + str(Z_top[i, j]) + ' ' +  str(Z_bot[i, j]) + ' 1.0'
			#print string
			tessfile.write(string + '\n')
			k = k + 1

import os
if os.path.isfile('tessutil_magnetize_model') == True:
	os.system('./tessutil_magnetize_model ' + gmi_config.IGRF_COEFF_FILENAME + ' model.tess ' + str(gmi_config.IGRF_DAY) + ' ' + str(gmi_config.IGRF_MONTH) + ' ' + str(gmi_config.IGRF_YEAR) + ' model.magtess')
else:
	print ("CAN NOT FIND tessutil_magnetize_model IN THE CURRENT DIRECTORY")
	exit(-1)

print "Magnetic tesseroid model \"model.magtess\" created. Number of tesseroids in the model: " + str(k)


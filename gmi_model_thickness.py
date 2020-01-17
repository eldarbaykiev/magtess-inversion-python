

import gmi_misc

gmi_misc.print_header()
print("Calculate model's thickness map [lon lat km]")

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
	grid_bot = np.loadtxt(gmi_config.BOT_SURFACE, delimiter=" ")
	grid_top = np.loadtxt(gmi_config.TOP_SURFACE, delimiter=" ")
except IOError as err:
	print ("ERROR: CAN NOT OPEN SURFACE FILE: {0}".format(err))

Z_bot = griddata((grid_bot[:,0], grid_bot[:,1]), grid_bot[:,2], (X,Y), method='nearest')
Z_top = griddata((grid_top[:,0], grid_top[:,1]), grid_top[:,2], (X,Y), method='nearest')



k = 0
with open('model_thickness.xyz', 'w') as tessfile:
	#keeping order as in reference CRUST1.0 file
	for i in range(n_lat-1, -1, -1):
		for j in range(n_lon):
			string = str(X[i, j]) + ' ' + str(Y[i, j]) + ' ' + str(abs(Z_top[i, j]-Z_bot[i, j])/1000.0)
			#print string
			tessfile.write(string + '\n')
			k = k + 1

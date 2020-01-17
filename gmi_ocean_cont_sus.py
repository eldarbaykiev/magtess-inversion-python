

import gmi_misc

gmi_misc.print_header()
print("Get average susceptibilities for ocean/cont")

import gmi_config
gmi_config.read_config()

import numpy as np

x0 = np.loadtxt('apriori_VIM/2degx2deg_apriori_hemant_crust1.0_wolfgang.x0.x0')
print(str(len(x0)))

land_mask = gmi_misc.read_suscept_global_grid_from_file('cont_ocean_mask/cont_ocean_CRUST_mask.xyz')
#x0 = land_mask*0.0

land = []
ocean = []
for i in range(len(x0)):
	if land_mask[i] < 0.5:
		land.append(x0[i])
	else:
		ocean.append(x0[i])
print('1')

av_land = np.sum(land)/len(land)
av_ocean = np.sum(ocean)/len(ocean)

print(av_land)
print(av_ocean)

print('2')
with open('averaged_cont_CRUST_ocean.x0', 'w') as averfile:
	for i in range(len(x0)):
		if land_mask[i] < 0.5:
			averfile.write(str(av_land) + '\n')
		else:
			averfile.write(str(av_ocean) + '\n')

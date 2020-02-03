import gmi_misc
import gmi_config

gmi_config.read_config()

import matplotlib.pyplot as plt

import gmi_gmt


import inspect
def _retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

	
gmi_misc.info(gmi_config.OBSERVED_DATA)
	
try:
	raw_grid = gmi_misc.read_tess_output_global_grid_from_file(gmi_config.OBSERVED_DATA)
	#raw_grid = gmi_misc.read_global_grid_from_xyz_file(gmi_config.OBSERVED_DATA)
	raw_grid = raw_grid
except IOError as err:
	print("CAN NOT OPEN OBSERVED DATAFILE: {0}".format(err))
	exit(-1)
	

gmi_gmt.plot_global_grid(raw_grid, 'test', -12, 12, 'polar', 'Magnetic field', 'nT')

gmi_misc.pause()
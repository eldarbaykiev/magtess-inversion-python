
import gmi_misc





import gmi_config
gmi_config.read_config()



import matplotlib.pyplot as plt
import pyshtools

import numpy as np
from scipy.interpolate import griddata

try:
	raw_grid = gmi_misc.read_global_grid_from_xyz_file('result_2degx2deg_LCS1_filtrem/observed_ufilt_shtools.xyz')

	raw_grid2 = gmi_misc.read_global_grid_from_xyz_file('result_2degx2deg_LCS1_filtrem/result_ufilt_shtools.xyz')
			#raw_grid = gmi_misc.read_global_grid_from_xyz_file(gmi_config.OBSERVED_DATA)
except IOError as err:
	print("CAN NOT OPEN OBSERVED DATAFILE: {0}".format(err))
	exit(-1)

shtools_inp_grid = pyshtools.SHGrid.from_array(raw_grid)
shtools_res_grid = pyshtools.SHGrid.from_array(raw_grid2)

		#get SH coefficients
shtools_coeff = shtools_inp_grid.expand(normalization='schmidt')

spec = shtools_coeff.spectrum()
print(spec)
print(len(spec))


deg = shtools_coeff.degrees()
#shtools_coeff.plot_spectrum2d()



shtools_coeff_filt = gmi_misc.remove_lw_sh_coeff(shtools_coeff, gmi_config.N_MIN_CUTOFF)
spec_filt = shtools_coeff_filt.spectrum()

spec_filt[gmi_config.N_MIN_CUTOFF:] = np.log10(spec_filt[gmi_config.N_MIN_CUTOFF:])
plt.plot(deg[gmi_config.N_MIN_CUTOFF:], spec_filt[gmi_config.N_MIN_CUTOFF:], 'r')
#plt.plot(deg, np.log10(spec), 'r')


shtools_coeff_res = shtools_res_grid.expand(normalization='schmidt')
spec_res = shtools_coeff_res.spectrum()

plt.plot(deg, np.log10(spec_res), 'b')


from scipy import optimize

def test_func(x, a, b, c, d, e, f, g, h, i, j ,k ,l,m):
	return np.polynomial.polynomial.polyval(x, [a, b, c, d, e, f, g, h, i, j ,k ,l,m])

params, params_covariance = optimize.curve_fit(test_func, deg, np.log10(spec),
                                               p0=[1,1,1,1,1,1,1,1,1,1,1,1,0])

#plt.plot(deg, test_func(deg, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9], params[10], params[11], params[12]), label='Fitted function')
print(params)

plt.legend(['observed', 'result'])
plt.savefig("spec.png")
plt.show()

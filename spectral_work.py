
import gmi_misc



import gmi_config
gmi_config.read_config()



import matplotlib.pyplot as plt
import pyshtools

import numpy as np
from scipy.interpolate import griddata

MINN = 1

#FOLDER = 'result_2degx2deg_100000_apriori_wolfgang_ocean_cont_CRUST'
#try:
#	raw_grid_inp = gmi_misc.read_global_grid_from_xyz_file(FOLDER + '/observed_ufilt_shtools.xyz')
#	raw_grid_res = gmi_misc.read_global_grid_from_xyz_file(FOLDER + '/result_ufilt_shtools.xyz')
#	raw_grid_res2 = gmi_misc.read_global_grid_from_xyz_file('result_2degx2deg_1000_apriori_wolfgang_ocean_cont_CRUST/result_ufilt_shtools.xyz')
	

#FOLDER = 'result_2degx2deg_100000_apriori_hemant_crust1.0_wolfgang.x0'
#try:
#	raw_grid_inp = gmi_misc.read_global_grid_from_xyz_file(FOLDER + '/observed_ufilt_shtools.xyz')
	#raw_grid_res = gmi_misc.read_global_grid_from_xyz_file(FOLDER + '/result_ufilt_shtools.xyz')
	#raw_grid_res2 = gmi_misc.read_global_grid_from_xyz_file('result_2degx2deg_apriori_hemant_crust1.0_wolfgang.x0/result_ufilt_shtools.xyz')
	
FOLDER = 'result_2degx2deg_100000_LCS1_filtrem'
try:
	raw_grid_inp = gmi_misc.read_global_grid_from_xyz_file(FOLDER + '/observed_ufilt_shtools.xyz')
	raw_grid_res = gmi_misc.read_global_grid_from_xyz_file(FOLDER + '/result_ufilt_shtools.xyz')
	raw_grid_res2 = gmi_misc.read_global_grid_from_xyz_file('result_2degx2deg_LCS1_filtrem/result_ufilt_shtools.xyz')
	MINN = 16
	
		
		
except IOError as err:
	print("CAN NOT OPEN OBSERVED DATAFILE: {0}".format(err))
	exit(-1)

shtools_inp_grid = pyshtools.SHGrid.from_array(raw_grid_inp)
shtools_res_grid = pyshtools.SHGrid.from_array(raw_grid_res)
shtools_res2_grid = pyshtools.SHGrid.from_array(raw_grid_res2)

		#get SH coefficients
shtools_inp_coeff = shtools_inp_grid.expand(normalization='schmidt')
shtools_res_coeff = shtools_res_grid.expand(normalization='schmidt')
shtools_res2_coeff = shtools_res2_grid.expand(normalization='schmidt')

spec_inp = shtools_inp_coeff.spectrum()
spec_res = shtools_res_coeff.spectrum()
spec_res2 = shtools_res2_coeff.spectrum()

deg = shtools_inp_coeff.degrees()



#shtools_coeff_filt = gmi_misc.remove_lw_sh_coeff(shtools_coeff, gmi_config.N_MIN_CUTOFF)
#spec_filt = shtools_coeff_filt.spectrum()

#spec_filt[gmi_config.N_MIN_CUTOFF:] = np.log10(spec_filt[gmi_config.N_MIN_CUTOFF:])
#plt.plot(deg[gmi_config.N_MIN_CUTOFF:], spec_filt[gmi_config.N_MIN_CUTOFF:], 'r')
#plt.plot(deg, np.log10(spec), 'r')


#shtools_coeff_res = shtools_res_grid.expand(normalization='schmidt')
#spec_res = shtools_coeff_res.spectrum()

plt.plot(deg[MINN:], np.log10(spec_inp)[MINN:], 'b-', lw=0.6)
plt.plot(deg[1:], np.log10(spec_res2)[1:], 'g-', lw=0.6)
plt.plot(deg[1:], np.log10(spec_res)[1:], 'r-', lw=0.6)

#plt.plot([16, 16], [min(min(np.log10(spec_inp)), min(np.log10(spec_res))), 0], 'c')

plt.grid()

a_yticks = np.array([1, 0.1, 0.01, 0.001, 0.0001])
plt.yticks(np.log10(a_yticks), a_yticks.astype(str))
a_xticks = np.array([1, 16, 20, 40, 60, 80, 89])
plt.xticks(a_xticks, a_xticks.astype(str))

#from scipy import optimize

#def test_func(x, a, b, c, d, e, f, g, h, i, j ,k ,l,m):
#	return np.polynomial.polynomial.polyval(x, [a, b, c, d, e, f, g, h, i, j ,k ,l,m])

#params, params_covariance = optimize.curve_fit(test_func, deg, np.log10(spec),
#                                               p0=[1,1,1,1,1,1,1,1,1,1,1,1,0])

#plt.plot(deg, test_func(deg, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9], params[10], params[11], params[12]), label='Fitted function')
#print(params)

plt.title('Power spectrum')
plt.xlabel('SH degree')
plt.ylabel('Power [nT^2]')
plt.legend(['observed', 'result N=1000', 'result N=100000'])
plt.savefig(FOLDER + '/spec.png')
plt.show()

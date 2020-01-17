import numpy as np
import pyshtools
import gmi_config
import gmi_misc
from scipy import optimize

def test_func(x, a, b, c, d, e, f, g, h, i, j ,k ,l,m):
	return np.polynomial.polynomial.polyval(x, [a, b, c, d, e, f, g, h, i, j ,k ,l,m])

def Estimate_LW_Power_Spectrum_Curve(input_obs_raw_grid):
	grd_observed_all = pyshtools.SHGrid.from_array(input_obs_raw_grid)
	sh_observed_all = grd_observed_all.expand(normalization='schmidt')
	spec_observed_all = sh_observed_all.spectrum()
	deg_observed_all = sh_observed_all.degrees()

	spec_observed_lw = spec_observed_all[0:gmi_config.N_MIN_CUTOFF]
	deg_observed_lw = deg_observed_all[0:gmi_config.N_MIN_CUTOFF]

	from scipy import optimize
	params, params_covariance = optimize.curve_fit(test_func, deg_observed_lw, np.log10(spec_observed_lw),
                                               p0=[1,1,1,1,1,1,1,1,1,1,1,1,0])

	
	approx_lw_spec = 10.0**test_func(deg_observed_lw, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9], params[10], params[11], params[12])

	return approx_lw_spec, deg_observed_lw

def Estimate_LW_Power_Spectrum_of_curr_solution(DesMatrix, Solution):
	R = np.matmul(DesMatrix, Solution)
	R_shtools = gmi_misc.convert_result_into_shtools_format(R, 'dummy.coeff')
	#sh_result_coeffs_shtools = pyshtools.SHCoeffs.from_file('result.coeff', normalization='schmidt')
	spec_result_all = R_shtools.spectrum()
	deg_result_all = R_shtools.degrees()

	spec_result_lw = spec_result_all[0:gmi_config.N_MIN_CUTOFF]
	deg_result_lw = deg_result_all[0:gmi_config.N_MIN_CUTOFF]

	#plt.plot(deg_result_lw, np.log10(spec_result_lw))

	return spec_result_lw, deg_result_lw
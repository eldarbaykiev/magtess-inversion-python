
import gmi_misc

gmi_misc.print_header()
print "Script no. 4: Inversion"

#read parameters from file

import gmi_config
gmi_config.read_config()



import matplotlib.pyplot as plt
import pyshtools

import numpy as np
from scipy.interpolate import griddata

try:
	raw_grid = gmi_misc.read_tess_output_global_grid_from_file(gmi_config.OBSERVED_DATA)  #fix this later
except IOError as err:
	print "CAN NOT OPEN OBSERVED DATAFILE: {0}".format(err)
	exit(-1)

shtools_inp_grid = pyshtools.SHGrid.from_array(raw_grid)

#get SH coefficients
shtools_coeff = shtools_inp_grid.expand(normalization='schmidt')
shtools_coeff_filt = gmi_misc.remove_lw_sh_coeff(shtools_coeff, gmi_config.N_MIN_CUTOFF)
shtools_coeff_filt.to_file("observed_filt.coeff")

d_sh = gmi_misc.read_coeffs_from_text_file("observed_filt.coeff", gmi_config.N_MIN_CUTOFF)
n_coeff = len(d_sh)

try:
	A_sh = np.load('design_matrix_shcoeff.npy')
except:
	print "CAN NOT OPEN SH COEFF DESIGN MATRIX"
	exit(-1)

import scipy.io
scipy.io.savemat("design_matrix_shcoeff.mat", {'A_sh_fromfile': A_sh, 'd_sh': d_sh})
A_sh = np.transpose(A_sh)

def show_matrix_corners(matr):
	print matr[0, 0]
	print matr[-1, -1]
	print matr[0, -1]
	print matr[-1, 0]



shtools_grd_filt  = shtools_coeff_filt.expand(grid='DH2')
a_grd = shtools_grd_filt.to_array()
d_grd = a_grd.flatten()
n_gridvals = len(d_grd)

try:
	A_grd = np.load('design_matrix_grd.npy')
except:
	print "CAN NOT OPEN GRID DESIGN MATRIX"
	exit(-1)
A_grd = np.transpose(A_grd)


n_tess = len(A_sh[:, 0])



import scipy.sparse.linalg
import scipy.optimize



#SOLVING

def Projected_Gradient(A, d, x_0):
	print "Projected Gradient inversion"
	import time
	start = time.time()

	A_T = np.transpose(A)

	n_bodies = len(A_T[:, 0])
	print "  Number of bodies: " + str(n_bodies)
	n_points = len(A_T[0, :])
	print "  Number of datapoints: " + str(n_points)

	import nimfa

	h=nimfa.Lsnmf(V=A, W=d, H=np.ones(n_bodies)*x_0, max_iter=1000, min_residuals=1e-6)
	print h()

	exit()
	end = time.time()
	print "  Time spent: " + str(end - start) + " sec"
	print h
	return h


#Generalized Tikhonov
def Generalized_Tikhonov(A, d, sigma_d, sigma_x, x_0):
	print "Generalized Tikhonov inversion"
	import time
	start = time.time()

	A_T = np.transpose(A)

	n_bodies = len(A_T[:, 0])
	print "  Number of bodies: " + str(n_bodies)
	n_points = len(A_T[0, :])
	print "  Number of datapoints: " + str(n_points)

	print "  Variance of data: " + str(sigma_d)
	print "  Variance of susceptibility: " + str(sigma_x) + " SI"
	print "  A-priori susceptibility: " + str(x_0) + " SI"

	#print str(n_bodies)
	#print str(n_points)


	COV_d = np.dot(np.identity(n_points), (sigma_d*sigma_d))
	P = np.linalg.inv(COV_d)
	COV_x = np.dot(np.identity(n_bodies), (sigma_x*sigma_x))
	Q = np.linalg.inv(COV_x)

	A_TP = np.dot(A_T, P)
	A_TPA = np.dot(A_TP, A)

	A_TPApQ_inv = np.linalg.inv(np.add(A_TPA, Q))

	A_TPd = np.matmul(A_TP, d)

	col = np.matmul(Q, (np.ones(n_bodies)*x_0))
	A_TPdpQx0 = np.add(A_TPd, col)

	h = np.matmul(A_TPApQ_inv, A_TPdpQx0)

	end = time.time()
	print "  Time spent: " + str(end - start) + " sec"
	print h
	return h

#L2 minimization
def L2_minimization(A, d, alpha):
	print "L2 minimization"
	import time
	start = time.time()

	A_T = np.transpose(A)
	ATA = np.dot(A_T, A)
	ATA_inv = np.linalg.inv(np.add(ATA, np.identity(len(ATA))*alpha**2))
	L = np.dot(ATA_inv, A_T)
	h = np.dot(L, d)

	end = time.time()
	print "  Time spent: " + str(end - start) + " sec"
	print h
	return h



#h_sh = Generalized_Tikhonov(A_sh, d_sh, 0.001, 0.01, 0.02)
#h_sh = L2_minimization(A_sh, d_sh, 0.25)
#h_sh = scipy.sparse.linalg.lsqr(A_sh, d_sh)
#h_sh = scipy.optimize.lsq_linear(A_sh, d_sh, bounds=(0, 0.06))
#h_sh = scipy.optimize.nnls(A_sh, d_sh)
h_sh = Projected_Gradient(A_sh, d_sh, 0.02)


h_grd = Generalized_Tikhonov(A_grd, d_grd, 0.5, 0.01, 0.02)
#h_grd = L2_minimization(A_grd, d_grd, 0.25)
#h_grd = scipy.sparse.linalg.lsqr(A_grd, d_grd)
#h_grd = scipy.optimize.lsq_linear(A_grd, d_grd, bounds=(0, 0.06))
#h_grd = scipy.optimize.nnls(A_grd, d_grd)
#h_grd = Projected_Gradient(A_grd, d_grd, 0.02)

######################

#output grid
min_lon = gmi_config.LON_MIN
max_lon = gmi_config.LON_MAX
min_lat = gmi_config.LAT_MIN
max_lat = gmi_config.LAT_MAX
step = gmi_config.WIDTH
print step

#NUMBER OF TESSEROIDS
n_lon = int(abs(max_lon - step/2.0 - (min_lon + step/2.0)) / step + 1)
n_lat = int(abs(max_lat - step/2.0 - (min_lat + step/2.0)) / step + 1)

lons = np.linspace(min_lon+ step/2.0, max_lon-step/2.0, n_lon)
lats = np.linspace(min_lat+ step/2.0, max_lat-step/2.0, n_lat)

X,Y = np.meshgrid(lons, lats)


ind = 0
with open('model_reslt_sh.xyz', 'w') as tessfile:
	for i in range(n_lat-1, -1, -1):
		for j in range(n_lon):
			k = h_sh
			string = str(X[i, j]) + ' ' + str(Y[i, j]) + ' ' + str(k[ind])
			#print string
			tessfile.write(string + '\n')
			ind = ind+1


ind = 0
with open('model_reslt_grd.xyz', 'w') as tessfile:
	for i in range(n_lat-1, -1, -1):
		for j in range(n_lon):
			k = h_grd
			string = str(X[i, j]) + ' ' + str(Y[i, j]) + ' ' + str(k[ind])
			#print string
			tessfile.write(string + '\n')
			ind = ind+1

#

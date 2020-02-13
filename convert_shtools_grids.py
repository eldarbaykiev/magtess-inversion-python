import numpy as np

import sys
import gmi_misc

def convert_sht_grid_to_xyz(inp):
    if isinstance(inp, str):
        try:
            grid = np.loadtxt(inp)
        except:
            gmi_misc.error('CAN NOT OPEN/WRONG FORMAT')
            exit()
    else:
        grid = inp

    lat_N = len(grid[:, 0])
    lon_N = len(grid[0, :])

    X = np.zeros(lat_N*lon_N)
    Y = np.zeros(lat_N*lon_N)
    Z = np.zeros(lat_N*lon_N)
    k = 0
    for i in range(0, lon_N):
        for j in range(0, lat_N):
            if (0.0+float(i)*360.0/float(lon_N) <180.0):

                X[k] = 0.0+float(i)*360.0/float(lon_N)
            else:
                X[k] = -360.0 + 0.0+float(i)*360.0/float(lon_N)

            Y[k] = 90.0-float(j)*180.0/float(lat_N)
            Z[k] = grid[j, i]
            k += 1


    return X, Y, Z


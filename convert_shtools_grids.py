import numpy as np

import sys

def conv_grid(fname):
    try:
        grid = np.loadtxt(fname)
    except:
        print('CAN NOT OPEN/WRONG FORMAT')
        exit()

    #print grid
    #print len(grid[:, 0])
    #print len(grid[0, :])

    lat_N = len(grid[:, 0])
    lon_N = len(grid[0, :])

    with open(fname[0:len(fname)-4] + '.xyz', 'w') as outputf:
        for i in range(0, lon_N):
            for j in range(0, lat_N):
                outputf.write(str(0.0+i*360.0/float(lon_N)) + ' ' +  str(90.0-j*180.0/float(lat_N)) + ' ' + str(grid[j, i]) + '\n')

    import os

    os.system('./plot_grid.sh ' + fname[0:len(fname)-4] + '\n')


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print('ERROR: enter SHTools grid name (*.dat)')
        exit()

    elif len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print('SHTOOLS GRID CONVERTER. Usage: python conver_shtools_grids.py grid_filename.dat')
            exit()

        else:
            print('FILENAME: ' + sys.argv[1])
            print('FILENAME: ' + sys.argv[1][0:len(sys.argv[1])-4])

            conv_grid(sys.argv[1])


    else:
        print('ERROR: wrong argument, use -h for help')
        exit()

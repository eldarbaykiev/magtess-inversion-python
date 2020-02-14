import numpy as np
from scipy.interpolate import griddata
import os
import sys

verbosity_level = 1

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    CBEIGE  = '\33[36m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CEND = '\033[0m'

def version():
    return "0.1.0"

def init_result_folder():

    import gmi_config
    gmi_config.read_config()

    if len(gmi_config.PROJECT_NAME) > 0:
        foldername = gmi_config.PROJECT_NAME
    else:
        from datetime import datetime
        now = datetime.now()
        foldername = now.strftime("%Y_%m_%d_%H_%M_%S")

    foldername = 'result_' + foldername

    try:
        os.mkdir(foldername)
    except:
        warning('RESULT FOLDER ALREADY EXIST!')

    return foldername

def print_header():
    from datetime import date
    today = date.today()

    message (bcolors.HEADER + "*"*34 + bcolors.ENDC)
    message (bcolors.HEADER + "*   GLOBAL MAGNETIC INVERSION    *" + bcolors.ENDC)
    message (bcolors.HEADER + "*      Eldar Baykiev, 2019       *" + bcolors.ENDC)
    message (bcolors.HEADER + "*        v" + version() + " "*(23-len(version()))+ "*" + bcolors.ENDC)
    message (bcolors.HEADER + "*                                *" + bcolors.ENDC)
    message (bcolors.HEADER + "*           " + today.strftime("%d/%m/%Y") + " "*11 + "*" + bcolors.ENDC)
    message (bcolors.HEADER + "*"*34 + bcolors.ENDC)
    message ("")
    message ("")

def create_tess_cpoint_grid():
    import numpy as np

    import gmi_config
    gmi_config.read_config()

    n_lon = int(abs(gmi_config.LON_MAX - gmi_config.WIDTH/2.0 - (gmi_config.LON_MIN + gmi_config.WIDTH/2.0)) / gmi_config.WIDTH + 1)
    n_lat = int(abs(gmi_config.LAT_MAX - gmi_config.WIDTH/2.0 - (gmi_config.LAT_MIN + gmi_config.WIDTH/2.0)) / gmi_config.WIDTH + 1)

    lons = np.linspace(gmi_config.LON_MIN+ gmi_config.WIDTH/2.0, gmi_config.LON_MAX-gmi_config.WIDTH/2.0, n_lon)
    lats = np.linspace(gmi_config.LAT_MIN+ gmi_config.WIDTH/2.0, gmi_config.LAT_MAX-gmi_config.WIDTH/2.0, n_lat)

    X,Y = np.meshgrid(lons, lats)

    return n_lon, n_lat, X, Y


def read_surf_grid(fname):

    n_lon, n_lat, X, Y = create_tess_cpoint_grid()
    try:
        grid_surf = np.loadtxt(fname, delimiter=" ")
    except IOError as err:
        error("ERROR: CAN NOT OPEN SURFACE FILE: {0}".format(err))

    grid = griddata((grid_surf[:,0], grid_surf[:,1]), grid_surf[:,2], (X,Y), method='nearest')
    return grid

def convert_surf_grid_to_xyz(grid):
    nlon, nlat, X, Y = create_tess_cpoint_grid()

    import numpy as np
    grd_X = np.zeros(nlon*nlat)
    grd_Y = np.zeros(nlon*nlat)
    grd_VAL = np.zeros(nlon*nlat)

    k = 0
    for i in range(nlat-1, -1, -1):
        for j in range(nlon):
            grd_X[k] = X[i, j]
            grd_Y[k] = Y[i, j]
            grd_VAL[k] = grid[i, j]
            k += 1

    return grd_X, grd_Y, grd_VAL

def read_sus_grid(fname):
    if ('.vim' in fname[-5:]) or ('.vis' in fname[-5:]):
        debug('SUSCEPTIBILITY FILE (' + fname + ') TYPE: VERTICALLY INTEGRATED SUSCEPTIBILITY GRID [lon] [lat] [VIS]')
        import gmi_config
        gmi_config.read_config()

        x0 = read_surf_grid(fname)

        try:
            grid_top = read_surf_grid(gmi_config.TOP_SURFACE)
            grid_bot = read_surf_grid(gmi_config.BOT_SURFACE)
        except:
            gmi_misc.error('CAN NOT OPEN TOP OR BOT')
        thickness = (grid_top - grid_bot)/1000.0

        grid = x0 / thickness


    elif ('.xyz' in fname[-5:]):
        grid = read_surf_grid(fname)

    elif ('.x0' in fname[-5:]):
        debug('SUSCEPTIBILITY FILE (' + fname + ') TYPE: x0 COLUMN [sus]')
        import numpy as np
        try:
            x0 = np.loadtxt(fname)
        except IOError as err:
            error("CAN NOT OPEN INITIAL SOLUTION FILE: {0}".format(err))

        nlon, nlat, X, Y = create_tess_cpoint_grid()

        with open('temp_surf.xyz', 'w') as surffile:
            k = 0
            for i in range(nlat-1, -1, -1):
                for j in range(nlon):
                    sus_curr = x0[k]

                    string = str(X[i, j]) + ' ' + str(Y[i, j]) + ' ' + str(sus_curr)
                    surffile.write(string + '\n')
                    k += 1

        grid = read_surf_grid('temp_surf.xyz')



    else:
        error('CAN NOT RECOGNIZE SUSCEPTIBILITY FILE (' + fname + ') TYPE, ABORTING')

    return grid


def warning(msg=None):
    if verbosity_level >= 1:
        print (bcolors.WARNING + f"WARNING [{sys._getframe().f_back.f_code.co_filename}|{sys._getframe().f_back.f_code.co_name}|{sys._getframe().f_back.f_lineno}]: {msg if msg is not None else ''}" + bcolors.ENDC)

def error(msg=None):
    import sys
    print(bcolors.FAIL + f"ERROR [{sys._getframe().f_back.f_code.co_filename}|{sys._getframe().f_back.f_code.co_name}|{sys._getframe().f_back.f_lineno}]: {msg if msg is not None else ''}" + bcolors.ENDC )

    #print (bcolors.FAIL + msg + bcolors.ENDC)
    exit(-1)

def debug(msg=None):
    if verbosity_level == 3:
        print (bcolors.CBEIGE + f"DEBUG [{sys._getframe().f_back.f_code.co_filename}|{sys._getframe().f_back.f_code.co_name}|{sys._getframe().f_back.f_lineno}]: {msg if msg is not None else ''}" + bcolors.ENDC)

def info(str):
    if verbosity_level >= 1:
        print (bcolors.OKBLUE + str + bcolors.ENDC)

def message(msg):
    print( msg)

def pause():
    programPause = input("Press the <ENTER> key to continue...")

def ok(str):
    print (bcolors.OKGREEN + str + bcolors.ENDC)

def ask():
    ans = input('(Y/N) << ').lower()
    if ans in ['yes', 'y']:
            return True
    if ans in ['no', 'n']:
            return False

def create_calc_grid(filename):
    import gmi_config
    gmi_config.read_config()

    from scipy.interpolate import griddata
    import numpy as np

    grid_n_lon = int(abs(gmi_config.GRID_LON_MAX - (gmi_config.GRID_LON_MIN)) / gmi_config.GRID_STEP + 1)
    grid_n_lat = int(abs(gmi_config.GRID_LAT_MAX - (gmi_config.GRID_LAT_MIN)) / gmi_config.GRID_STEP + 1)

    grid_lons = np.linspace(gmi_config.GRID_LON_MIN, gmi_config.GRID_LON_MAX, grid_n_lon)
    grid_lats = np.linspace(gmi_config.GRID_LAT_MIN, gmi_config.GRID_LAT_MAX, grid_n_lat)

    grid_X, grid_Y = np.meshgrid(grid_lons, grid_lats)

    with open('grid.txt', 'w') as tessfile:
            for i in range(grid_n_lat):
                    for j in range(grid_n_lon):
                            string = str(grid_X[i, j]) + ' ' + str(grid_Y[i, j]) + ' ' + str(gmi_config.GRID_ALT) + ' '
                            #print string
                            tessfile.write(string + '\n')

    return


def read_data_grid(filename):
    import numpy as np
    from scipy.interpolate import griddata

    import gmi_config
    gmi_config.read_config()

    try:
        data = np.loadtxt(filename, delimiter="\t")
    except ValueError:
        #warning(str(filename) + ' is suspected not to have a tabular delimiter, trying with a space delimiter')

        try:
            data = np.loadtxt(filename, delimiter=" ")

        except:
            error('CAN NOT READ ' + str(filename) + ' with space delimiter, abort!')
            exit(-1)


    factor = 1.0
    val_col = 2
    n_col = len(data[0, :])
    if n_col == 3:
        debug("xyz grid")

    elif n_col == 4:
        factor = -1.0
        val_col = 3
        debug("magtess output")
    else:
        error("WRONG NUMBER OF COLUMNS (" + str(n_col) + ") IN " + filename + ", ABORTING")


    LON = data[:, 0]
    LAT = data[:, 1]
    VAL = data[:, val_col] * factor

    step = gmi_config.GRID_STEP#abs(LON[1] - LON[0])

    #flip coord system to fit SHTOOLS convention
    for i in range(1, len(LON), 1):
        if LON[i]<0:
            LON[i] = 360+LON[i]

    min_lon = 0
    max_lon = 360
    min_lat = -90
    max_lat = 90

    n_lat = len(np.arange(min_lat, max_lat, step))
    n_lon = len(np.arange(min_lon, max_lon, step))

    lats = np.linspace(max_lat, min_lat, n_lat)
    lons = np.linspace(min_lon, max_lon, n_lon)

    X,Y = np.meshgrid(lons, lats)

    #in SHTOOLS format
    raw_grid = griddata((LON, LAT), VAL, (X,Y), method='nearest')

    return raw_grid


def subtract_tess_output_global_grids(filename1, filename2, output_filename):
    #NOT TESTED
    import numpy as np
    from scipy.interpolate import griddata

    import gmi_config
    gmi_config.read_config()

    data1 = np.loadtxt(filename1, delimiter=" ")
    LON = data1[:, 0]
    LAT = data1[:, 1]
    ALT = data1[:, 2]
    VAL1 = data1[:, 3]

    data2 = np.loadtxt(filename2, delimiter=" ")
    VAL2 = data2[:, 3]

    VAL = VAL1 - VAL2

    with open(output_filename, 'w') as ofile:
            for i in range(len(LON)):
                    ofile.write(str(LON[i]) + ' ' + str(LAT[i]) + ' ' + str(ALT[i]) + ' ' + str(VAL[i]) + '\n')

    return




def read_suscept_global_grid_from_file(filename):
    import numpy as np
    from scipy.interpolate import griddata

    import gmi_config
    gmi_config.read_config()

    try:
        data = np.loadtxt(filename, delimiter="\t")
    except ValueError:
        debug('WARNING! ' + str(filename) + ' is suspected not to have a tabular delimiter, trying with a space delimiter')

        try:
            data = np.loadtxt(filename, delimiter=" ")

        except:
            print('CON NOT READ ' + str(filename) + ' with space delimiter, abort!')
            exit(-1)


    LON = data[:, 0]
    LAT = data[:, 1]
    VAL = data[:, 2]

    n_lon, n_lat, X, Y = create_tess_cpoint_grid()

    #in SHTOOLS format
    sus_grid = griddata((LON, LAT), VAL, (X,Y), method='nearest')

    x_0 = np.zeros(n_lon*n_lat)
    ind = 0
    for i in range(n_lat-1, -1, -1):
        for j in range(n_lon):
            x_0[ind] = sus_grid[i, j]
            ind += 1

    return sus_grid




def remove_lw_sh_coeff(sh_coff, n_cutoff):
    import pyshtools
    shtools_zero_coeff = pyshtools.SHCoeffs.from_zeros(len(sh_coff.degrees())-1)
    shtools_zero_coeff = shtools_zero_coeff.convert('schmidt')
    shtools_zero_coeff.coeffs[:, n_cutoff:, :] = sh_coff.coeffs[:, n_cutoff:, :]
    return shtools_zero_coeff


def read_coeffs_from_text_file(shc_filename, n_cutoff):
    import numpy as np
    data = np.loadtxt(shc_filename, delimiter=",")

    #print data[:, 0]
    ind = np.where(data[:, 0] < n_cutoff)
    data[ind, 2] = np.zeros(len(ind))
    data[ind, 3] = np.zeros(len(ind))

    out = np.concatenate((data[:, 2], data[:, 3]))
    return out

def convert_result_into_shtools_format(vect, fname):
    import numpy as np

    try:
        shdata = np.loadtxt('model/tess_n0.coeff', delimiter=",")
    except:
        print ("CAN NOT OPEN model/tess_n0.coeff")
        exit(-1)

    half = len(shdata[:, 2])
    shdata[:, 2] = vect[0:half]
    shdata[:, 3] = vect[half:]

    with open(fname, 'w') as fresult:
        for i in range(half):
            fresult.write(str(int(shdata[i, 0])) + ', ' + str(int(shdata[i, 1])) + ', ' + str(float(shdata[i, 2])) + ', ' + str(float(shdata[i, 3])) + '\n')

    import pyshtools
    shtools_result_coeff = pyshtools.SHCoeffs.from_file(fname, normalization='schmidt')
    return shtools_result_coeff


def write_sus_grid_to_file(sus, fname):
    import numpy as np

    import gmi_config
    gmi_config.read_config()

    n_lon, n_lat, X, Y = create_tess_cpoint_grid()
    grid = X*0.0

    ind = 0
    with open(fname, 'w') as resfile:
        for i in range(n_lat-1, -1, -1):
            for j in range(n_lon):
                string = str(X[i, j]) + ' ' + str(Y[i, j]) + ' ' + str(sus[ind])
                grid[i, j] = sus[ind]

                resfile.write(string + '\n')
                ind = ind+1

    return X, Y, grid


def write_xyz_grid_to_file(x, y, z, fname):
    with open(fname, 'w') as resfile:
        for i in range(len(z)):
            string = str(x[i]) + ' ' + str(y[i]) + ' ' + str(z[i])
            resfile.write(string + '\n')

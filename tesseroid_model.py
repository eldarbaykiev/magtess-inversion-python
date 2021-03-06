

def _download_igrf():
    import wget
    import gmi_config

    url = "https://www.ngdc.noaa.gov/IAGA/vmod/geomag70_linux.tar.gz"

    wget.download(url, 'geomag70_linux.tar.gz')

    import tarfile

    tar = tarfile.open('geomag70_linux.tar.gz', "r:gz")
    tar.extractfile()
    tar.close()
	


def _create_tess_model_file(fname, suscept, x_grid, y_grid, z_topg, z_botg):
    import numpy as np
    import os

    import gmi_config
    gmi_config.read_config()

    import gmi_misc

    nlat, nlon = x_grid.shape

    if gmi_config.T_DO_TILES:
        width = gmi_config.T_WIDTH
        minlon = gmi_config.T_LON_MIN-gmi_config.T_EDGE_EXT
        maxlon = gmi_config.T_LON_MAX+gmi_config.T_EDGE_EXT

        minlat = gmi_config.T_LAT_MIN-gmi_config.T_EDGE_EXT
        maxlat = gmi_config.T_LAT_MAX+gmi_config.T_EDGE_EXT
    else:
        width = gmi_config.WIDTH
        minlon = gmi_config.LON_MIN
        maxlon = gmi_config.LON_MAX

        minlat = gmi_config.LAT_MIN
        maxlat = gmi_config.LAT_MAX

    with open(fname + '.tess', 'w') as tessfile:
        k = 0
        for i in range(nlat-1, -1, -1):
            for j in range(nlon):
                if isinstance(suscept, np.ndarray):
                    sus_curr = suscept[k]
                elif isinstance(suscept, float):
                    sus_curr = suscept
                else:
                    pass

                if gmi_misc.check_if_in_boundary(x_grid[i, j], y_grid[i, j], minlon, maxlon, minlat, maxlat):
                    string = str(x_grid[i, j]-width/2.0) + ' ' + str(x_grid[i, j]+width/2.0) + ' ' + str(y_grid[i, j]-width/2.0) + ' ' + str(y_grid[i, j]+width/2.0) + ' ' + str(z_topg[i, j]) + ' ' +  str(z_botg[i, j]) + ' 1.0 ' + str(sus_curr)
                    tessfile.write(string + '\n')

                k = k + 1

    if not os.path.isfile(gmi_config.IGRF_COEFF_FILENAME):
        gmi_misc.warning('main field SH model ' + gmi_config.IGRF_COEFF_FILENAME + ' is missing, downloading IGRF13 from https://www.ngdc.noaa.gov/IAGA/vmod/geomag70_linux.tar.gz as a substitute! Check your config file')
        _download_igrf()
        gmi_config.IGRF_COEFF_FILENAME = 'geomag70_linux/IGRF13.COF'

    os.system(gmi_config.TESSUTIL_MAGNETIZE_MODEL_FILENAME + ' ' + gmi_config.IGRF_COEFF_FILENAME + ' ' + fname + '.tess ' + str(gmi_config.IGRF_DAY) + ' ' + str(gmi_config.IGRF_MONTH) + ' ' + str(gmi_config.IGRF_YEAR) + ' ' + fname + '.magtess')

    if os.path.isfile(fname + '.tess'):
        gmi_misc.ok("Magnetic tesseroid model " + fname + '.tess' + " is created")
    else:
        gmi_misc.error("model.magtess WAS NOT CREATED, CHECK IF " + '\033[1m' + gmi_config.TESSUTIL_MAGNETIZE_MODEL_FILENAME + '\033[0m' + " IS WORKING PROPERLY")
		

	
	

def main(dr):
    #**************** TESTING PARAMS (WOULD BE REMOVED)*******#
    CREATE_VIM_MODEL = True
    #**************** ---------------------------------*******#

    import gmi_misc
    #**************** PRINT HEADER ***************************#
    gmi_misc.print_header()
    gmi_misc.message("Creation of a tesseroid model")
    #**************** ------------ ***************************#

    #**************** GET WORKING DIRECTORY ******************#
    import os
    old_cwd = os.getcwd()
    gmi_misc.info('Current directory: '+ old_cwd)

    try:
        os.chdir(dr)
    except:
        gmi_misc.error('CAN NOT OPEN WORKING DIRECTORY '+ dr + ', ABORTING...')

    gmi_misc.message('Working directory: '+ os.getcwd())
    #**************** --------------------- ******************#


    #**************** read parameters from file **************#
    import gmi_config
    gmi_config.read_config()
    #**************** ------------------------- **************#


    result_folder = gmi_misc.init_result_folder()

    import numpy as np

    n_lon, n_lat, X, Y = gmi_misc.create_tess_cpoint_grid()
    
    #*********************************************************#
    
    gmi_misc.message('Path to surfaces: '+ gmi_config.PATH_SURFACES)
    
    import glob, re
    surfaces_filenames = glob.glob(gmi_config.PATH_SURFACES + '/*')
    try:
        surfaces_filenames.sort(key=lambda f: int(re.sub('\D', '', f))) #good initial sort but doesnt sort numerically very well
        sorted(surfaces_filenames) #sort numerically in ascending order
    except:
        gmi_misc.error('CHECK FILENAMES IN LAYERS FOLDER - THERE SHOULD BE INTEGER NUMBERS IN FILENAMES TO INDICATE THE ORDER OF SURFACES')
        
    
    gmi_misc.message('All surfaces: ' + str(surfaces_filenames))
    
    for li,this_surf,next_surf in zip(range(len(surfaces_filenames)-1), surfaces_filenames[0:-1], surfaces_filenames[1:]):
        gmi_misc.message('Layer '+ str(li)+': upper surface ' + this_surf + ', lower surface: ' + next_surf)
        
        Z_bot = gmi_misc.read_surf_grid(next_surf)
        Z_top = gmi_misc.read_surf_grid(this_surf)
        
        if gmi_config.MULTIPLICATOR != 1.0:
            gmi_misc.warning("NOTE: SUSCEPTIBILITY OF EACH TESSEROID IS MULTIPLIED BY "+ str(gmi_config.MULTIPLICATOR))

        _create_tess_model_file('layer' + str(li), 1.0*gmi_config.MULTIPLICATOR, X, Y, Z_top, Z_bot)


    #**************** WRITE MD5 PARAMS **************#

    #/fix it
    '''
    import hashlib
    file_name = 'model.magtess'
    with open(file_name, 'r') as file_to_check:
        # read contents of the file
        data = file_to_check.read()
        # pipe contents of the file through
        md5_returned = hashlib.md5(data.encode('utf-8')).hexdigest()

    #Save
    dictionary = {'stage1':md5_returned,
            'stage2':'',
            'stage3':'',
            'stage4':'',
    }
    np.save('checksums.npy', dictionary)
    #**************** ---------------- **************#
    '''

    #**************** RETURN BACK TO INITIAL PATH ***#
    os.chdir(old_cwd)

    #**************** --------------------------- ***#


if __name__ == '__main__':
    #**************** GET WORKING DIRECTORY ******************#

    WORKING_DIR = ''
    import sys
    if len(sys.argv) == 1:
            WORKING_DIR = ''

    WORKING_DIR = sys.argv[1]

    #**************** --------------------- ******************#
    main(WORKING_DIR)

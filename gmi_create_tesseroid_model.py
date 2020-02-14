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

                string = str(x_grid[i, j]-gmi_config.WIDTH/2.0) + ' ' + str(x_grid[i, j]+gmi_config.WIDTH/2.0) + ' ' + str(y_grid[i, j]-gmi_config.WIDTH/2.0) + ' ' + str(y_grid[i, j]+gmi_config.WIDTH/2.0) + ' ' + str(z_topg[i, j]) + ' ' +  str(z_botg[i, j]) + ' 1.0 ' + str(sus_curr)
                tessfile.write(string + '\n')
                k = k + 1

	if not os.path.isfile(gmi_config.IGRF_COEFF_FILENAME):
		gmi_misc.warning('main field SH model ' + gmi_config.IGRF_COEFF_FILENAME + ' is missing, downloading IGRF13 from https://www.ngdc.noaa.gov/IAGA/vmod/geomag70_linux.tar.gz as a substitute! Check your config file')
		_download_igrf()
		gmi_config.IGRF_COEFF_FILENAME = 'geomag70_linux/IGRF13.COF'

    os.system(gmi_config.TESSUTIL_MAGNETIZE_MODEL_FILENAME + ' ' + gmi_config.IGRF_COEFF_FILENAME + ' ' + fname + '.tess ' + str(gmi_config.IGRF_DAY) + ' ' + str(gmi_config.IGRF_MONTH) + ' ' + str(gmi_config.IGRF_YEAR) + ' ' + fname + '.magtess')

    if os.path.isfile(fname + '.tess'):
        gmi_misc.ok("Magnetic tesseroid model " + '\033[1m' + fname + '.tess' + '\033[0m' + " is created")
    else:
        gmi_misc.error("model.magtess WAS NOT CREATED, CHECK IF " + '\033[1m' + gmi_config.TESSUTIL_MAGNETIZE_MODEL_FILENAME + '\033[0m' + " IS WORKING PROPERLY")
		

	
	

def main(dr):
    #**************** TESTING PARAMS (WOULD BE REMOVED)*******#
    CREATE_VIM_MODEL = True
    #**************** ---------------------------------*******#

    import gmi_misc
    #**************** PRINT HEADER ***************************#
    gmi_misc.print_header()
    print ("Script no. 1: Creation of global tesseroid model")
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

    Z_bot = gmi_misc.read_surf_grid(gmi_config.BOT_SURFACE)
    Z_top = gmi_misc.read_surf_grid(gmi_config.TOP_SURFACE)

    if gmi_config.MULTIPLICATOR != 1.0:
        gmi_misc.warning("NOTE: SUSCEPTIBILITY OF EACH TESSEROID IS MULTIPLIED BY "+ str(gmi_config.MULTIPLICATOR))

    _create_tess_model_file('model', 1.0*gmi_config.MULTIPLICATOR, X, Y, Z_top, Z_bot)

    if CREATE_VIM_MODEL:
        if ('.vim' in gmi_config.INIT_SOLUTION) or ('.vis' in gmi_config.INIT_SOLUTION):
            sus_grid = gmi_misc.read_sus_grid(gmi_config.INIT_SOLUTION)
            dm1, dm2, x0 = gmi_misc.convert_surf_grid_to_xyz(sus_grid)

            _create_tess_model_file(result_folder + '/model_with_x0', x0, X, Y, Z_top, Z_bot)
            _create_tess_model_file(result_folder + '/model_with_x0_mult', x0*gmi_config.MULTIPLICATOR, X, Y, Z_top, Z_bot)
            np.savetxt(result_folder + '/init_solution.x0', x0)
            gmi_misc.write_sus_grid_to_file(x0, result_folder + 'init_solution.xyz')


    #**************** WRITE MD5 PARAMS **************#

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

def main(dr):

    import gmi_misc
    #**************** PRINT HEADER ***************************#
    gmi_misc.print_header()
    print("Grid reading test")
    #**************** ------------ ***************************#


    #**************** GET WORKING DIRECTORY ******************#
    import os
    old_cwd = os.getcwd()
    gmi_misc.info('Current directory: '+ old_cwd)

    try:
        os.chdir(dr)
    except:
        gmi_misc.error('CAN NOT OPEN WORKING DIRECTORY '+ dr + ', ABORTING...')

    gmi_misc.info('WORKING DIRECTORY: '+ os.getcwd())
    #**************** --------------------- ******************#


    #**************** read parameters from file **************#
    import gmi_config
    gmi_config.read_config()
    #**************** ------------------------- **************#


    #BODY*****************************************************#
    import matplotlib.pyplot as plt
    import pyshtools

    import numpy as np
    from scipy.interpolate import griddata

    #read design matrices
    try:
        A = np.load('design_matrix_shcoeff.npy')
        A = np.transpose(A)

    except:
        print("CAN NOT OPEN SH COEFF DESIGN MATRIX")
        exit(-1)

    #read initial solution
    sus_grid = gmi_misc.read_sus_grid(gmi_config.INIT_SOLUTION)
    dm1, dm2, x0 = gmi_misc.convert_surf_grid_to_xyz(sus_grid)

    obs_matmul = np.matmul(A, x0)

    #read PRECALCULATED observed grid all degrees
    try:
        raw_grid = gmi_misc.read_data_grid(gmi_config.OBSERVED_DATA)
    except IOError as err:
        print("CAN NOT OPEN OBSERVED DATAFILE: {0}".format(err))
        exit(-1)

    shtools_inp_grid = pyshtools.SHGrid.from_array(raw_grid)

    sht_obs_tessfc_alldegrees = shtools_inp_grid.expand(normalization='schmidt')
    sht_obs_tessfc = gmi_misc.remove_lw_sh_coeff(sht_obs_tessfc_alldegrees, gmi_config.N_MIN_CUTOFF)
    sht_obs_tessfc.to_file("test_sht_obs_tessfc.coeff")

    obs_tessfc = gmi_misc.read_coeffs_from_text_file("test_sht_obs_tessfc.coeff", gmi_config.N_MIN_CUTOFF)
    obs_diff = (obs_matmul - obs_tessfc)
    print (obs_diff)
    print (np.linalg.norm(obs_diff))



    #*********************************************************#


    #**************** RETURN BACK TO INITIAL PATH ***#
    os.chdir(old_cwd)
    #**************** --------------------------- ***#


if __name__ == '__main__':
    #**************** GET WORKING DIRECTORY ******************#
    '''
    WORKING_DIR = ''
    import sys
    if len(sys.argv) == 1:
            WORKING_DIR = ''

    WORKING_DIR = sys.argv[1]
    '''
    #**************** --------------------- ******************#
    #main('/Volumes/Seagate Backup Plus Drive 1/workspace_nomult_gmi')
    main('/Volumes/Seagate Backup Plus Drive 1/workspace1_gmi')

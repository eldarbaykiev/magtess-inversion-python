def main(dr):
    import gmi_misc
    #**************** PRINT HEADER ***************************#
    gmi_misc.print_header()
    print("Script no. 4: Inversion")
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



    #************ check if previous stages were launched *****#
    '''
    import gmi_hash
    stages = [0,0,0]
    stages, dictionary = gmi_hash.read_dict('checksums.npy')


    err = 0
    if stages[0] == -1:
            gmi_misc.warning('model.magtess was changed after the run of Script 1, restart Script no. 1 first! ABORTING...')
            err += 1
    elif stages[0] == 0:
            gmi_misc.warning('model.magtess was changed after the run of Script 1, restart Script no. 1 first! ABORTING...')
            err += 1
    else:
            pass

    if stages[1] == -1:
            gmi_misc.warning('Folder model was changed after the run of Script 2, restart Script no. 2 first! ABORTING...')
            err += 1
    elif stages[1] == 0:
            gmi_misc.warning('Folder model was changed after the run of Script 2, restart Script no. 2 first! ABORTING...')
            err += 1
    else:
            pass

    if stages[2] == -1:
            gmi_misc.warning('Design matrix was changed after the run of Script 3, restart Script no. 3 first! ABORTING...')
            err += 1
    elif stages[2] == 0:
            gmi_misc.warning('Design matrix was changed after the run of Script 3, restart Script no. 3 first! ABORTING...')
            err += 1
    else:
            pass

    if err > 0:
            gmi_misc.error('CHECKSUM FAILED, ABORTING!')
    '''
    #**************** --------------------- ******************#


    import matplotlib.pyplot as plt
    import pyshtools

    import numpy as np
    from scipy.interpolate import griddata


    gmi_misc.warning("INPUT GRID IS MULTIPLIED BY "+ str(gmi_config.MULTIPLICATOR))

    ##READ DESIGN MATRIX

    A = np.load('design_matrix_shcoeff.npy')
    #A_alldeg = np.load('design_matrix_ufilt_shcoeff.npy')

    import scipy.io
    A = np.transpose(A)
    #A_alldeg = np.transpose(A_alldeg)

    ##READ INITIAL SOLUTION
    #read initial solution
    sus_grid = gmi_misc.read_sus_grid(gmi_config.INIT_SOLUTION)
    dm1, dm2, x0 = gmi_misc.convert_surf_grid_to_xyz(sus_grid)


    d_ideal = np.matmul(A, x0)

    ##READ OBSERVED GRID
    obs_grid = gmi_misc.read_data_grid(gmi_config.OBSERVED_DATA) #* gmi_config.MULTIPLICATOR


    ##READ SUBTRACTABLE FIELD
    try:
        sub_grid = gmi_misc.read_data_grid(gmi_config.SUBTRACT_DATA) * gmi_config.MULTIPLICATOR
    except IOError as err:
        print("CAN NOT OPEN SUBTRACTEBLE DATAFILE: {0}".format(err))
        sub_grid = obs_grid*0.0

    ##REMOVE SUBTRACTABLE FIELD
    obs_grid = obs_grid - sub_grid

    ##CONVERT OBSERVED GRID INTO SHCOEFF
    obs_sht_grid = pyshtools.SHGrid.from_array(obs_grid)
    obs_sht_shcoeff = obs_sht_grid.expand(normalization='schmidt')

    obs_sht_shcoeff_trunc = gmi_misc.remove_lw_sh_coeff(obs_sht_shcoeff, gmi_config.N_MIN_CUTOFF)
    obs_sht_shcoeff_trunc.to_file("obs_sht_shcoeff_trunc.coeff")

    d = gmi_misc.read_coeffs_from_text_file("obs_sht_shcoeff_trunc.coeff", gmi_config.N_MIN_CUTOFF)
    n_coeff = len(d)

    #SOLVING
    import gmi_inv_methods

    print ("d_ideal (np.matmul(A, x0)):" + str(d_ideal))
    print ("d (from magtess calculated grid):" + str(d))
    print ("|d_ideal - d| = " + str(np.linalg.norm(d_ideal - d)))

    h = gmi_inv_methods.Projected_Gradient(A, d, x0)

    print ("x0:" + str(x0))
    print ("h:" + str(h))
    print ("|x0 - h| = " + str(np.linalg.norm(x0 - h)))

    d_res = np.matmul(A, h)

    ######################

    gmi_misc.write_sus_grid_to_file(h, 'res.xyz')
    gmi_misc.write_sus_grid_to_file(x0 - h, 'x0-res.xyz', )
    gmi_misc.write_sus_grid_to_file(x0, 'x0.xyz')


    #save result
    result_folder = gmi_misc.init_result_folder()

    import shutil
    shutil.copyfile('input.txt', './' + result_folder + '/' + 'input.txt')
    shutil.copyfile('x0-res.xyz', './' + result_folder + '/' + 'x0-res.xyz')
    shutil.copyfile('x0.xyz', './' + result_folder + '/' + 'x0.xyz')
    shutil.copyfile('res.xyz', './' + result_folder + '/' + 'res.xyz')
    shutil.copyfile('nlssubprob.dat', './' + result_folder + '/' + 'nlssubprob.dat')

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

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

    import convert_shtools_grids


    gmi_misc.warning("INPUT GRID IS MULTIPLIED BY "+ str(gmi_config.MULTIPLICATOR))

    ##READ DESIGN MATRIX

    A = np.load('design_matrix_shcoeff.npy')
    A_alldeg = np.load('design_matrix_ufilt_shcoeff.npy')

    import scipy.io
    A = np.transpose(A)
    A_alldeg = np.transpose(A_alldeg)

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

    def _save_powerspectrum(specname, shc):
        spectrum = shc.spectrum()
        deg = shc.degrees()
        with open(specname, 'w') as f:
            for i in range(len(deg)):
                f.write(str(deg[i]) + ' ' + str(spectrum[i]) + '\n')

    ##CONVERT OBSERVED GRID INTO SHCOEFF
    obs_sht_grid = pyshtools.SHGrid.from_array(obs_grid)
    obs_sht_shcoeff = obs_sht_grid.expand(normalization='schmidt')
    obs_sht_shcoeff.to_file("obs_sht_shcoeff.sht_shcoeff")

    ##save unfiltered input grid
    obs_sht_grid = obs_sht_shcoeff.expand(grid='DH2')
    glon, glat, gval = convert_shtools_grids.convert_sht_grid_to_xyz(obs_sht_grid.to_array())
    gmi_misc.write_xyz_grid_to_file(glon, glat, gval, 'obs_grid.xyz')
    _save_powerspectrum('obs_sht_shcoeff.spec', obs_sht_shcoeff)

    ##FILTER OBSERVED GRID INTO SHCOEFF
    obs_sht_shcoeff_trunc = gmi_misc.remove_lw_sh_coeff(obs_sht_shcoeff, gmi_config.N_MIN_CUTOFF)
    obs_sht_shcoeff_trunc.to_file("obs_sht_shcoeff_trunc.sht_shcoeff")

    ##save filtered input grid
    obs_sht_grid_filt = obs_sht_shcoeff_trunc.expand(grid='DH2')
    glon, glat, gval = convert_shtools_grids.convert_sht_grid_to_xyz(obs_sht_grid_filt.to_array())
    gmi_misc.write_xyz_grid_to_file(glon, glat, gval, 'obs_grid_filt.xyz')
    _save_powerspectrum('obs_sht_shcoeff_trunc.spec', obs_sht_shcoeff_trunc)

    d = gmi_misc.read_coeffs_from_text_file("obs_sht_shcoeff_trunc.sht_shcoeff", gmi_config.N_MIN_CUTOFF)
    n_coeff = len(d)

    #SOLVING
    import gmi_inv_methods

    print ("d_ideal (np.matmul(A, x0)) = " + str(d_ideal))
    print ("d = " + str(d))
    print ("|d_ideal - d| = " + str(np.linalg.norm(d_ideal - d)))

    h = gmi_inv_methods.Projected_Gradient(A, d, x0)

    print ("x0 = " + str(x0))
    print ("h = " + str(h))
    print ("|x0 - h| = " + str(np.linalg.norm(x0 - h)))

    d_res = np.matmul(A_alldeg, h)

    res_sht_shcoeff = gmi_misc.convert_result_into_shtools_format(d_res, 'res_sht_shcoeff.sht_shcoeff')

    res_sht_grid = res_sht_shcoeff.expand(grid='DH2')
    glon, glat, gval = convert_shtools_grids.convert_sht_grid_to_xyz(res_sht_grid.to_array())
    gmi_misc.write_xyz_grid_to_file(glon, glat, gval, 'res_grid.xyz')
    _save_powerspectrum('res_sht_shcoeff.spec', res_sht_shcoeff)

    res_sht_shcoeff_trunc = gmi_misc.remove_lw_sh_coeff(res_sht_shcoeff, gmi_config.N_MIN_CUTOFF)
    res_sht_shcoeff_trunc.to_file("res_sht_shcoeff_trunc.sht_shcoeff")

    res_sht_grid_filt = res_sht_shcoeff_trunc.expand(grid='DH2')
    glon, glat, gval = convert_shtools_grids.convert_sht_grid_to_xyz(res_sht_grid_filt.to_array())
    gmi_misc.write_xyz_grid_to_file(glon, glat, gval, 'res_grid_filt.xyz')
    _save_powerspectrum('res_sht_shcoeff_trunc.spec', res_sht_shcoeff_trunc)

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

    shutil.copyfile('obs_grid_filt.xyz', './' + result_folder + '/' + 'obs_grid_filt.xyz')
    shutil.copyfile('obs_sht_shcoeff_trunc.spec', './' + result_folder + '/' + 'obs_sht_shcoeff_trunc.spec')
    shutil.copyfile('obs_sht_shcoeff_trunc.sht_shcoeff', './' + result_folder + '/' + 'obs_sht_shcoeff_trunc.sht_shcoeff')

    shutil.copyfile('obs_grid.xyz', './' + result_folder + '/' + 'obs_grid.xyz')
    shutil.copyfile('obs_sht_shcoeff.spec', './' + result_folder + '/' + 'obs_sht_shcoeff.spec')
    shutil.copyfile('obs_sht_shcoeff.sht_shcoeff', './' + result_folder + '/' + 'obs_sht_shcoeff.sht_shcoeff')

    shutil.copyfile('res_grid_filt.xyz', './' + result_folder + '/' + 'res_grid_filt.xyz')
    shutil.copyfile('res_sht_shcoeff_trunc.spec', './' + result_folder + '/' + 'res_sht_shcoeff_trunc.spec')
    shutil.copyfile('res_sht_shcoeff_trunc.sht_shcoeff', './' + result_folder + '/' + 'res_sht_shcoeff_trunc.sht_shcoeff')

    shutil.copyfile('res_grid.xyz', './' + result_folder + '/' + 'res_grid.xyz')
    shutil.copyfile('res_sht_shcoeff.spec', './' + result_folder + '/' + 'res_sht_shcoeff.spec')
    shutil.copyfile('res_sht_shcoeff.sht_shcoeff', './' + result_folder + '/' + 'res_sht_shcoeff.sht_shcoeff')


    shutil.copyfile('nlssubprob.dat', './' + result_folder + '/' + 'nlssubprob.dat')

    try:
        shutil.copyfile('video_log.mp4', './' + result_folder + '/' + 'video_log.mp4')
    except:
        print('could not cave video')


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

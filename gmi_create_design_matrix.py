def main(dr):

    #**************** TESTING PARAMS (WOULD BE REMOVED)*******#
    TRUNCATE = True
    #**************** ---------------------------------*******#



    import gmi_misc
    #**************** PRINT HEADER ***************************#
    gmi_misc.print_header()
    print ("Script no. 3: Creation of design matrices")
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
    import gmi_hash
    stages = [0,0,0]
    stages, dictionary = gmi_hash.read_dict('checksums.npy')

    if __name__ == '__main__':
        err = 0
        if stages[0] == -1:
            err += 1
            gmi_misc.warning('model.magtess was changed after the run of Script 1, restart Script no. 1 first! ABORTING...')
        elif stages[0] == 0:
            err += 1
            gmi_misc.warning('model.magtess was changed after the run of Script 1, restart Script no. 1 first! ABORTING...')
        else:
            pass

        if stages[1] == -1:
            err += 1
            gmi_misc.warning('Folder model was changed after the run of Script 2, restart Script no. 2 first! ABORTING...')
        elif stages[1] == 0:
            err += 1
            gmi_misc.warning('Folder model was changed after the run of Script 2, restart Script no. 2 first! ABORTING...')
        else:
            pass

        if err > 0:
            gmi_misc.error('CHECKSUM FAILED, ABORTING!')

    #**************** --------------------- ******************#



    #**************** CREATE DESIGN MATRICES *****************#
    import os
    import glob

    os.chdir('model')
    coefflist = glob.glob("*.coeff")
    os.chdir('..')

    n_tess = len(coefflist)
    if n_tess == 0:
        gmi_misc.error("NO CALCULATED SH MODELS OF EACH TESSEROID'S MAGNETIC FIELD")
        exit(-1)

    if gmi_config.MULTIPLICATOR != 1.0:
        gmi_misc.warning("NOTE: SUSCEPTIBILITY OF EACH TESSEROID IS MULTIPLIED BY "+ str(gmi_config.MULTIPLICATOR))

    import pyshtools
    import numpy as np

    coeff_filename = 'model/tess_n' + str(0) + '.coeff'

    b = gmi_misc.read_coeffs_from_text_file(coeff_filename, gmi_config.N_MIN_CUTOFF)
    n_vals = len(b)

    gmi_misc.message('Assemblying design matrices...')
    from tqdm import tqdm
    A = np.zeros((n_tess, n_vals))
    A_ufilt = np.zeros((n_tess, n_vals))





    #if __name__ == '__main__':
    for i in tqdm(range(n_tess)):
        coeff_filename = 'model/tess_n' + str(i) + '.coeff'

        b = gmi_misc.read_coeffs_from_text_file(coeff_filename, gmi_config.N_MIN_CUTOFF)
        b_ufilt = gmi_misc.read_coeffs_from_text_file(coeff_filename, 0)
        A[i, :] = b[:]
        A_ufilt[i, :] = b_ufilt[:]
    '''
    else:
        from PyQt5 import QtWidgets

        app = QtWidgets.QApplication.instance()
        if app is None:
            # if it does not exist then a QApplication is created
            app = QtWidgets.QApplication([])

        from progress_bar import ProgressBar
        pb = ProgressBar()

        for i in range(n_tess):
            coeff_filename = 'model/tess_n' + str(i) + '.coeff'

            b = gmi_misc.read_coeffs_from_text_file(coeff_filename, gmi_config.N_MIN_CUTOFF)
            b_ufilt = gmi_misc.read_coeffs_from_text_file(coeff_filename, 0)
            A[i, :] = b[:]
            A_ufilt[i, :] = b_ufilt[:]

            pb.setValue(((i + 1) / n_tess) * 100)
            app.processEvents()

        pb.close()
    '''

    gmi_misc.ok('...done')

    #**************** SAVE MATRICES *****************#

    np.save('design_matrix_shcoeff', A)
    np.save('design_matrix_ufilt_shcoeff', A_ufilt)

    #**************** ------------- *****************#



    #**************** WRITE MD5 PARAMS **************#
    import hashlib
    SHAhash = hashlib.md5()

    f1 = open('design_matrix_shcoeff.npy', 'rb')
    while 1:
        # Read file in as little chunks
        buf = f1.read(4096)
        if not buf : break
        SHAhash.update(hashlib.md5(buf).hexdigest().encode('utf-8'))
    f1.close()


    f2 = open('design_matrix_ufilt_shcoeff.npy', 'rb')
    while 1:
        # Read file in as little chunks
        buf = f2.read(4096)
        if not buf : break
        SHAhash.update(hashlib.md5(buf).hexdigest().encode('utf-8'))
    f2.close()

    dictionary['stage3'] = SHAhash.hexdigest()
    dictionary['stage4'] = ''
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

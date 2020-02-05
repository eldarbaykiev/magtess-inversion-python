
def main(dr, tc=True):
    import gmi_misc

    import os
    old_cwd = os.getcwd()
    gmi_misc.info('Current directory: '+ old_cwd)

    try:
            os.chdir(dr)
    except:
            gmi_misc.error('CAN NOT OPEN WORKING DIRECTORY '+ dr + ', ABORTING...')

    gmi_misc.info('WORKING DIRECTORY: '+ os.getcwd())



    print ("HASH TEST")

    import gmi_config
    gmi_config.read_config()


    #**************** HASH TESTS    **************************#
    import gmi_hash

    stages = [0, 0, 0]
    stages, dict = gmi_hash.read_dict('checksums.npy', runcheck=tc)
    #**************** ----------    **************************#


    os.chdir(old_cwd)
    return stages, dict




if __name__ == '__main__':
    #**************** GET WORKING DIRECTORY ******************#

    WORKING_DIR = ''
    import sys
    if len(sys.argv) == 1:
            WORKING_DIR = ''

    WORKING_DIR = sys.argv[1]

    #**************** --------------------- ******************#
    main(WORKING_DIR)

import gmi_misc
#**************** PRINT HEADER ***************************#
gmi_misc.print_header()
print("Grid reading test")
#**************** ------------ ***************************#

#**************** GET WORKING DIRECTORY ******************#
import os
old_cwd = os.getcwd()
gmi_misc.info('Current directory: '+ old_cwd)

WORKING_DIR = ''
import sys
if len(sys.argv) == 1:
    WORKING_DIR = ''

WORKING_DIR = sys.argv[1]

try:
    os.chdir(WORKING_DIR)
except:
    gmi_misc.error('CAN NOT OPEN WORKING DIRECTORY '+ WORKING_DIR + ', ABORTING...')

gmi_misc.info('WORKING DIRECTORY: '+ os.getcwd())
#**************** --------------------- ******************#


#**************** read parameters from file **************#
import gmi_config
gmi_config.read_config()
#**************** ------------------------- **************#


#BODY*****************************************************#






#*********************************************************#


#**************** RETURN BACK TO INITIAL PATH ***#
os.chdir(old_cwd)
#**************** --------------------------- ***#

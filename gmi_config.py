import gmi_misc

#
PROJECT_NAME = ''

#Global Tesseroid Model
LON_MIN = 0
LON_MAX = 0
LAT_MIN = 0
LAT_MAX = 0
WIDTH = 0

TOP_SURFACE = ""
BOT_SURFACE = ""

MULTILAYER = False
PATH_SURFACES = ""

IGRF_DAY = 0
IGRF_MONTH = 0
IGRF_YEAR = 0
IGRF_COEFF_FILENAME = ""

#Global Grid
GRID_LON_MIN = 0
GRID_LON_MAX = 0
GRID_LAT_MIN = 0
GRID_LAT_MAX = 0

GRID_ALT = 0
GRID_STEP = 0

#Spherical Harmonics
N_MIN_CUTOFF = 0

#Inversion
OBSERVED_DATA = ""
SUBTRACT_DATA = ""
INIT_SOLUTION = ""
MAX_ITER = 100000
MULTIPLICATOR = 100000.0

#Tiles
T_DO_TILES = False
T_LON_MIN = 0
T_LON_MAX = 0
T_LAT_MIN = 0
T_LAT_MAX = 0
T_WIDTH = 0
T_EDGE_EXT = 0
T_GRID_STEP = 0

#
TESSUTIL_MAGNETIZE_MODEL_FILENAME  = 'tessutil_magnetize_model'
TESSBZ_FILENAME = 'tessbz'

def create_empty_config():
    import configparser
    config = configparser.ConfigParser()

    config['Name'] = {'PROJECT_NAME': 'project_name'}

    #Global Tesseroid Model
    config['Global Tesseroid Model'] = {'LON_MIN' : -180,
                                        'LON_MAX' : 180,
                                        'LAT_MIN' : -90,
                                        'LAT_MAX' : 90,
                                        'WIDTH' : 2.0,

                                        'TOP_SURFACE' : '',
                                        'BOT_SURFACE' : '',
                                        'PATH_SURFACES' : '',

                                        'IGRF_DAY' : 1,
                                        'IGRF_MONTH' : 1,
                                        'IGRF_YEAR' : 2014,
                                        'IGRF_COEFF_FILENAME' : 'IGRF12.COF'}

    config['Global Grid'] = {'GRID_LON_MIN' : -180,
                             'GRID_LON_MAX' : 180,
                             'GRID_LAT_MIN' : -90,
                             'GRID_LAT_MAX' : 90,

                             'GRID_ALT' : 400000,
                             'GRID_STEP': 2.0}

    config['Spherical Harmonics'] = {'N_MIN_CUTOFF' : 16}

    config['Inversion'] = {'OBSERVED_DATA' : '',
                           'SUBTRACT_DATA' : '',
                           'INIT_SOLUTION' : '',
                           'MAX_ITER' : 100,
                           'MULTIPLICATOR' : 1.0}

    with open('input.txt', 'w') as configfile:
            config.write(configfile)


def read_config():
    import os
    import gmi_misc
    #gmi_misc.debug('Reading config file ' + os.path.abspath("mydir/myfile.txt"))

    import sys
    this = sys.modules[__name__]

    import configparser
    config = configparser.ConfigParser()

    try:
        config.readfp(open(r'input.txt'))
    except:
        gmi_misc.warning('no input.txt file in the directory, creating an empty one...')
        create_empty_config()
        config.readfp(open(r'input.txt'))
        
    #get project name
    try:
        this.PROJECT_NAME = str(config.get('Name', 'PROJECT_NAME'))
    except:
        gmi_misc.error('Necessary parameters in input.txt are missing! ABORTING') 


    try:
        this.MULTILAYER = True
        this.PATH_SURFACES = config.get('Global Tesseroid Model', 'PATH_SURFACES')
    except:
        gmi_misc.debug('Path to the list of surfaces in input.txt is missing! ABORTING')
        this.MULTILAYER = False
       

    if (this.MULTILAYER == False):
        try:
            this.TOP_SURFACE = config.get('Global Tesseroid Model', 'TOP_SURFACE')
            this.BOT_SURFACE = config.get('Global Tesseroid Model', 'BOT_SURFACE')
                
        except:
            gmi_misc.error('Necessary parameters in input.txt are missing! ABORTING')    
        

    try:
        #Global Tesseroid Model
        this.LON_MIN = float(config.get('Global Tesseroid Model', 'LON_MIN'))
        this.LON_MAX = float(config.get('Global Tesseroid Model', 'LON_MAX'))
        this.LAT_MIN = float(config.get('Global Tesseroid Model', 'LAT_MIN'))
        this.LAT_MAX = float(config.get('Global Tesseroid Model', 'LAT_MAX'))
        this.WIDTH = float(config.get('Global Tesseroid Model', 'WIDTH'))

        

        this.IGRF_DAY = int(config.get('Global Tesseroid Model', 'IGRF_DAY'))
        this.IGRF_MONTH = int(config.get('Global Tesseroid Model', 'IGRF_MONTH'))
        this.IGRF_YEAR = int(config.get('Global Tesseroid Model', 'IGRF_YEAR'))
        this.IGRF_COEFF_FILENAME = config.get('Global Tesseroid Model', 'IGRF_COEFF_FILENAME')

        #Global Grid
        this.GRID_LON_MIN = float(config.get('Global Grid', 'GRID_LON_MIN'))
        this.GRID_LON_MAX = float(config.get('Global Grid', 'GRID_LON_MAX'))
        this.GRID_LAT_MIN = float(config.get('Global Grid', 'GRID_LAT_MIN'))
        this.GRID_LAT_MAX = float(config.get('Global Grid', 'GRID_LAT_MAX'))

        this.GRID_ALT = float(config.get('Global Grid', 'GRID_ALT'))
        this.GRID_STEP = float(config.get('Global Grid', 'GRID_STEP'))

        #Spherical Harmonics
        this.N_MIN_CUTOFF = int(config.get('Spherical Harmonics', 'N_MIN_CUTOFF'))

        #Inversion
        this.OBSERVED_DATA = config.get('Inversion', 'OBSERVED_DATA')
        this.SUBTRACT_DATA = config.get('Inversion', 'SUBTRACT_DATA')
        this.INIT_SOLUTION = config.get('Inversion', 'INIT_SOLUTION')
        this.MAX_ITER = int(config.get('Inversion', 'MAX_ITER'))
        this.MULTIPLICATOR = float(config.get('Inversion', 'MULTIPLICATOR'))
    except:
        gmi_misc.error('Necessary parameters in input.txt are missing! ABORTING')
        

    try:
        #Tiles
        this.T_DO_TILES = True

        this.T_LON_MIN = float(config.get('Tiles', 'T_LON_MIN'))
        this.T_LON_MAX = float(config.get('Tiles', 'T_LON_MAX'))
        this.T_LAT_MIN = float(config.get('Tiles', 'T_LAT_MIN'))
        this.T_LAT_MAX = float(config.get('Tiles', 'T_LAT_MAX'))
        this.T_WIDTH = float(config.get('Tiles', 'T_WIDTH'))
        this.T_EDGE_EXT = float(config.get('Tiles', 'T_EDGE_EXT'))
        this.T_GRID_STEP = float(config.get('Tiles', 'T_GRID_STEP'))

    except:
        gmi_misc.debug('Tile inversion parameters are missing in input.txt')
        this.T_DO_TILES = False




    import platform
    import os
    oper_system = platform.system()

    this.TESSUTIL_MAGNETIZE_MODEL_FILENAME = './tessutil_magnetize_model'
    if os.path.isfile(this.TESSUTIL_MAGNETIZE_MODEL_FILENAME) == False:
        gmi_misc.error("CAN NOT FIND " + this.TESSUTIL_MAGNETIZE_MODEL_FILENAME)

    this.TESSBZ_FILENAME = './tessbz'
    if os.path.isfile(this.TESSBZ_FILENAME) == False:
        gmi_misc.error("CAN NOT FIND " + this.TESSBZ_FILENAME)

    return config

    #print "                     ...done"

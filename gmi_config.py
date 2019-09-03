#Global Tesseroid Model
LON_MIN = 0
LON_MAX = 0
LAT_MIN = 0
LAT_MAX = 0
WIDTH = 0

TOP_SURFACE = ""
BOT_SURFACE = ""

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

def read_config():
	#print "Reading config file..."
	import sys
	this = sys.modules[__name__]

	import ConfigParser
	config = ConfigParser.ConfigParser()

	try:
		config.readfp(open(r'input.txt'))

		#Global Tesseroid Model
		this.LON_MIN = float(config.get('Global Tesseroid Model', 'LON_MIN'))
		this.LON_MAX = float(config.get('Global Tesseroid Model', 'LON_MAX'))
		this.LAT_MIN = float(config.get('Global Tesseroid Model', 'LAT_MIN'))
		this.LAT_MAX = float(config.get('Global Tesseroid Model', 'LAT_MAX'))
		this.WIDTH = float(config.get('Global Tesseroid Model', 'WIDTH'))

		this.TOP_SURFACE = config.get('Global Tesseroid Model', 'TOP_SURFACE')
		this.BOT_SURFACE = config.get('Global Tesseroid Model', 'BOT_SURFACE')

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

	except ValueError as err:
		print ("MISTAKE IN THE INPUT FILE: {0}".format(err))
		exit(-1)
	except IOError:
		print ("CAN NOT OPEN INPUT FILE")
		exit(-1)

	#print "                     ...done"

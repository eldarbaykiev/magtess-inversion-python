# Magnetic Tesseroid Inversion
Program for global magnetic tesseroid inversion

## Installation

Download the distibution archive (https://github.com/eldarbaykiev/magtess-inversion-python/archive/master.zip) to your computer and unpack it into a folder (for example `~/magtess-inversion-python`). 

### Linux (Ubuntu)

1. Install all necessary packages (**Python 3** with packages, **GMT**, **ffmpeg**):
```
apt install python3
apt install python3-pip
python3 -m pip install --upgrade pip

python3 -m pip install scipy
python3 -m pip install matplotlib
python3 -m pip install tqdm

apt install ffmpeg
apt install gmt gmt-dcw gmt-gshhg
```

If you have older **Ubuntu** (<=18.04), just install **PyQT5**:
```
python3 -m pip install pyqt5
```
If you have latest **Ubuntu** 19.10, there is a bug in **PyQT5** isntallation. Try to execute this:
```
apt install python3-widgetsnbextension
apt install python3-testresources
python3 -m pip install --upgrade setuptools
python3 -m pip install pyqt5==5.14
```
or look up for solutions on the internet to install **PyQT5** without errors.

2. Check if **PyQT5**, **SciPy**, **MatPlotLib** and **tqdm** are importable in **Python 3** environment. If they are not, try to reinstall these packages through **apt** or running **pip** as administator
```
sudo python3 -m pip install [packagename]
```

3. Run code
```
cd magtess-inversion-python
python3 gmi_gui.py
```

### macOS
1. In **macOS**, first install [iTerm2](https://iterm2.com). Within **iTerm2** terminal install [brew](https://brew.sh) with command:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew update && brew upgrade
```

Than install **zsh** with command :
```
brew install zsh
```

Make **zsh** a default shell in **iTerm2** by clicking iTerm2 -> Profiles -> Command: /bin/zsh.

Restart **iTerm2** and install [Oh My Zsh](https://ohmyz.sh) with command:
```
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

2. Install **Python 3** and other packages and programs:
```
brew install python3
pip3 install --upgrade pip

python3 -m pip install --upgrade pip

python3 -m pip install scipy
python3 -m pip install matplotlib
python3 -m pip install tqdm

python3 -m pip install pyqt5

brew install gmt
brew install libvpx
brew install ffmpeg
```

3. Run code
```
cd magtess-inversion-python
python3 gmi_gui.py
```



## Usage

To run the program, execute:

```
python3 gmi_gui.py
```

In the opened window you should provide paths to a Working directory (a folder with the project and parameter file input.txt) and to compiled executables (tessutil_magnetiza_model, tessbz) from the [magnetic tesseroids](https://github.com/eldarbaykiev/magnetic-tesseroids) package. Once provided, click OK and a main window would open.


### INPUT.TXT

Main window contain the editor for the main parameter file - `input.txt`.
Parameter file `input.txt` contains of several sections and parameters:

| Section | Parameter | Description | Example |
|---|---|---|---|
| Name | | | |
| | PROJECT_NAME | Project name | inv_test_tile_1_nov_2020 |
| Global Tesseroid Model | | Global model's edges | |
| | LON_MIN | Minimal longitude (should be -180) | -180 |
| | LON_MAX | Maximal longitude (should be 180) | 180 |
| | LAT_MIN | Minimal latitude (should be -90) | -90 |
| | LAT_MAX | Maximal latitude (should be 90) | 90 |
| | WIDTH | Tesseroid width  in the model | 2.0 |
| | TOP_SURFACE | Path to the file (LON LAT HEIGHT [m] format) with the geometry of the top model's surface | data/crust1_top.csv |
| |  BOT_SURFACE | Path to the file (LON LAT HEIGHT [m] format) with the geometry of the bottom model's surface | global_moho/moho.csv |
| | IGRF_DAY | Datum for magnetizing main field - day | 1 |
| | IGRF_MONTH | Month | 1 |
| | IGRF_YEAR | Year | 2012 |
| | IGRF_COEFF_FILENAME | Path to the SH of the main field (IGRF) | IGRF12.COF |
| Global Grid | | Calculation grid's parameters | |
| | GRID_LON_MIN | Minimal grid longitude/western edge | -180 |
| | GRID_LON_MAX | Maximal grid longitude/eastern edge | 180 |
| | GRID_LAT_MIN | Minimal grid latitude/southern edge | -90 |
| | GRID_LAT_MAX | Maximal grid latitude/northern edge | 90 |
| | GRID_ALT | Grid altitude | 400000 |
| | GRID_STEP | Grid spacing in degrees | 0.5 |
| Spherical Harmonics | | |
| | N_MIN_CUTOFF | Cutoff degree (all SH degrees below are removed) | 16
| Inversion | | Inversion parameters |
| | OBSERVED_DATA | Path to the grid with observed data (LON LAT Bz [nT] format) | bangui_test_area_5km/LCS1_paper_inv_res.magtess_grid_sat_glob.txt_Bz.xyz | 
| | SUBTRACT_DATA | Path to the grid that should be subtracted from the observed data (LON LAT Bz [nT] format) | bangui_test_area_5km/LCS1_paper_inv_res.magtess_grid_sat_glob.txt_Bz.xyz_minus_piece_LCS1_paper_inv_res.magtess_grid_sat_glob.txt_Bz.xyz |
| | INIT_SOLUTION | Path to the grid with the initial solution (LON LAT SUSCEPTIBILITY format) | result_LCS1_hemant_iter10000/res.xyz |
| | MAX_ITER | Maximal number of iterations | 10000 |
| | MULTIPLICATOR | Multiplicator (for cases of very small values) | 1.0 |
| Tiles | | Tile inversion parameters | |
| | T_LON_MIN | Western edge of the tile (and the calculation grid) | -5 |
| | T_LON_MAX | Eastern edge of the tile | 30 |
| | T_LAT_MIN | Southern edge of the tile | -5 |
| | T_LAT_MAX | Northern edge of the tile | 30 |
| |  T_WIDTH = 0.5 | Tesseroid width | 0.5 |
| |  T_EDGE_EXT = 15 | Tile extension in degrees | 15 |
| | T_GRID_STEP = 0.5 | Tile calculation grid spacing | 0.5 |

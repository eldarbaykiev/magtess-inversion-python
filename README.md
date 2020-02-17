# Magnetic Tesseroid Inversion
Program for global magnetic tesseroid inversion

## Installation

Download the distibution archive (https://github.com/eldarbaykiev/magtess-inversion-python/archive/master.zip) to your computer and unpack it into a folder (for example `~/magtess-inversion-python`). 

### Linux (Ubuntu)

1. Install all necessary packages (**Python 3** with packages, **GMT**, **ffmpeg**):
```
sudo apt install python3
sudo apt install python3-pip
python3 -m pip install --upgrade pip

python3 -m pip install scipy
python3 -m pip install matplotlib
python3 -m pip install tqdm

sudo apt-get install ffmpeg
sudo apt install gmt
```

If you have older **Ubuntu** (<=18.04), just install **PyQT5**:
```
sudo python3 -m pip install pyqt5
```
If you have latest **Ubuntu** 19.10, there is a bug in **PyQT5** isntallation. Try to execute this:
```
sudo apt install python3-widgetsnbextension
sudo apt install python3-testresources
python3 -m pip install --upgrade setuptools
sudo python3 -m pip install pyqt5==5.14
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

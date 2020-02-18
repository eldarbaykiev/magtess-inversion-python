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

# Cross-K project
### Based on kivy framework
### Objective:
    Create multiplatform target builds with real time net driver.
    Basic : player , networking , 3d/2d canvas based engine also 
    UX layouts 

## This is the beginning of a beautiful friendship
![](https://github.com/zlatnaspirala/cross-k/blob/master/engine/assets/logo/logo.png)

### You need before everything to run:

Windows command line
```cmd
python -m virtualenv kivy_venv
```

```cmd
kivy_venv\Scripts\activate
```

Bash command
```bash
source kivy_venv/Scripts/activate
```

Run Engine:
```
python3 main.py
```

## Install and Uninstall

```cmd
python3 -m pip install kivy[full] kivy_examples 
python3 -m pip install --upgrade pip wheel setuptools 
python3 -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --user
python3 -m pip install kivy.deps.gstreamer
python3 -m pip install kivy.deps.angle
python3 -m pip install kivy

pip3.9 install docutils pygments pypiwin32 kivy.deps.sdl2

python3 -m pip uninstall kivy
python3 -m pip uninstall kivy.deps.sdl2
python3 -m pip uninstall kivy.deps.glew
python3 -m pip uninstall kivy.deps.gstreamer
python3 -m pip uninstall image

python3 -m pip install --upgrade pip wheel setuptools
python3 -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --extra-index-url https://kivy.org/downloads/packages/simple/
python3 -m pip install kivy
```

### Android

```
pip install python-for-android
```
# Cross-K project
### Based on kivy framework
### Objective:
    Create multiplatform target builds with real time net driver.
    Basic : player , networking , 3d/2d canvas based engine also 
    UX layouts 

## This is the beginning of a beautiful friendship
![](https://github.com/zlatnaspirala/cross-k/blob/master/engine/assets/logo/logo.png)

### Actual buggies
https://stackoverflow.com/questions/66283282/kivy-bind-dinamic-button-event-return-always-only-last-item-values

### After cloning this project only need to install python3 , pip3 and kivy framework
### You need first time to create `kivy_venv` :
Windows command line
```cmd
python -m c kivy_venv
```

### Activate env before run engine
Windows command
```cmd
kivy_venv\Scripts\activate
```
Bash command
```bash
source kivy_venv/Scripts/activate
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

python3 -m pip install pyinstaller

pip3 install --upgrade pyinstaller
pip3.9 install pyinstaller

python3 -m pip uninstall kivy
python3 -m pip uninstall kivy.deps.sdl2
python3 -m pip uninstall kivy.deps.glew
python3 -m pip uninstall kivy.deps.gstreamer
python3 -m pip uninstall image

python3 -m pip install --upgrade pip wheel setuptools
python3 -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --extra-index-url https://kivy.org/downloads/packages/simple/
python3 -m pip install kivy
```

## Run Engine:

```
python3 main.py
```

# Package

```
 pip3 install --upgrade pyinstaller
```

[WINDOWS]

Package whole engine:
```
kivy_venv/Scripts/python.exe -m PyInstaller --onefile --name NIKI --distpath packages/projectTest --workpath .cache/ main.py
```


# [TODO]

##  [2D-KIVY_BASED]
<pre>

[EDITOR]
 - Add option solution for dimension ref system
   (use pixels or percents)
 - Manage scene element 
     - Details box with save options
     - SceneContainer to select
 - Add other type:
       - Label element
       - Image element
       - Layouts (dinamic with props) element
 - Layouts - Handle sub components

[PACKAGE-SYSTEM]
 - Package for windows

[PLATFORM-WINDOWS]
  - Test

[PLATFORM-LINUX]
  - Test

[PLATFORM-MACOS]
  - Test

[PLATFORM-ANDROID]
 - Test kivy solution
 - Test canvas solution (if ti posible)
 - Test opengles2/3
 
</pre>



### Android No test
```
pip install python-for-android
```

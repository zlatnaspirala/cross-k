
# Cross-K project
### Based on kivy 2.0 framework (Python3)
### Objective:
    Create multiplatform target builds with real time net driver.
    Basic : UI visual app creator. Future player, networking, 3d/2d canvas based engine.

## This is the beginning of a beautiful friendship
![](https://github.com/zlatnaspirala/cross-k/blob/master/engine/assets/logo/logo.png)

After cloning this project only need to install python3, pip3 and kivy 2.0 framework
You need first time to create `kivy_venv`:

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

```js
python3 -m pip install kivy[full] kivy_examples
python3 -m pip install --upgrade pip wheel setuptools
python3 -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --user
python3 -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --extra-index-url https://kivy.org/downloads/packages/simple/
python3 -m pip install kivy.deps.gstreamer
python3 -m pip install kivy.deps.angle
c install kivy
pip3.9 install docutils pygments pypiwin32 kivy.deps.sdl2


python3 -m pip install pyinstaller
pip3 install --upgrade pyinstaller
pip3.9 install pyinstaller

python3 -m pip uninstall kivy
python3 -m pip uninstall kivy.deps.sdl2
python3 -m pip uninstall kivy.deps.glew
python3 -m pip uninstall kivy.deps.gstreamer
python3 -m pip uninstall image
```

If you have problem with :
```js
python3 -m pip ...
Them use this format
pip3 install ...
```

## Run Engine:

```
python3 main.py
```

# Package System

[WINDOWS]

For now i make package for whole engine:

```js
kivy_venv/Scripts/python.exe -m PyInstaller --onefile --name NIKI --distpath packages/projectTest --workpath .cache/ main.py
```

# [TODO-LIST]

<pre>

BETA VERSION [0.1.0] STATUS

[EDITOR]
 - Add option solution for dimension ref system
   (use pixels, percents or combine)            [DONE]
 - Manage scene element 
     - Details box with save options            [DONE]
     - SceneContainer to select                 [DONE]
 - Add Element type:
       - Button element                         [DONE]
       - Label element                          [DONE]
       - Image element
       - ....
       - Layouts (dinamic with props) element   [DONE][must be upgraded]
 - Layouts - Handle sub components              [DONE][must be upgraded]
 - Layouts ( Details commands (ADD_BTN) )       [DONE][must be upgraded]
 - Basic script bind attacher for live (app) buttons. [DONE]

[PACKAGE-SYSTEM]
 - Package for windows                             [WIP]
 - Package for android                             [WIP]
 - Package for macOS                               [WIP]
 - Package for Linux                               [WIP]

[PACKAGE-ANDROID]
 - Test kivy solution                               [WIP]
 - Test canvas solution (if ti posible)             [WIP]
 - Test opengles2/3                                 [WIP]

[EDITOR_PLATFORM-WINDOWS]
  - Test

[EDITOR_PLATFORM-LINUX]
  - Test

[EDITOR_PLATFORM-MACOS]
  - Test

</pre>

### Android No tested
```
pip install python-for-android
```

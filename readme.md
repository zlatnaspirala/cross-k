
# Cross-K project
### Based on kivy 2.0 framework (Python3)
### Objective:
    Create multiplatform target builds with real time net driver.
    Basic : 2D UI visual app creator. Future features player, networking, 3d/2d canvas based engine.
    Because html5 is excluded for now from this story maybe some real time networking makes fit for 
    all platforms. 
    In basic we can create server-client native application for any platform (desktops, android)

## This is the beginning of a beautiful friendship
![](https://github.com/zlatnaspirala/cross-k/blob/master/engine/assets/logo/logo.png)

## First Demo with attaching script
![](https://github.com/zlatnaspirala/cross-k/blob/master/non-project-files/CROSSK_APP_ENGINE_BETA.png)

After cloning this project only need to install python3, pip3and kivy 2.0 framework
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

## Installation

```js
pip3 install kivy[full] kivy_examples
pip3 install --upgrade pip wheel setuptools
pip3 install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --user
pip3 install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew 
             --extra-index-url https://kivy.org/downloads/packages/simple/
pip3 install kivy
pip3 install kivy.deps.gstreamer
pip3 install kivy.deps.angle
pip3 install --upgrade pyinstaller
```

If you have problem with:
```js
pip3 ...
Then use this format
pip3.9 install ...
or
python3 -m pip install
```

## Run Engine:

```
python3 main.py
```

# Package System

[WINDOWS]

```js
kivy_venv/Scripts/python.exe -m PyInstaller --onefile --name SOCIAL_NETWORK_TEST --distpath packages/projectTest --workpath .cache/ app.py
```

For now i make package for whole engine:

```js
kivy_venv/Scripts/python.exe -m PyInstaller --onefile --name CROSSK_Beta --distpath packages/projectTest --workpath .cache/ main.py
```



## STRUCTURE FILES
 Its not perfect for now.

(non project files) => Files from marked folder are not in active dependency 
 of this software.
(Auto generated)    => Usually dont edit dont use it
(VisualCode/debugger)  => You can find help script for python debugger
from MS Visual Code Editor.

<pre>
├── .cache/                        (Auto generated)
├── .vscode/                       (VisualCode/debugger)
├── components/                    (empty for now)
├── demos/                         (not project files)
├── engine/
|   ├── assets/
|   ├── common/
|   |   └── commons.py
|   |   └── enginePackage.py
|   |   └── modification.py
|   |   └── operationBox.py
|   |   └── operationButton.py
|   |   └── operationLabel.py
|   ├── editor/
|   |   └── layout.py
|   |   └── networking.py           [BASIC]
|   |   └── resources.py            [EMPTY]
|   |   └── scripter.py             Future visual node sub editor
|   |   └── sceneGUIContainer.py
|   ├── config.py                  (Engine editor config)
|   ├── editor_main.py             Main Engine File
|   ├── app_main.py                Main Final App File [Used for package procces]
|   ├── kivy_venv/
|   ├── projects/                  (Auto generated - Project files)
|   ├── shader-editor/             (non project files)
</pre>


# [TODO-LIST]

<pre>

ACTUAL VERSION [no release]

BETA VERSION [0.1.0] STATUS

[EDITOR]

 - Add option solution for dimension ref system
   (use pixels, percents or combine)            [DONE]

 - Add option solution for frameLayout and 
   position hint also.
   (use pixels, percents or combine)            [DONE]

 - Manage scene element 
     - Details box with save options            [DONE]
     - SceneContainer to select and preview
       in left side -scroll added               [DONE]

 - Add Element type:
       - Button element                         [DONE]
       - Label element                          [DONE]
       - Image element                          [0.1.1]
       - CheckBox element                       [0.1.2]
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

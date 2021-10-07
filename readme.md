
# Cross-K project
### Based on kivy 2.0 framework (Python3)

    Based on kivy 2.0 python framework. GPL-3.0 License with available source code.
    CrossK is a small but conspiratorial app engine based on kivy 2 / opengles 2.0 in background.
    Created to make future fast and quick.

### Objective:
    - Create multiplatform target builds with real time net driver.
    Basic : 2D UI visual app creator. Future features player, networking, 3d/2d canvas based engine.
    Because html5 is excluded for now from this story maybe some real time networking makes fit for 
    all platforms. In basic we can create server-client native application for any platform (desktops, android)
    - Create server part with also visual GUI approach.
    Strong implementation and relationship between creating server database entity with client
    automatic adaptation in preview mode.

## This is the beginning of a beautiful friendship
![](https://github.com/zlatnaspirala/cross-k/blob/master/engine/assets/logo/logo.png)

## Video 10 min app demostration
https://www.youtube.com/watch?v=Ci8GNd3FDHw&ab_channel=javascriptfanatic

## Screenshot Basic usage

 - Left is Scene list and assets list scrollbars
![](https://github.com/zlatnaspirala/cross-k/blob/master/non-project-files/0.4.0.png)

- Label details box
![](https://github.com/zlatnaspirala/cross-k/blob/master/non-project-files/details.png)

- Images example
![](https://github.com/zlatnaspirala/cross-k/blob/master/non-project-files/cross-k.png)


## Installation

 - 1) After cloning this project only need to install python (current used 3.9.5 python version),
      pip on you computer. Allow adding env variable during installation.

 - 2) Run this `pre-installation.bat`

 - 3) You need first time to create `kivy_venv`:

  Windows command line [Only first time]
  ```cmd
    python -m pip install --upgrade --force-reinstall pip
    python -m pip install --upgrade pip setuptools virtualenv
    python -m virtualenv kivy_venv
  ```

- 4) Activate env 
     [you need to activate env every time before start to work on it]

  Windows command
  ```cmd
  kivy_venv\Scripts\activate
  ```

  Bash command
  ```bash
  source kivy_venv/Scripts/activate
  ```

 - Now you can install last version of kivy 2.1.0 framework.

  You can try this windows installation script `install-win.bat`
  You can try this macox installation script `install-macos.sh`
  You can try this linux installation script `install-ubuntu.sh`


## Run Engine:

```
python main.py
```

# Package System

[WINDOWS]

Pack Application for windows10 with GUI command.

Manual you can package whole engine not just application project.
```js
kivy_venv/Scripts/python.exe -m PyInstaller --onefile --name CROSSK_PROJECT1 --distpath packages/projectTest --workpath .cache/ main.py
```

[ANDROID] WIP


## STRUCTURE

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
├── main.py                        (Engine Instance)
├── app.py                         (App Instance)
├── engine/
|   ├── assets/
|   ├── common/
|   |   └── assetsEditor.py
|   |   └── assetsEditorOperation.py
|   |   └── commons.py
|   |   └── enginePackage.py
|   |   └── modification.py
|   |   └── operationBox.py
|   |   └── operationButton.py
|   |   └── operationLabel.py
|   |   └── operationsPicture.py
|   ├── editor/
|   |   └── layout.py
|   |   └── networking.py
|   |   └── resources.py
|   |   └── scripter.py            Future visual node sub editor,text script for now
|   |   └── resourcesGUIContainer.py
|   |   └── sceneGUIContainer.py
|   ├── config.py                  (Engine editor config)
|   ├── editor_main.py             Main Engine File
|   ├── app_main.py                Main Final App File [Used for package proccess]
|   ├── kivy_venv/                 (Auto generated - env libraries)
|   ├── projects/                  (Auto generated - Project files)
|   ├── shader-editor/             (non project files)
</pre>

# [CROSSK-STATUS-LIST]

<pre>

ACTUAL VERSION [no release] BETA

BETA VERSION [0.4.0] STATUS

[EDITOR]

 - Add option solution for dimension ref system
   (use pixels, percents or combine)

 - Add option solution for frameLayout and 
   position hint also.
   (use pixels, percents or combine)

 - Manage scene element
     - Details box with save options
     - SceneContainer to select and preview render elements
       in left side of engine window -scroll added
     - AssetsContainer to select and preview assets items
       in left side of engine window -scroll added

 - Remove elements
 - Add Element type:
       - Button element
       - Label element
       - CheckBox element
       - Picture Clickable
       - Layouts (dinamic with props) element
 - Layouts - Handle sub components
 - Layouts ( Details commands:
                      - Add button
                      - Add Label
                      - Add layout )
 - CrossK Scripter, Basic script bind attacher for live (app) buttons.

[ASSETS EDITOR]

 - Operation ( Type of Asset:
                          - imageResource,
                          - fontResource)
 - OperationAdd

[PACKAGE-SYSTEM]

 - Package for windows                             [SUPPORTED]
 - Package for Linux                               [SUPPORTED]
 - Package for android                             [NOTESTED]
 - Package for macOS                               [NOTESTED]

[PACKAGE-ANDROID]

 - Test kivy solution                               [NOTESTED]
 - Test canvas solution (if ti posible)             [NOTESTED]
 - Test opengles2/3 in native canvas manir          [NOTESTED]

</pre>


### Android WIP

Best choose Linux Ubuntu
```
pip install python-for-android
```

For windows users use docker

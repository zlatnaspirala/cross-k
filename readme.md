
# Cross-K project
### Based on kivy 2.0 framework (Python3)

    Based on kivy 2.0 python framework. GPL-3.0 License with avavailable source code.
    CrossK is a small but conspiratorial app engine based on kivy opengles2.0 in background.
    Created to make future fast and quick. No builds losing time any more.

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
python3 -m c kivy_venv
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
pip3 install python-for-android

cd submodules/
docker build --tag=p4a --file Dockerfile .

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

You can use it like this if have some `paths` problem `kivy_venv/Scripts/python.exe`.

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

```js
docker run \
    --interactive \
    --tty \
    --volume "G:\web_server\xampp\htdocs\PRIVATE_SERVER\PYTHON\cross-k\cross-k\":/home/user/testapps \
    p4a sh -c
        '. venv/bin/activate \
        && cd testapps \
        && python setup_vispy.py apk \
        --sdk-dir $ANDROID_SDK_HOME \
        --ndk-dir $ANDROID_NDK_HOME'

docker run --interactive --tty --volume "/G/web_server/xampp/htdocs/PRIVATE_SERVER/PYTHON/cross-k/cross-k/submodules/python-for-android/testapps":/home/user/testapps p4a sh -c ". venv/bin/activate && cd testapps && python setup_testapp_python3_sqlite_openssl.py apk --package=nikola.car.sdl2 --name='nidzasdl2' --version=0.5 --bootstrap=sdl2 --sdk-dir $ANDROID_SDK_HOME --ndk-dir $ANDROID_NDK_HOME "

Docker:

p4a apk python3 setup_testapp_python3_sqlite_openssl.py --package=nikola.car.sdl2 --name='nidzasdl2' --version=0.5 --bootstrap=sdl2 --sdk-dir=/usr/lib/android-sdk --ndk-dir=/home/user/android-ndk/android-ndk-r20

/usr/lib/android-sdk
/home/user/android-ndk/android-ndk-r20

wget -c https://dl.google.com/android/repository/android-ndk-r20-linux-x86_64.zip 
unzip android-ndk-r20-linux-x86_64.zip 

export ANDROIDSDK="/usr/lib/android-sdk"
export ANDROIDNDK="/home/user/android-ndk/android-ndk-r20"
export ANDROIDAPI="28"  # Target API version of your application
export NDKAPI="20"  # Minimum supported API version of your application
export ANDROIDNDKVER="r20"  # Version of the NDK you installed
export PATH=/usr/lib/android-sdk/:$PATH
export PATH=/usr/lib/android-sdk/cmdline-tools/3.0/bin/:$PATH
source /etc/bash.bash
source .bashrc

sudo su

docker cp C/Users/Nikola Lukic/Downloads/commandlinetools-linux.zip CONTAINER_ID:/usr/lib/android-sdk
android tools still needed to install 
docker commit 3ecefc2ff45d  crossk/android:ver2

```


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

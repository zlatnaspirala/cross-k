
[ANDROID] WIP

## Requirements

  Installed Docker application.

  For manual setup:
   - https://guides.codepath.com/android/installing-android-sdk-tools
   - https://androidsdkmanager.azurewebsites.net/Buildtools


## AUTOMATISATION FLOW [WIP]
### This can help for any host platform.
```bash

sudo apt-get update

sudo apt-get install cython3
sudo apt-get install autoconf
sudo apt-get install automake
sudo apt-get install g++
sudo apt-get install libtool m4 automake
sudo apt-get install lld

sudo apt-get install libltdl-dev TEST

pip3 install Cython
pip3 install --upgrade Cython
sudo apt-get install -y cython3

pip3 install certifi
pip3 install requests
pip3 install python-for-android

export ANDROID_SDK_HOME=/home/user/Android/android-sdk
export ANDROID_HOME=/home/user/Android/android-sdk
export ANDROIDSDK=/home/user/Android/android-sdk
export ANDROID_NDK_HOME=/home/user/android-ndk-r21e
export PATH=$ANDROID_HOME/cmdline-tools/3.0/bin:$PATH
export PATH=$ANDROID_HOME/tools:$PATH
export PATH=/home/user/.local/bin:$PATH

# Defaults Paths can be different
# tools/bin/sdkmanager "platforms;android-27" "build-tools;27.0.0"
sdkmanager "platforms;android-27" "build-tools;27.0.0"

# ACTIVATE KIVY PY ENV
# . venv/bin/activate

# DOWNLOAD PROCEDURE
# wget https://dl.google.com/android/repository/build-tools_r27.0.3-linux.zip
# unzip myzip.zip

# Intro android sdk tools
# ./android update sdk --no-ui
```

## Buildozer

```bash
git clone https://github.com/kivy/buildozer.git
sudo python3 setup.py install
buildozer init
```

## Docker part
```
docker run --interactive --tty --volume "/G/web_server/xampp/htdocs/PRIVATE_SERVER/PYTHON/cross-k/cross-k/":/home/user/testapps
```

Test
```bash
p4a apk python3 setup_testapp_python3_sqlite_openssl.py --package=org.maximumroulette.crossktest1 --name "Crossk android application" --version 0.1 --bootstrap=sdl2 --requirements=python3,kivy --sdk-dir=$ANDROID_SDK_HOME

p4a apk --package=org.maximumroulette.crossktest1 --name "Crossk android application" --version 0.1 --bootstrap=sdl2 --requirements=python3,kivy --sdk-dir=$ANDROID_SDK_HOME

buildozer -v android debug


ncurses5-compat-libs

```


### Simple copy folder

cp -R /usr/lib/android-sdk /home/user/Android
Default path Not in use `/usr/lib/android-sdk` !


### Download 19 , 20 or 21 Defautl 19.

```bash
wget -c https://dl.google.com/android/repository/android-ndk-r20-linux-x86_64.zip 
unzip android-ndk-r20-linux-x86_64.zip
```

# Copy file from host to docker container
# In case that you download from windows host and wanna put it intro docker ...
# Optimal - better all works done in container then commit to new docker image!

```bash
docker cp C/Users/Nikola Lukic/Downloads/commandlinetools-linux.zip CONTAINER_ID:/usr/lib/android-sdk
# android tools still needed to install
docker commit 3ecefc2ff45d  crossk/android:ver2
```


docker run \
    --interactive \
    --tty \
    --volume "G:\web_server\xampp\htdocs\PRIVATE_SERVER\PYTHON\cross-k\cross-k\":/home/user/crossk \
    p4a sh -c
        '. venv/bin/activate \
        && cd testapps \
        && python setup_vispy.py apk \
        --sdk-dir $ANDROID_SDK_HOME \
        --ndk-dir $ANDROID_NDK_HOME'




docker run \
     zlatnaspirala/crossk-android:beta
    --interactive \
    --tty \
    --volume "G:\web_server\xampp\htdocs\PRIVATE_SERVER\PYTHON\cross-k\cross-k\":/home/user/crossk \
    sh -c
        'cd.. \
        && cd crossk \
        && buildozer -v android debug'


docker ${args_to_docker} run ${args_to_run} image_ref ${cmd_in_container}

docker container run -d --name CROSSKDOCK --tty --volume "G:\web_server\xampp\htdocs\PRIVATE_SERVER\PYTHON\cross-k\cross-k\":/home/user/crossk zlatnaspirala/crossk-android:beta /bin/bash cd.. && cd crossk && buildozer -v android debug

docker run -a stdin -a stdout -i -t -v /g/web_server/xampp/htdocs/PRIVATE_SERVER/PYTHON/cross-k/cross-k:/home/user/crossk zlatnaspirala/crossk-android:beta /bin/bash

docker run -a stdin -a stdout -i -t -v "G:/web_server/xampp/htdocs/PRIVATE_SERVER/PYTHON/cross-k/cross-k/":/home/user/crossk zlatnaspirala/crossk-android:beta /bin/bash 


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

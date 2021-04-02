
## First build 
### version 0.2.0 BETA

New dep: 
```  psutil   ```


 - Create and activate env

```
python3 -m venv ubuntu-env 

cd ./ubuntu-env 
. ./bin/activate
```

or 

```
python3 -m venv ubuntu-env 

cd ./ubuntu-env 
source ./bin/activate
```

Testing android pack from Ubuntu:

```
pip3 install python-for-android
```

```
p4a apk --requirements=kivy --private /home/nidza/Desktop/cross-k/cross-k/ --package=net.test.nidza --name="app" --version=0.5 --bootstrap=sdl2
```
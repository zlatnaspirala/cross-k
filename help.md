
# MANUAL INSTALATION

 If you have trouble with install-win.bat  use this :

```js
pip install kivy[full] kivy_examples
pip install --upgrade pip wheel setuptools
pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --user
pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew 
            --extra-index-url https://kivy.org/downloads/packages/simple/
pip install kivy
pip install kivy.deps.gstreamer
pip install kivy.deps.angle
pip install --upgrade pyinstaller
pip install python-for-android
```

Or 

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
```

Or

```js
python -m pip install kivy[full] kivy_examples
python -m pip install --upgrade pip wheel setuptools
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --user
python -m pip install kivy
python -m pip install kivy.deps.gstreamer
python -m pip install kivy.deps.angle
python -m pip install --upgrade pyinstaller
```

If you got error log with sdl2 try to (Potencial fix) add env YOUR_PYTHONPATH + \share\sdl2\bin


## About code

- operati prefix py files indicate `add new control` forms.

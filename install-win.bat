ECHO =INSTALLATION FOR CROSSK ENGINE
python -m pip install kivy[full] kivy_examples
python -m pip install --upgrade pip wheel setuptools
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --user
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew --extra-index-url https://kivy.org/downloads/packages/simple/
python -m pip install kivy
python -m pip install kivy.deps.gstreamer
python -m pip install kivy.deps.angle
python -m pip install pyenchant
python -m pip install psutil
python -m pip install --upgrade pyinstaller
ECHO =INSTALLATION FOR CROSSK ENGINE DONE

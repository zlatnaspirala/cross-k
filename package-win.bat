
ECHO =MAKE PACKAGE EXECUTE FILE FOR WINDOWS
ECHO =DONT FORGET THAT YOU CAN MAKE PACKAGE FROM EDITOR
kivy_venv/Scripts/python.exe -m PyInstaller --onefile --name SOCIAL_NETWORK_TEST --distpath packages/projectTest --workpath .cache/ app.py
ECHO =MAKE PACKAGE EXECUTE FILE FOR WINDOWS DONE

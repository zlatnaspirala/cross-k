import shutil
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from engine.common.commons import PictureInternal
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.utils import platform
import os
import io
import threading
from functools import partial
from shutil import copyfile

from engine.common.commons import getMessageBoxYesNo

class PackagePopupAndroid():

    def __init__(self, **kwargs):
      self.engineConfig = kwargs.get("engineConfig")
      self.showWindowsPackPopup()

    def makeLinuxPack(self, ins):
        CURRENT_PACK_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../projects/' + self.engineConfig.currentProjectName + "/Package/")
        )
        if not os.path.exists(CURRENT_PACK_PATH):
            print("MAKE PACK DIR.")
            os.mkdir(CURRENT_PACK_PATH)
        print("CrossK Editor: copy data files in package folder.")
        testpackfolder = "projects/" + self.engineConfig.currentProjectName + "/Package/"
        if not os.path.exists(testpackfolder):
            os.mkdir(testpackfolder)

        if platform == 'win':
            csrcdata = "projects/" + self.engineConfig.currentProjectName + "/" + self.engineConfig.currentProjectName + ".json"
            dsrcdata = "projects/" + self.engineConfig.currentProjectName + "/Package/" + self.engineConfig.currentProjectName + "/" + self.engineConfig.currentProjectName +".json"
            startsrcdata = "projects/" + self.engineConfig.currentProjectName + "/data/"
            destsrcdata = "projects/" + self.engineConfig.currentProjectName + "/Package/" + self.engineConfig.currentProjectName
            if not os.path.exists(destsrcdata):
                print("CrossK Editor: Creating package data folder.")
                os.mkdir(destsrcdata)
            destsrcdata = destsrcdata + "/data/"
            if not os.path.exists(destsrcdata):
                print("CrossK Editor: Creating package data folders!!!")
                os.mkdir(destsrcdata)
            copyfile(csrcdata, dsrcdata)
            for root, dirs, files in os.walk(startsrcdata):
                for file in files:
                    path_file = os.path.join(root,file)
                    #print("CrossK Editor SRC = " + path_file)
                    #print("CrossK Editor DEST = " + destsrcdata)
                    collectName = file.split(".")[0]
                    if file.split(".")[1] != "json" :
                        finaldestdata = destsrcdata + "/" + collectName + "/"
                    else:
                        finaldestdata = destsrcdata + "/"
                    if not os.path.exists(finaldestdata):
                        os.mkdir(finaldestdata)
                    shutil.copy2(path_file, finaldestdata, follow_symlinks=True)

        elif platform == 'linux' or True:
            csrcdata = "projects/" + self.engineConfig.currentProjectName + "/" + self.engineConfig.currentProjectName + ".json"
            dsrcdata = "projects/" + self.engineConfig.currentProjectName + "/Package/" + self.engineConfig.currentProjectName + "/" + self.engineConfig.currentProjectName +".json"
            startsrcdata = "projects/" + self.engineConfig.currentProjectName + "/data/"
            destsrcdata = "projects/" + self.engineConfig.currentProjectName + "/Package/" + self.engineConfig.currentProjectName
            if not os.path.exists(destsrcdata):
                print("CrossK Editor: Creating package data folders!!!")
                os.mkdir(destsrcdata)
            destsrcdata = destsrcdata + "/data/"
            if not os.path.exists(destsrcdata):
                print("CrossK Editor: Creating package data folders!!!")
                os.mkdir(destsrcdata)
            copyfile(csrcdata, dsrcdata)
            for root, dirs, files in os.walk(startsrcdata):
                for file in files:
                    path_file = os.path.join(root,file)
                    collectName = file.split(".")[0]
                    if file.split(".")[1] != "json" :
                        finaldestdata = destsrcdata + "/" + collectName + "/"
                    else:
                        finaldestdata = destsrcdata + "/"
                    if not os.path.exists(finaldestdata):
                        os.mkdir(finaldestdata)
                    shutil.copy2(path_file, finaldestdata, follow_symlinks=True)

        bashCommand = "python -m PyInstaller --onefile --name " + self.engineConfig.currentProjectName + " --distpath " + "projects/" + self.engineConfig.currentProjectName + "/Package/" + " --workpath .cache/ app.py"
        print("Pack script: ", bashCommand )
        import subprocess
        process = subprocess.run(bashCommand.split())
        try:
            if procces.stdout != None and procces.stdout != 'NoneType':
                for line in iter(process.stdout.readline, b'\n'): # b'\n'-separated lines
                    self.testLog = str(line)
                    self.LOGS.text = self.testLog
                    print ("PACKAGE:",  self.testLog)
        except NameError: print ("PACKAGE ERROR INTERNAL:")
        print("Package application for linux ended.")

    def showWindowsPackPopup(self):

        print("showWindowsPackPopup....")
        box = BoxLayout(orientation="vertical", spacing=1)

        self.infoBtn = Button(text='Cancel', size_hint=(1, 0.5))
        PictureInternal(injectWidget=box, accessAssets="logo")
        if platform == 'win':
            box.add_widget(Label(size_hint=(1, 0.5), text='Make android APK final application package with PROJECT_NAME data folder. \n You will need to have docker installed on your computer.'))
        elif platform == 'linux':
            box.add_widget(Label(size_hint=(1, 0.5), text='Make android APK final application package with PROJECT_NAME data folder. \n You will need to have docker installed on your computer.'))
        else:
            box.add_widget(Label(size_hint=(1, 0.5), text='Make android APK final application package with PROJECT_NAME data folder. \n You will need to have docker installed on your computer. Not tested env !'))

        _local1 = '[b]Relative path:[b] ' + self.engineConfig.currentProjectName
        box.add_widget(Label(size_hint=(1, 0.2), markup=True, text=_local1))
        _local0 = '[b]Package Execute File destination path:[b] ' + self.engineConfig.currentProjectPath + '/Package/'
        box.add_widget(Label(size_hint=(1, 0.2), markup=True, text=_local0 ))

        self.makeWinPackBtn = Button(markup=True, size_hint=(1, 0.5), text='[b]Make Package[b]')

        self.testLog = "test log"
        self.LOGS = TextInput(text='', foreground_color=(0,1,0,1) ,
            background_color=self.engineConfig.getThemeBackgroundColor())

        self.debugLogTextLabel = Label(markup=True, text="Building final execute package in progress ... Editor will be freezed until packaging works. You can go to VisualCode terminal to see logs.")
        box.add_widget(self.debugLogTextLabel)
        box.add_widget(self.LOGS)

        box.add_widget(self.makeWinPackBtn)
        box.add_widget(self.infoBtn)

        _local = 'CrossK ' + self.engineConfig.getVersion()
        popup = Popup(title=_local , content=box, auto_dismiss=False)

        self.infoBtn.bind(on_press=popup.dismiss)

        if platform == 'win':
            self.makeWinPackBtn.bind(on_press=lambda a:self.runInNewThread())
        elif platform == 'linux' or True:
            self.makeWinPackBtn.bind(on_press=lambda a:self.runInNewThread())
            # self.makeWinPackBtn.bind(on_press=lambda a:self.makeLinuxPack())
            # self.makeWinPackBtn.bind(on_press=partial(self.makeLinuxPack))

        popup.open()

    def runInNewThread(self):
        t = threading.Thread(target=self.makeAndroidPack)
        t.start()
        print('started')
        t.join()
        print('finished')
        getMessageBoxYesNo("Packing finised. Please check your PROJECT_NAME/Package folder.", "OK")

    def log_subprocess_output(self, pipe):
        for line in io.TextIOWrapper(pipe, encoding="utf-8"):
            print(line)
            self.LOGS.text = self.LOGS.text + line
        #for line in iter(pipe.readline, b''): # b'\n'-separated lines
        #    self.infoBtn.text = str(line)
        #    print('got line from subprocess: %r', line)

    def makeAndroidPack(self):

        CURRENT_PACK_PATH = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../../projects/' + self.engineConfig.currentProjectName + "/Package/")
        )
        if not os.path.exists(CURRENT_PACK_PATH):
            print("CrossK Editor: Creating package folder. All nessesery files will be created intro "  + self.engineConfig.currentProjectName + "/package folder.")
            os.mkdir(CURRENT_PACK_PATH)
        else:
            print("CrossK Editor: Package folder exist.")

        print("CrossK Editor: copy data files in package folder.")

        testpackfolder = "projects/" + self.engineConfig.currentProjectName + "/Package/"
        if not os.path.exists(testpackfolder):
            os.mkdir(testpackfolder)

        if platform == 'winDISABLED':
            csrcdata = "projects/" + self.engineConfig.currentProjectName + "/" + self.engineConfig.currentProjectName + ".json"
            dsrcdata = "projects/" + self.engineConfig.currentProjectName + "/Package/" + self.engineConfig.currentProjectName + "/" + self.engineConfig.currentProjectName +".json"
            startsrcdata = "projects/" + self.engineConfig.currentProjectName + "/data/"
            destsrcdata = "projects/" + self.engineConfig.currentProjectName + "/Package/" + self.engineConfig.currentProjectName
            if not os.path.exists(destsrcdata):
                print("CrossK Editor: Creating package data folders!!!")
                os.mkdir(destsrcdata)
            destsrcdata = destsrcdata + "/data/"
            if not os.path.exists(destsrcdata):
                print("CrossK Editor: Creating package data folders!!!")
                os.mkdir(destsrcdata)
            copyfile(csrcdata, dsrcdata)
            for root, dirs, files in os.walk(startsrcdata):
                for file in files:
                    path_file = os.path.join(root,file)
                    #print("CrossK Editor SRC = " + path_file)
                    #print("CrossK Editor DEST = " + destsrcdata)
                    collectName = file.split(".")[0]
                    if file.split(".")[1] != "json" :
                        finaldestdata = destsrcdata + "/" + collectName + "/"
                    else:
                        finaldestdata = destsrcdata + "/"
                    if not os.path.exists(finaldestdata):
                        os.mkdir(finaldestdata)
                    shutil.copy2(path_file, finaldestdata, follow_symlinks=True)

        elif platform == 'DISABLED':
            csrcdata = "projects/" + self.engineConfig.currentProjectName + "/" + self.engineConfig.currentProjectName + ".json"
            dsrcdata = "projects/" + self.engineConfig.currentProjectName + "/Package/" + self.engineConfig.currentProjectName + "/" + self.engineConfig.currentProjectName +".json"
            startsrcdata = "projects/" + self.engineConfig.currentProjectName + "/data/"
            destsrcdata = "projects/" + self.engineConfig.currentProjectName + "/Package/" + self.engineConfig.currentProjectName
            if not os.path.exists(destsrcdata):
                print("CrossK Editor: Creating package data folders!!!")
                os.mkdir(destsrcdata)
            destsrcdata = destsrcdata + "/data/"
            if not os.path.exists(destsrcdata):
                print("CrossK Editor: Creating package data folders!!!")
                os.mkdir(destsrcdata)
            copyfile(csrcdata, dsrcdata)
            for root, dirs, files in os.walk(startsrcdata):
                for file in files:
                    path_file = os.path.join(root,file)
                    #print("CrossK Editor SRC = " + path_file)
                    #print("CrossK Editor DEST = " + destsrcdata)
                    collectName = file.split(".")[0]
                    if file.split(".")[1] != "json" :
                        finaldestdata = destsrcdata + "/" + collectName + "/"
                    else:
                        finaldestdata = destsrcdata + "/"
                    if not os.path.exists(finaldestdata):
                        os.mkdir(finaldestdata)
                    shutil.copy2(path_file, finaldestdata, follow_symlinks=True)


        bashCommand = "ls"
        # bashCommand = " --name ANDROIDPACK " + self.engineConfig.currentProjectName + " --distpath " + "projects/" + self.engineConfig.currentProjectName + "/Package/" + " --workpath .cache/ "
        # bashCommand = "kivy_venv/Scripts/python.exe -m PyInstaller --onefile --name " + self.engineConfig.currentProjectName + " --distpath " + "projects/" + self.engineConfig.currentProjectName + "/Package/" + " --workpath .cache/ app.py"
        import subprocess
        # stdout=PIPE, stderr=STDOUT
        process = subprocess.Popen(bashCommand.split(), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        #process = subprocess.run(bashCommand.split())
        # print(process.stdout)
        with process.stdout:
            self.log_subprocess_output(process.stdout)
        #for line in iter(process.stdout.readline, b'\n'): # b'\n'-separated lines
        #    print ("PACKAGE:",  str(line))
            print("Package application for windows ended.")

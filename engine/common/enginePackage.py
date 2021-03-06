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

class PackagePopup():

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
        else:
            print("PACK DIR EXIST.")

        bashCommand = "python3 -m PyInstaller --onefile --name " + self.engineConfig.currentProjectName + " --distpath " + "projects/" + self.engineConfig.currentProjectName + "/Package/" + " --workpath .cache/ app.py"
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
        box = BoxLayout(orientation="vertical")

        self.infoBtn = Button(text='Cancel')
        PictureInternal(injectWidget=box, accessAssets="logo")
        if platform == 'win':
            box.add_widget(Label(text='Make windows app.exe final application package.'))
        elif platform == 'linux':
            box.add_widget(Label(text='Make final linux application package.'))
        else:
            box.add_widget(Label(text='Make final macos application package.'))
        
        _local1 = '[b]Relative path:[b] ' + self.engineConfig.currentProjectName
        box.add_widget(Label(markup=True, text=_local1))
        _local0 = '[b]Package Execute File destination path:[b] ' + self.engineConfig.currentProjectPath
        box.add_widget(Label( markup=True, text=_local0 ))
    
        self.makeWinPackBtn = Button(markup=True, text='[b]Make Package[b]')
        
        self.testLog = "test log"
        self.LOGS = TextInput(text='', foreground_color=(0,1,0,1) ,
            background_color=self.engineConfig.getThemeBackgroundColor())

        box.add_widget(Label(markup=True,
                            text="""[b]Debug logs[b]"""))
        box.add_widget(self.LOGS)

        box.add_widget(self.makeWinPackBtn)
        box.add_widget(self.infoBtn)

        _local = 'CrossK ' + self.engineConfig.getVersion()
        popup = Popup(title=_local , content=box, auto_dismiss=False)

        self.infoBtn.bind(on_press=popup.dismiss)

        if platform == 'win':
            self.makeWinPackBtn.bind(on_press=lambda a:self.runInNewThread())
        elif platform == 'linux' or True:
            # self.makeWinPackBtn.bind(on_press=lambda a:self.makeLinuxPack())
            self.makeWinPackBtn.bind(on_press=partial(self.makeLinuxPack))

        popup.open()

    def runInNewThread(self):
        t = threading.Thread(target=self.makeWinPack)
        t.start()
        print('...started')
        t.join()
        print('finished')
    
    # DISABLED
    def runInNewThreadLinux(self):
 
        t = threading.Thread(target=self.makeLinuxPack)
        t.start()
        print('...started')
        t.join()
        print('finished')
  
    def log_subprocess_output(self, pipe):
        for line in io.TextIOWrapper(pipe, encoding="utf-8"):
           self.LOGS.text = self.infoBtn.text + line
        #for line in iter(pipe.readline, b''): # b'\n'-separated lines
        #    self.infoBtn.text = str(line)
        #    print('got line from subprocess: %r', line)
    
    def makeWinPack(self):

        CURRENT_PACK_PATH = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../../projects/' + self.engineConfig.currentProjectName + "/Package/")
        )
        if not os.path.exists(CURRENT_PACK_PATH):
            print("MAKE PACK DIR")
            os.mkdir(CURRENT_PACK_PATH)
        else:
            print("PACK DIR EXIST...")

        bashCommand = "kivy_venv/Scripts/python.exe -m PyInstaller --onefile --name " + self.engineConfig.currentProjectName + " --distpath " + "projects/" + self.engineConfig.currentProjectName + "/Package/" + " --workpath .cache/ app.py"
        import subprocess
        #  stdout=PIPE, stderr=STDOUT
        # process = subprocess.Popen(bashCommand.split(), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        process = subprocess.run(bashCommand.split())

        print(process.stdout)
        #with process.stdout:
        #    self.log_subprocess_output(process.stdout)
        #for line in iter(process.stdout.readline, b'\n'): # b'\n'-separated lines
        #    print ("PACKAGE:",  str(line))

        print("Package application for windows ended.")
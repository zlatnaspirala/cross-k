from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from engine.common.commons import Picture
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import os
import io

class PackagePopup():

    def __init__(self, **kwargs):
      self.engineConfig = kwargs.get("engineConfig")
      self.showWindowsPackPopup()

    def showWindowsPackPopup(self):
      print("showWindowsPackPopup....")
      box = BoxLayout(orientation="vertical")

      self.infoBtn = Button(text='Cancel')

      box.add_widget(Label(markup=True,
                          text="""[b]win64[b]"""))
      Picture(injectWidget=box, accessAssets="logo")

      box.add_widget(Label(text='Make windows app.exe final application package.'))

      _local1 = 'Relative path: ' + self.engineConfig.currentProjectName
      box.add_widget(Label(text=_local1))
      _local0 = 'Package EXE destination path: ' + self.engineConfig.currentProjectPath
      box.add_widget(Label(text=_local0 ))
  
      self.makeWinPackBtn = Button(text='Make Package')

      box.add_widget(self.makeWinPackBtn)
      box.add_widget(self.infoBtn)

      _local = 'CrossK ' + self.engineConfig.getVersion()
      popup = Popup(title=_local , content=box, auto_dismiss=False)

      self.infoBtn.bind(on_press=popup.dismiss)
      
      self.makeWinPackBtn.bind(on_press=lambda a:self.makeWinPack())

      self.LOGS = TextInput()
      box.add_widget(self.LOGS)

      popup.open()

    def makeWinPack(self):

        CURRENT_PACK_PATH = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../../projects/' + self.engineConfig.currentProjectName + "/Package/")
        )
        if not os.path.exists(CURRENT_PACK_PATH):
            print("MAKE PACK DIR")
            os.mkdir(CURRENT_PACK_PATH)
        else:
            print("PACK DIR EXIST...")

        bashCommand = "kivy_venv/Scripts/python.exe -m PyInstaller --onefile --name " + self.engineConfig.currentProjectName + " --distpath " + "projects/" + self.engineConfig.currentProjectName + "/Package/" + " --workpath .cache/ main.py"
        import subprocess
        #  stdout=PIPE, stderr=STDOUT
        process = subprocess.Popen(bashCommand.split(), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        #with process.stdout:
        #    self.log_subprocess_output(process.stdout)
        myLogs = []
        for line in iter(process.stdout.readline, b'\n'): # b'\n'-separated lines
            myLogs.append( str(line) )
            print(str(line))
        # print('got line from subprocess: %r', line)
        # print('Take one line:', myLogs[30])
        #while True:
        #    line = process.stdout.readline()
        #    if line != '':
        #        test_str = str(subprocess.check_output(["echo", line]))
        #        # self.LOGS.text =+ test_str
        #        print(subprocess.check_output(["echo", line]))
        #    else:
        #        break

        # output, error = process.communicate()
        print("Package application for windows ended.")

    def log_subprocess_output(self, pipe):

        for line in io.TextIOWrapper(pipe, encoding="utf-8"):
           self.LOGS.text = self.infoBtn.text + line

        #for line in iter(pipe.readline, b''): # b'\n'-separated lines
        #    self.infoBtn.text = str(line)
        #    print('got line from subprocess: %r', line)
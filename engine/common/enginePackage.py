from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from engine.common.commons import Picture
from kivy.uix.popup import Popup
import os

class PackagePopup():

    def __init__(self, **kwargs):
      self.engineConfig = kwargs.get("engineConfig")
      self.showWindowsPackPopup()

    def showWindowsPackPopup(self):
      print("showWindowsPackPopup....")
      box = BoxLayout(orientation="vertical")

      infoBtn = Button(text='Cancel')

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
      box.add_widget(infoBtn)

      _local = 'CrossK ' + self.engineConfig.getVersion()
      popup = Popup(title=_local , content=box, auto_dismiss=False)

      infoBtn.bind(on_press=popup.dismiss)
      
      self.makeWinPackBtn.bind(on_press=lambda a:self.makeWinPack())

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

        bashCommand = "kivy_venv/Scripts/python.exe -m PyInstaller --onefile --name " +
            self.engineConfig.currentProjectName + " --distpath " + "projects/" +
            self.engineConfig.currentProjectName + "/Package/" + " --workpath .cache/ main.py"

        import subprocess
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print("Package application for windows ended.")

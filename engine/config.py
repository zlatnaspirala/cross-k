
from dataclasses import dataclass
from kivy.properties import StringProperty, ObjectProperty

class EngineConfig:

  def __init__(self, *args, **kwargs):

    # Engine version 0.1.0 beta
    self.version = "0.1.0"

    # Windows solution
    self.runInFullScreen = False

    self.programmer = {
      "nickname": "Nikola Lukic",
      "slogan" : "meta data"
    }

    self.auth = {
      'username': 'admin',
      'password': 'admin'
    }

    # Themes
    self.currentTheme = "light"
    self.setupThemes()

    # RUNTIME - Predefinitions
    self.currentProjectPath = 'mynull'
    self.currentProjectName = 'mynull'
    print("Engine config getVersion test." )
    
    print("Engine config loaded.", )

  def setupThemes(self):

    print("Setup init colors shema.")
    self.themes = {
      "light" : {
        "background": {
          "r" : 0,
          "b" : 0,
          "g" : 0,
        },
        "maintext": {
          "r" : 1,
          "b" : 1,
          "g" : 1,
        }
      },
      "black" : {
        "background": {
          "r" : 1,
          "b" : 1,
          "g" : 1,
        },
        "maintext": {
          "r" : 0,
          "b" : 0,
          "g" : 0,
        }
      },
    }

  def getTheme(self):
    return self.themes[self.currentTheme]

  def getThemeTextColor(self):
    return self.themes[self.currentTheme]["maintext"]

  def getVersion(self):
    print("Current CrossK version :" + self.version)

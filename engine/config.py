
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
        },
        "sceneGUIbgBTN": {
          "r" : 0.55,
          "b" : 0.65,
          "g" : 0.45,
        },
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
        },
        "sceneGUIbgBTN": {
          "r" : 0.45,
          "b" : 0.55,
          "g" : 0.65,
        },
      },
    
    }

  def getTheme(self):
    return self.themes[self.currentTheme]

  def getThemeTextColorByComp(self, test):
    return self.themes[self.currentTheme]["maintext"]

  def getThemeTextColor(self):
    print("TEST COLOR ")
    return (
      self.getThemeTextColorByComp("maintext")["r"],
      self.getThemeTextColorByComp("maintext")["b"],
      self.getThemeTextColorByComp("maintext")["g"],
      1
    )

  def getThemeBackgroundColor(self):
    return (
      self.getThemeTextColorByComp()["r"],
      self.getThemeTextColorByComp()["b"],
      self.getThemeTextColorByComp()["g"],
      1
    )

  def getVersion(self):
    print("Current CrossK version :" + self.version)


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
    self.currentTheme = "black"
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
          "r" : 0.6,
          "b" : 0.2,
          "g" : 0.2,
        },
        "sceneGUIbgWidget": {
          "r" : 0.9,
          "b" : 0.2,
          "g" : 0.9,
        },
        "consoleText": {
          "r" : 0,
          "b" : 1,
          "g" : 0,
        },
      },
      "black" : {
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
          "r" : 0.2,
          "b" : 0.2,
          "g" : 0.6,
        },
        "sceneGUIbgWidget": {
          "r" : 0.2,
          "b" : 0.2,
          "g" : 0.9,
        },
        "consoleText": {
          "r" : 0,
          "b" : 1,
          "g" : 0,
        },
      },
    
    }

  def getTheme(self):
    return self.themes[self.currentTheme]

  def getThemeTextColorByComp(self, flag):
    return self.themes[self.currentTheme][flag]

  def getThemeCustomColor(self, key):
    # print("TEST COLOR ")
    return (
      self.getThemeTextColorByComp(key)["r"],
      self.getThemeTextColorByComp(key)["b"],
      self.getThemeTextColorByComp(key)["g"],
      1
    )

  def getThemeTextColor(self):
    # print("TEST COLOR ")
    return (
      self.getThemeTextColorByComp("maintext")["r"],
      self.getThemeTextColorByComp("maintext")["b"],
      self.getThemeTextColorByComp("maintext")["g"],
      1
    )

  def getThemeBackgroundColor(self):
    return (
      self.getThemeTextColorByComp("background")["r"],
      self.getThemeTextColorByComp("background")["b"],
      self.getThemeTextColorByComp("background")["g"],
      1
    )

  def getThemeBgSceneBtnColor(self):
    return (
      self.getThemeTextColorByComp("sceneGUIbgBTN")["r"],
      self.getThemeTextColorByComp("sceneGUIbgBTN")["b"],
      self.getThemeTextColorByComp("sceneGUIbgBTN")["g"],
      1
    )

  def getThemeBgSceneBoxColor(self):
    return (
      self.getThemeTextColorByComp("sceneGUIbgWidget")["r"],
      self.getThemeTextColorByComp("sceneGUIbgWidget")["b"],
      self.getThemeTextColorByComp("sceneGUIbgWidget")["g"],
      1
    )

  def getVersion(self):
    print("Current CrossK version: " + self.version)
    return "current version: " + self.version

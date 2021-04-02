
from dataclasses import dataclass
from kivy.properties import StringProperty, ObjectProperty

class EngineConfig:

  def __init__(self, *args, **kwargs):

    # Engine version 0.3.0 beta
    self.version = "0.3.0"
    self.licence = "GPL v3"

    # Windows solution
    self.runInFullScreen = False

    self.programmer = {
      "nickname": "Nikola Lukic",
      "slogan" : "Everything is possible",
      "www": "https://maximumroulette.com"
    }

    self.auth = {
      'username': 'admin',
      'password': 'admin'
    }

    # Define Themes black/light
    self.currentTheme = "black"
    self.setupThemes()

    # RUNTIME USAGE IN APP LEVEL - PreDefinitions
    self.currentProjectPath = 'mynull'
    self.currentProjectName = 'mynull'

    self.platformRoles = {
      'showAboutBoxOnLoad': False,
      'win': {
        'fullscreen': False,
        'initialWidth': 1200,
        'initialHeight': 700
      }
    }

  def setupThemes(self):

    self.themes = {
      "light" : {
        "background": {
          "r" : 1,
          "g" : 1,
          "b" : 1,
        },
        "maintext": {
          "r" : 1,
          "g" : 1,
          "b" : 1,
        },
        "engineBtnsBackground": {
          "r" : 0.3,
          "g" : 0.3,
          "b" : 0.3,
        },
        "engineBtnsColor": {
          "r" : 0,
          "g" : 0,
          "b" : 0,
        },
        "warn": {
          "r" : 1,
          "g" : 0.3,
          "b" : 0.3,
        },
        "alert": {
          "r" : 1,
          "g" : 0.1,
          "b" : 0.1,
        },
        "sceneGUIbgLabel": {
          "r" : 0.5,
          "g" : 0.3,
          "b" : 0.3,
        },
        "sceneGUIbgBTN": {
          "r" : 0.7,
          "g" : 0.3,
          "b" : 0.3,
        },
        "sceneGUIbgWidget": {
          "r" : 0.6,
          "g" : 0.4,
          "b" : 0.4,
        },
        "consoleText": {
          "r" : 0,
          "g" : 1,
          "b" : 0,
        },
      },
      "black" : {
        "background": {
          "r" : 0,
          "g" : 0,
          "b" : 0,
        },
        "maintext": {
          "r" : 1,
          "g" : 1,
          "b" : 1,
        },
        "engineBtnsBackground": {
          "r" : 0.2,
          "g" : 0.2,
          "b" : 0.2,
        },
        "engineBtnsColor": {
          "r" : 1,
          "g" : 1,
          "b" : 1,
        },
        "warn": {
          "r" : 0.8,
          "g" : 0,
          "b" : 0.5,
        },
        "alert": {
          "r" : 1,
          "g" : 0.3,
          "b" : 0.3,
        },
        "sceneGUIbgLabel": {
          "r" : 0.4,
          "g" : 0,
          "b" : 0.5,
        },
        "sceneGUIbgBTN": {
          "r" : 0.6,
          "g" : 0.2,
          "b" : 0.6,
        },
        "sceneGUIbgWidget": {
          "r" : 0.4,
          "g" : 0.1,
          "b" : 0.6,
        },
        "consoleText": {
          "r" : 0,
          "g" : 1,
          "b" : 0,
        },
      },
    }

  def getTheme(self):
    return self.themes[self.currentTheme]

  def getThemeTextColorByComp(self, flag):
    return self.themes[self.currentTheme][flag]

  def getThemeCustomColor(self, key):
    return (
      self.getThemeTextColorByComp(key)["r"],
      self.getThemeTextColorByComp(key)["g"],
      self.getThemeTextColorByComp(key)["b"],
      1
    )

  def getThemeTextColor(self):
    return (
      self.getThemeTextColorByComp("maintext")["r"],
      self.getThemeTextColorByComp("maintext")["g"],
      self.getThemeTextColorByComp("maintext")["b"],
      1
    )

  def getThemeBackgroundColor(self):
    return (
      self.getThemeTextColorByComp("background")["r"],
      self.getThemeTextColorByComp("background")["g"],
      self.getThemeTextColorByComp("background")["b"],
      1
    )

  def getThemeBgSceneBtnColor(self):
    return (
      self.getThemeTextColorByComp("sceneGUIbgBTN")["r"],
      self.getThemeTextColorByComp("sceneGUIbgBTN")["g"],
      self.getThemeTextColorByComp("sceneGUIbgBTN")["b"],
      1
    )

  def getThemeBgSceneBoxColor(self):
    return (
      self.getThemeTextColorByComp("sceneGUIbgWidget")["r"],
      self.getThemeTextColorByComp("sceneGUIbgWidget")["g"],
      self.getThemeTextColorByComp("sceneGUIbgWidget")["b"],
      1
    )

  def getVersion(self):
    print("Current CrossK version: " + self.version)
    return "Current version: " + self.version

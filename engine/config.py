
from dataclasses import dataclass

class EngineConfig:

  def __init__(self):
    # TEST
    self.runInFullScreen = False
    self.auth = {
      'username': 'admin',
      'password': 'admin'
    }

    self.currentTheme = "light"
    self.setupThemes()

    print("Engine config loaded.")

  def setupThemes(self):

    print("Setup init colors shema.")
    self.themes = {
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
        }
      },
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
        }
      },
    }

  def getTheme(self):
    return self.themes[self.currentTheme]

  def getThemeTextColor(self):
    return self.themes[self.currentTheme]["maintext"]

  def getVersion(self):
    print(self.auth['username'])
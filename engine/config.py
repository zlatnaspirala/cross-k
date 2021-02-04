
from dataclasses import dataclass

class EngineConfig:

  def __init__(self):
    # TEST
    self.runInFullScreen = False
    self.auth = {
      'username': 'admin',
      'password': 'admin'
    }
    print("Engine config loaded.")
  def getVersion(self):
    print(self.auth['username'])
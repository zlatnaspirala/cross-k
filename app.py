
import os
import kivy
from kivy.config import Config

print(kivy.__version__)

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button

Config.set('kivy', 'keyboard_mode', 'systemandmulti')

# Replace here
from engine.app_main import EditorMain

Config.set('graphics', 'resizable', True) 

class MyApp(App):

    def aboutCrossK(self):

        print("-------------------------------------------------")
        print("-CrossK engine App build 0.5.0 BETA            .-")
        print("-This is build pack root class for final app     .-")
        print("-build. Optimised and represent single target    .-")
        print("-point. We build all platforms with this class   .-")
        print("---------------------------------------------------")
        print("- ACTION NEEDED                                  .-")
        print("- NEEDS COPY OF PROJECTNAMEFOLDER WITH DATA.      -")
        print("--------------------------------------------------")
        print("-SUPPORT PACKAGE TARGETS: WIN, LINUX--------------")
        print("--------------------------------------------------")

    def build(self):
        self.title = 'CROSSK ENGINE'
        self.aboutCrossK()
        return EditorMain(pack="Project1")

if __name__ == '__main__':
    MyApp().run()

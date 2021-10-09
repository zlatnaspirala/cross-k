
import os

#os.environ["KIVY_NO_ARGS"] = "1"
#os.environ['KIVY_IMAGE'] = "pil,sdl2" # use pil instead of SDL2 image if you get the libpng16 error
# you must add to the path the location of your SDL2 binaries
#os.environ['PATH'] += ';' + os.path.expandvars('%AppData%\\Python\\share\\glew\\bin')
#os.environ['PATH'] += ';' + os.path.expandvars('%AppData%\\Python\\share\\sdl2\\bin')

import kivy
from kivy.config import Config

print(kivy.__version__)

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button

Config.set('kivy', 'keyboard_mode', 'systemandmulti')

from engine.editor_main import EditorMain

Config.set('graphics', 'resizable', True)

class MyApp(App):

    def aboutCrossK(self, instance):

        print("-------------------------------------------------")
        print("-CrossK engine 0.2.0                           .-")
        print(" Version Beta                                  .-")
        print(" - Support UI context [add/edit gui]           .-")
        print("  ->Button, Layout, Label, PictureCliclable    .-")
        print("  ->Scene container                            .-")
        print(" - Bind Script [extend kivy2/python3.9]        .-")
        print("-------------------------------------------------")

    def build(self):
        self.title = 'CrossK Multiplatform App Engine'
        return EditorMain()

if __name__ == '__main__':
    MyApp().run()

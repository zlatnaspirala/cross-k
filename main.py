
import os
import kivy
from kivy.config import Config

print(kivy.__version__)

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from engine.editor_main import EditorMain

Config.set('graphics', 'resizable', True)

class MyApp(App):

    def aboutCrossK(self, instance):

        print("-------------------------------------------------")
        print("-CrossK engine 0.2.0                           .-")
        print(" Version Beta                                  .-")
        print(" - Support UI context [add/edit gui]           .-")
        print("  ->Button, Layout, Label, PictureCliclable    .-")
        print(" - Bind Script [extend kivy2/python3.9]        .-")
        print("-------------------------------------------------")

    def build(self):
        self.title = 'CrossK Multiplatform App Engine'
        return EditorMain()

if __name__ == '__main__':
    MyApp().run()

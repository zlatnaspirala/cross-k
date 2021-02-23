

import os
import kivy
from kivy.config import Config  

print(kivy.__version__)

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button

#from components.main_form.layout import LoginScreen
from engine.editor_main import EditorMain

Config.set('graphics', 'resizable', True) 

class MyApp(App):

    def aboutCrossK(self, instance):
        print("-------------------------------------------------")
        print("-CrossK engine 0.1.0                           .-")
        print("-------------------------------------------------")

    def build(self):
        self.title = 'CrossK game engine beta test'

        return EditorMain()

if __name__ == '__main__':
    MyApp().run()
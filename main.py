
import kivy

print(kivy.__version__)

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button

from components.main_form.layout import LoginScreen
from engine.editor_main import EditorMain

class MyApp(App):

    def aboutCrossK(self, instance):
        print("-----------------------------------------------")
        print("I have a good feeling about this. Python Roles.")
        print("-----------------------------------------------")
        
    def build(self):
        self.title = 'CrossK game engine test'
        return EditorMain()

if __name__ == '__main__':
    MyApp().run()
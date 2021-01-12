import kivy

print(kivy.__version__)

kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button

from components.main_form.layout import LoginScreen
from engine.createProject import CreateProject

class MyApp(App):

    def animate(self, instance):
        print("BALBAL")
        
    def build(self):
        self.title = 'Cross K game engine test'
        return CreateProject()

if __name__ == '__main__':
    MyApp().run()
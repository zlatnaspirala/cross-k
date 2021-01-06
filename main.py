import kivy

print(kivy.__version__)

kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label


class MyApp(App):

    def build(self):
        self.title = 'Cross K game engine test'
        return Label(text='This is the beginning of a beautiful friendship')


if __name__ == '__main__':
    MyApp().run()
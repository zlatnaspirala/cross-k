from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class EngineLayout(BoxLayout):

    def action_engine_create_project(self, instance):
        print("create project")

    def __init__(self, **kwargs):
        super(EngineLayout, self).__init__(**kwargs)
        pass
        print("Testing layout size: ", self.size )
        print("Testing layout pos: ", self.pos )

        self.engineTitle = Label(text='TEXT COMPONENT', size_hint=(.5, .1), color=(1,0,1,1) )

        self.add_widget(self.engineTitle)
         
        self.button = Button(text='plop', pos=(1,1),size_hint=(.5, .1), on_press=self.action_engine_create_project)
        self.add_widget(self.button)

        with self.canvas.before:
            Color(0.3, 0.1, 0.6, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

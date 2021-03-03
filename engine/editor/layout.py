from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty

class EngineLayout(BoxLayout):

    # This is root app class container. I need to pass all needed staff
    # from main-editor or make copy of main-editor and remove unused code.
    # Must be done before package feature

    currentProjectPath = StringProperty('null')
    currentProjectName = StringProperty('null')

    def loadAppElementsStore():
        print("This is app level root")

    def __init__(self, **kwargs):
        super(EngineLayout, self).__init__(**kwargs)
        # print("Testing layout size: ", self.size)
        # print("Testing layout pos: ", self.pos)

        with self.canvas.before:
            Color(0.3, 0.1, 0.6, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    # Definition for update call bg
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

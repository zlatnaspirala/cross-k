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
from kivy.cache.cache import Cache

class ResourcesGUIContainer():

    def __init__(self, **kwargs):
        super(ResourcesGUIContainer, self).__init__(**kwargs)

    def access(self):
        print("ATTACH")

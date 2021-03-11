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
# from kivy.cache.cache import Cache
from kivy.network.urlrequest import UrlRequest

class Networking():

    def on_error(self, error):
        print("Networking - on_error", error)

    def on_failure(self, error):
        print("Networking - on_failure", error)

    def on_redirect(self, error):
        print("Networking - on_redirect", error)

    def analyzeJson(self, *args):
        print("Networking - analyzeJson", args[0][1]['headers'])
        for key in args[0][1]['headers']:
            print(' key {}: value {} '.format(key, args[0][1]['headers'][str(key)]))

    def __init__(self, **kwargs):
        super(Networking, self).__init__(**kwargs)
        print("Networking ... ")

    def getJson(self):
        req = UrlRequest('https://maximumroulette.com/', 
        #self.analyzeJson, None, self.on_error ,self.on_error)
            on_error=lambda *args: self.on_error(args),
            on_failure=lambda *args: self.on_failure(args),
            on_redirect=lambda *args: self.on_redirect(args),
            on_success=lambda *args: self.analyzeJson(args) )
        print("get JSON")


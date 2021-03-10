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

    def __init__(self, **kwargs):
        super(Networking, self).__init__(**kwargs)
        print("Networking ... ")
 
        def on_error(error):
            print("Networking - analyzeJson")

        def analyzeJson(req, result):
            print("Networking - analyzeJson")
            for key, value in req.resp_headers.items():
                print('{}: {}'.format(key, value))

    # def access(self):
        req = UrlRequest('https://httpbin.org/headers', analyzeJson, None, on_error)
        print("Networking")

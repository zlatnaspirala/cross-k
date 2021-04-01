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
from kivy.network.urlrequest import UrlRequest

class Networking():

    # Override
    def onAnalyzeJson(self, data):
        print('not overrided.', data)

    def on_error(self, error):
        print("Networking - on_error", error)

    def on_failure(self, error):
        print("Networking - on_failure", error)

    def on_redirect(self, error):
        print("Networking - on_redirect", error)

    def analyzeJson(self, *args):
        # Abstract determination
        print("Networking - analyzeJson args    -> ")
        if (type(args) is tuple) == True:
            for index, item in enumerate(args):
                print(' ---> {} '.format(item))
                if (type(item) is tuple) == True:
                    for sIndex, sItem in enumerate(item):
                        print(' sIndex ', sIndex)
                        print(' sInde ' , sItem)
                        if "<UrlRequest" not in str(sItem):
                            self.callbackAnalyzeJson(sItem)

        else:
            print('net res => Not tuple')
            for key in args:
                print(' key {}: value {} '.format(key, args[str(key)]))

    def __init__(self, **kwargs):
        super(Networking, self).__init__(**kwargs)
        print("[Networking Construct]")

    def getJson(self):
        req = UrlRequest('https://maximumroulette.com/apps/crossk/get-countries/countries.json', 
            on_error=lambda *args: self.on_error(args),
            on_failure=lambda *args: self.on_failure(args),
            on_redirect=lambda *args: self.on_redirect(args),
            on_success=lambda *args: self.analyzeJson(args) )
        print("get JSON")

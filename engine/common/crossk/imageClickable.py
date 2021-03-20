import re
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image, AsyncImage 
from kivy.uix.popup import Popup
from kivy.metrics import dp
from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
import os

class PictureClickable():

    def __init__(self, **kwargs):

        # get any files into images directory
        self.injectWidget = kwargs.get("injectWidget")
        self.accessAssets = kwargs.get("accessAssets")

        #curdir = dirname(__file__)
        assetsPath = os.getcwd()
        print('test this on device on builded app... assetsPath = ', assetsPath)
        # path = os.getcwd()

        print('check congif', self.injectWidget)
        curdir2 =  assetsPath + '/projects/' + self.accessAssets +  '/' + self.accessAssets + '.png'
        picture1 = AsyncImage(source=curdir2, size_hint=(1, 1))

        self.injectWidget.add_widget(picture1)

    def on_pause(self):
        return True

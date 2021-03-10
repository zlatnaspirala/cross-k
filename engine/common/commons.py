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

class Picture():

    def __init__(self, **kwargs):
        # get any files into images directory
        self.injectWidget = kwargs.get("injectWidget")
        self.accessAssets = kwargs.get("accessAssets")
        #curdir = dirname(__file__)
        assetsPath = os.getcwd()
        # backward 
        # path = os.getcwd()
        # print(os.path.abspath(os.path.join(path, os.pardir)))
        curdir2 =  assetsPath + '/engine/assets/' + self.accessAssets +  '/' + self.accessAssets + '.png'
        picture1 = AsyncImage(source=curdir2, size_hint=(1, 1))
        self.injectWidget.add_widget(picture1)

    def on_pause(self):
        return True

def crossKValidateNumbers(txt):
    return re.findall('[^0-9]', txt)

def getAboutGUI():

    box = BoxLayout(
            orientation="vertical")

    infoBtn = Button(markup=True, 
                     text='[b]ok[/b]',
                     font_size=22,
                     size_hint=(1,0.2))
    box.add_widget(Label(
            markup=True, 
            text='[b]maximumroulette.com production[/b]',
            font_size=25,
            size_hint=(1,0.1)
        ))
    Picture(injectWidget=box, accessAssets="logo")
    box.add_widget(Label(markup=True,
        text="""Based on kivy 2.0 python framework. GPL-3.0 License with avavailable source code.
        CrossK is a small but conspiratorial app engine based on kivy opengles2.0 in background.
        
        [b]https://github.com/zlatnaspirala/cross-k[/b]
        Licence:
        Only `Engine source code` is under GPL-3.0.
        - Feel free to use this program.
        - You can sell your crossK generated applications without any licence.
        - Your applications are exempt from any license.
        - Any modification in the engine source code must be shared and available in your 
          about box with next attribution:
          [i]
          CrossK GPL-3.0 License
          [MODIFICATION_SHORT_DESCRIBE]
          [MODIFICATION_ENGINE_SOURCE_LINK]
          [b]https://github.com/zlatnaspirala/cross-k[/b] 
          [/i]

        [b]Credits:[/b]
        https://www.python.org
        https://kivy.org"""))

    box.add_widget(Label(text='Created by zlatnaspirala 2021',
                         font_size=22,
                         size_hint=(1,0.2)
                        ))
    
    box.add_widget(infoBtn)
        
    popup = Popup(title='About CrossK 0.1.0 beta version', content=box, auto_dismiss=False)
    infoBtn.bind(on_press=popup.dismiss)
    popup.open()

def getMessageBoxYesNo(message, msgType, callback):

    box = BoxLayout(orientation="vertical")
    yesBtn = Button(text='YES')
    noBtn = Button(text='NO')
    box.add_widget(Label(text=message))
    box.add_widget(Label(text='Maybe you wanna load project'))
    box.add_widget(Label(text='crossK engine'))

    if (msgType == "OK"):
        yesBtn.text = "OK"
        box.add_widget(yesBtn)
    else:
        box.add_widget(yesBtn)
        box.add_widget(noBtn)

    popup = Popup(title='CrossK MessageBox', content=box, auto_dismiss=False)

    yesBtn.bind(on_press=popup.dismiss)
    noBtn.bind(on_press=popup.dismiss)

    popup.open()

## DEEP 
def deepSearch(arg1 , arg2):
    print("Deep arg 1", arg1)
    print("Deep arg 2", arg2)

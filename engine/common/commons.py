import re
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

def crossKValidateNumbers(txt):
    return re.findall('[^0-9]', txt)

def getAboutGUI():

    box = BoxLayout(orientation="vertical")
    infoBtn = Button(text='CrossK 2d context engine solution')
    box.add_widget(Label(text='Based on kivy 2.0 python framework'))
    box.add_widget(Label(text='mixamumroulette.com production'))
    box.add_widget(Label(text='Created by Nikola Lukic 2021'))
    box.add_widget(infoBtn)
    popup = Popup(title='About CrossK 0.1.0 beta version', content=box, auto_dismiss=False)
    infoBtn.bind(on_press=popup.dismiss)
    popup.open()

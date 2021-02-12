import re
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from engine.common.modifycation import AlignedTextInput
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker

def localCall():
    
    print("works")

# To monitor changes, we can bind to color property changes
def on_color(instance, value):
    print( "RGBA = ", str(value) ) #  or instance.color
    print( "HSV = ", str(instance.hsv))
    print( "HEX = ", str(instance.hex_color))

def addNewButtonGUIOperation():

    content = BoxLayout(orientation="vertical")

    
    clr_picker = ColorPicker()
    
    content.add_widget(Label(text='color'))
    content.add_widget(clr_picker)
    content.add_widget(Label(text='Text'))
    content.add_widget(AlignedTextInput(text='My Button', halign="middle", valign="center"))
    popup = Popup(title='Add new button editor box', content=content, auto_dismiss=False)
    infoBtn = Button(text='Add new button')
    infoBtn.bind(on_press=popup.dismiss)
    content.add_widget(infoBtn)
    clr_picker.bind(color=on_color)
    popup.open()
    localCall()


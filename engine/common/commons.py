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
    box.add_widget(Label(text="""Based on kivy 2.0 python framework. GPL-3.0 License with avavailable source code.
                                 [b]https://github.com/zlatnaspirala/cross-k[b]"""))
    box.add_widget(Label(text='maximumroulette.com production'))
    box.add_widget(Label(text='Created by @zlatnaspirala 2021'))
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

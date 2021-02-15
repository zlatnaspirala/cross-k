import re
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from engine.common.modifycation import AlignedTextInput
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker

class EditorOperationAdd():

    def __init__(self, **kwargs):

        # Definitions
        self.newBtnColor = (0,0,0,1)

        self.store = kwargs.get("store")
        print("Access store -> ", self.store)

        # Prepare content
        content = BoxLayout(orientation="vertical")
        clr_picker = ColorPicker()
        infoBtn = Button(text='Add new button')
        content.add_widget(Label(text='color'))
        content.add_widget(clr_picker)
        content.add_widget(Label(text='Text'))
        content.add_widget(AlignedTextInput(text='My Button', halign="middle", valign="center"))
        content.add_widget(infoBtn)

        # Popup
        self.popup = Popup(title='Add new button editor box', content=content, auto_dismiss=False)

        # Events attach
        clr_picker.bind(color=self.on_color)
        
        # Open popup
        self.popup.open()

        infoBtn2 = Button(text='Add new button', on_press=lambda a:self.oAddBtn(self))
        content.add_widget(infoBtn2)
        
    def oAddBtn(self, instance):
        ####################################################
        # Operation `Add`
        ####################################################
        print("instance on local call -> ", self.newBtnColor)
        calculatedElements = [ "Button(text='0.1.0', color=" + self.newBtnColor + ", size=(60, 100), size_hint=(None, None) )" ]
        self.store.put('renderComponentArray', elements=calculatedElements)
        print("instance on local call -> ", calculatedElements)


        if self.store.exists('renderComponentArray'):
            print('renderComponentArray exists:', self.store.get('renderComponentArray'))
            print('renderComponentArray exists:', self.store.get('renderComponentArray')['elements'])
            #store.delete('tito')
        #for item in self.store.find(name='renderComponentArray'):
        #    print('Looking data intro project files .... ', item)
 

    # To monitor changes, we can bind to color property changes
    def on_color(self, instance, value):
        self.newBtnColor = str(value)
        print( "RGBA = ", str(value) ) #  or instance.color
        print( "HSV = ", str(instance.hsv))
        print( "HEX = ", str(instance.hex_color))

    def operationAdd(self, instance):
        print("Operation add.")
        self.popup.dismiss()

    def addNewButtonGUIOperation(self):
        print("empty")


        # self.localCall()




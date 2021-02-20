import re
import uuid
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from engine.common.modifycation import AlignedTextInput

class EditorOperationAdd():

    def __init__(self, **kwargs):

        # Definitions defaults - config implementation later!
        self.newBtnColor = (0, 0, 0, 1)
        self.newBtnBgColor = (1, 1, 1, 1)
        self.newBtnWidth = 200
        self.newBtnHeight = 80

        self.store = kwargs.get("store")
        self.engineLayout = kwargs.get("engineLayout")
        print("Access store -> ", self.store)

        # Prepare content
        content = BoxLayout(orientation="vertical")
        clrPickerTextColor = ColorPicker()
        clrPickerBackgroundColor = ColorPicker()
        content.add_widget(Label(text='Button Name(Tag)'))
        self.buttonNameText = AlignedTextInput(text='MyButton', halign="middle", valign="center")
        content.add_widget(self.buttonNameText)
        content.add_widget(Label(text='Button background color'))
        content.add_widget(clrPickerBackgroundColor)
        content.add_widget(Label(text='Button text color'))
        content.add_widget(clrPickerTextColor)
        content.add_widget(Label(text='Text'))
        self.buttonText = AlignedTextInput(text='My Button Text', halign="middle", valign="center")
        content.add_widget(self.buttonText)
        content.add_widget(Label(text='Dimensions'))
        self.buttonWidthText = AlignedTextInput(text='200', halign="middle", valign="center")
        content.add_widget(self.buttonWidthText)
        self.buttonHeightText = AlignedTextInput(text='100', halign="middle", valign="center")
        content.add_widget(self.buttonHeightText)

        # Popup
        self.popup = Popup(title='Add new button editor box', content=content, auto_dismiss=False)

        # Events attach
        clrPickerTextColor.bind(color=self.on_color) # pylint: disable=no-member
        clrPickerBackgroundColor.bind(color=self.on_bgcolor) # pylint: disable=no-member
        # Open popup
        self.popup.open()

        # Bind elements
        infoBtn2 = Button(text='Add new button', on_press=lambda a:self.oAddBtn(self))
        content.add_widget(infoBtn2)

    def oAddBtn(self, instance):
        ####################################################
        # Operation `Add`
        ####################################################
        print("instance on local call -> ", self.newBtnColor)


        calculatedButtonData = {
            "id": str(uuid.uuid4()),
            "name": self.buttonNameText.text,
            "type": "BUTTON",
            "text": self.buttonText.text,
            "color": self.newBtnColor,
            "bgColor": self.newBtnBgColor,
            "width": self.buttonWidthText.text,
            "height": self.buttonHeightText.text
        }

        calculatedElement = Button(
            # id=calculatedButtonData,
            text=self.buttonText.text,
            color=self.newBtnColor,
            width=self.buttonWidthText.text,
            height=self.buttonHeightText.text,
            size_hint=(None, None),
            background_normal= '',
            background_color= self.newBtnBgColor
            # size_hint_x size_hint_y
        )

        print("calculatedButtonData on local call -> ", calculatedButtonData)

        localStagedElements = []

        if self.store.exists('renderComponentArray'):
            print('renderComponentArray exists:', self.store.get('renderComponentArray')['elements'])
            
            localStagedElements = self.store.get('renderComponentArray')['elements']
            
            for item in localStagedElements:
                print('Staged element text  -> ', item['text'])
                #print('Staged element color -> ', item.color)
            
            localStagedElements.append(calculatedButtonData)
            #store.delete('tito')

        # Final
        self.store.put('renderComponentArray', elements=localStagedElements)
        
        print(">>>>>>>>>>>>>>>>>>>", calculatedElement)
        self.engineLayout.add_widget(calculatedElement)
        self.popup.dismiss()

    # To monitor changes, we can bind to color property changes
    def on_color(self, instance, value):

        self.newBtnColor = str(value)
        print( "RGBA = ", (value[0], value[1], value[2], 1 )) #  or instance.color
        self.newBtnColor = (value[0], value[1], value[2], 1 )
        print( "HSV = ", str(instance.hsv))
        print( "HEX = ", str(instance.hex_color))

    def on_bgcolor(self, instance, value):

        print( str(value) , ' ,,,,, color')
        print( "RGBA = ", (value[0], value[1], value[2], 1 )) #  or instance.color
        self.newBtnBgColor = (value[0], value[1], value[2], 1 )
        print( "HSV = ", str(instance.hsv))
        print( "HEX = ", str(instance.hex_color))

    def DissmisPopup(self, instance):
        print("Operation add.")
        self.popup.dismiss()

    def updateScene(self):
        print("empty")





import re
import uuid
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.checkbox import CheckBox
from engine.common.modifycation import AlignedTextInput
from kivy.uix.textinput import TextInput

class EditorOperationLabel():

    def __init__(self, **kwargs):

        # Definitions defaults - config implementation later!
        self.newLabelColor = (0, 0, 0, 1)
        self.newLabelBgColor = (1, 1, 1, 1)
        self.newLabelWidth = 200
        self.newLabelHeight = 80

        self.store = kwargs.get("store")
        self.engineLayout = kwargs.get("engineLayout")
        self.engineRoot = kwargs.get("engineRoot")
        print("Access store -> ", self.store)

        # Prepare content
        content = BoxLayout(orientation="vertical", padding=[150,0,150,0])
        clrPickerTextColor = ColorPicker(size_hint=(1, 5))
        clrPickerBackgroundColor = ColorPicker(size_hint=(1, 5))
        content.add_widget(Label(text='Label Name(Tag)'))
        self.buttonNameText = AlignedTextInput(text='MyLabel', halign="middle", valign="center")
        content.add_widget(self.buttonNameText)
        content.add_widget(Label(text='Label background color'))
        content.add_widget(clrPickerBackgroundColor)
        content.add_widget(Label(text='Label text color'))
        content.add_widget(clrPickerTextColor)
        content.add_widget(Label(text='Text'))
        self.buttonText = AlignedTextInput(text='My Label Text', halign="middle", valign="center")
        content.add_widget(self.buttonText)

        content.add_widget(Label(text='Font size'))
        self.fontSizeBtn = AlignedTextInput(text='', halign="middle", valign="center")
        content.add_widget(self.fontSizeBtn)

        # Bold check box
        myCheckBold = BoxLayout()
        myCheckBold.add_widget(Label(text='Use Bold'))
        content.add_widget(myCheckBold)
        self.checkBoxBold = CheckBox()
        myCheckBold.add_widget(self.checkBoxBold)

        self.checkBoxBold.bind(active=self.on_checkbox_bold_active) # pylint disable=no-member


        myCheckDimSys = BoxLayout()
        myCheckDimSys.add_widget(Label(text='Use Pixel Dimensions'))
        content.add_widget(myCheckDimSys)
        self.checkboxDim = CheckBox()
        myCheckDimSys.add_widget(self.checkboxDim)

        self.checkboxDim.bind(active=self.on_checkbox_active) # pylint disable=no-member

        content.add_widget(Label(text='Use Pixel Dimensions'))
        self.buttonWidthText = TextInput(text='200')
        content.add_widget(self.buttonWidthText)
        self.buttonHeightText = TextInput(text='100')
        content.add_widget(self.buttonHeightText)

        myCheckPerSys = BoxLayout()
        myCheckPerSys.add_widget(Label(text='Use Pixel Dimensions'))
        content.add_widget(myCheckPerSys)
        self.checkboxPer = CheckBox(active=True)
        myCheckPerSys.add_widget(self.checkboxPer)
        self.checkboxPer.bind(active=self.on_checkbox_per_active) # pylint disable=no-member

        content.add_widget(Label(text='Use percent dimensions.'))
        self.buttonHintX = TextInput(text='1')
        content.add_widget(self.buttonHintX)
        self.buttonHintY = TextInput(text='1')
        content.add_widget(self.buttonHintY)

        # Popup 
        self.popup = Popup(title='Add new label editor box', content=content, auto_dismiss=False)

        # Events attach
        clrPickerTextColor.bind(color=self.on_color) # pylint: disable=no-member
        clrPickerBackgroundColor.bind(color=self.on_bgcolor) # pylint: disable=no-member
        # Open popup
        self.popup.open()

        # Bind elements
        infoBtn2 = Button(text='Add new label', on_press=lambda a:self.oAdd(self))
        content.add_widget(infoBtn2)

    def oAdd(self, instance):
        ####################################################
        # Operation `Add`
        ####################################################
        print("instance on local call -> ", self.newLabelColor)

        dimensionRole = "pixel"
        if self.checkboxDim.active == True: 
            local_size_hintX = None
            local_size_hintY = None
            print(" SET HINT NONE ")
            # self.buttonHintX.text, self.buttonHintY.text
        elif self.checkboxPer.active == True: 
            print(" SET HINT ")

            if self.buttonHintX.text == "None":
                local_size_hintX = None
            else:
                local_size_hintX = float(self.buttonHintX.text)

            if self.buttonHintY.text == "None":
                local_size_hintY = None
            else:
                local_size_hintY = self.buttonHintY.text
                
            
            dimensionRole = "hint"
        elif self.checkboxCombine.active == True: 
            print(" SET COMBINE ")
            if self.buttonHintX.text == "None":
                local_size_hintX = None
            else:
                local_size_hintX = float(self.buttonHintX.text)

            if self.buttonHintY.text == "None":
                local_size_hintY = None
            else:
                local_size_hintY = self.buttonHintY.text
                
            dimensionRole = "combine"

   
        calculatedLabelData = {
            "id": str(uuid.uuid4()),
            "name": self.buttonNameText.text,
            "type": "LABEL",
            "text": self.buttonText.text,
            "fontSize": self.fontSizeBtn.text,
            "bold": str(self.checkBoxBold.active),
            "color": self.newLabelColor,
            "bgColor": self.newLabelBgColor,
            "width": self.buttonWidthText.text,
            "height": self.buttonHeightText.text,
            "size_hint_x": str(self.buttonHintX.text),
            "size_hint_y": str(self.buttonHintY.text),
            "dimensionRole": dimensionRole
        } 
    

        if self.checkboxPer.active == True: 
            calculatedElement = Label(
                text=self.buttonText.text,
                color=self.newLabelColor,
                font_size=float(self.fontSizeBtn.text),
                #width=self.buttonWidthText.text,
                #height=self.buttonHeightText.text,
                size_hint_x=local_size_hintX,
                size_hint_y=local_size_hintY,
                #background_normal= '',
                #background_color= self.newLabelBgColor
                # size_hint_x size_hint_y
            )
        else:
            calculatedElement = Label(
                text=self.buttonText.text,
                color=self.newLabelColor,
                font_size=self.fontSizeBtn.text,
                width=self.buttonWidthText.text,
                height=self.buttonHeightText.text,
                size_hint_x=local_size_hintX,
                size_hint_y=local_size_hintY,
                #background_normal= '',
                # background_color= self.newLabelBgColor
                # size_hint_x size_hint_y
            )

        print("calculatedLabelData on local call -> ", calculatedLabelData)

        localStagedElements = []

        if self.store.exists('renderComponentArray'):
            print('renderComponentArray exists:', self.store.get('renderComponentArray')['elements'])
            
            localStagedElements = self.store.get('renderComponentArray')['elements']
            
            for item in localStagedElements:
                print('Staged element text  -> ', item['text'])

            localStagedElements.append(calculatedLabelData)
            #store.delete('tito')

        # Final
        self.store.put('renderComponentArray', elements=localStagedElements)
        
        print(">>>>>>>>>>>>>>>>>>>", calculatedElement)
        self.engineLayout.add_widget(calculatedElement)

        self.engineRoot.updateScene(localStagedElements)
        self.engineRoot.sceneGUIContainer.selfUpdate()
        
        self.popup.dismiss()

    def on_color(self, instance, value):
        self.newLabelColor = str(value)
        self.newLabelColor = (value[0], value[1], value[2], 1 )

    def on_bgcolor(self, instance, value):
        self.newLabelBgColor = (value[0], value[1], value[2], 1 )

    def DissmisPopup(self, instance):
        print("Operation add.")
        self.popup.dismiss()

    def on_checkbox_active(instance, value1, value):
        print(" 1 : ", instance)
        print(" 2 ", value1)
        print(" 3 ", value)
        if value:
            print('The dimensions checkbox', value1, 'is active')
            instance.checkboxPer.active = False

        else:
            print('The dimensions checkbox', value1, 'is inactive')

    def on_checkbox_bold_active(instance, value1, value):
        print(" 1 : ", instance)
        print(" 2 ", value1)
        print(" 3 ", value)
        if value:
            print('The bold checkbox', value1, 'is active')
            # instance.checkboxPer.active = False

        else:
            print('The bold checkbox', value1, 'is inactive')

    def on_checkbox_per_active(instance, value1, value):
        print(" input percent ", value)
        print(" acess ", instance)
        if value:
            print('The dimensions checkbox', value1, 'is active')
            instance.checkboxDim.active = False
        else:
            print('The dimensions checkbox', value1, 'is inactive')


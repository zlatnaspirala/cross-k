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

class EditorOperationButton():

    def __init__(self, **kwargs):

        # Definitions defaults - config implementation later!
        self.newBtnColor = (0, 0, 0, 1)
        self.newBtnBgColor = (1, 1, 1, 1)
        self.newBtnWidth = 200
        self.newBtnHeight = 80

        self.store = kwargs.get("store")
        self.currentLayout = kwargs.get("currentLayout")

        self.engineRoot = kwargs.get("engineRoot")
        print("Access store -> ", self.store)

        # Prepare content
        content = BoxLayout(orientation="vertical", padding=[150,0,150,0])
        clrPickerTextColor = ColorPicker(size_hint=(1, 5))
        clrPickerBackgroundColor = ColorPicker(size_hint=(1, 5))
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

        myCheckDimSys = BoxLayout()
        myCheckDimSys.add_widget(Label(text='Use Pixel Dimensions'))
        content.add_widget(myCheckDimSys)
        self.checkboxDim = CheckBox()
        myCheckDimSys.add_widget(self.checkboxDim)

        self.checkboxDim.bind(active=self.on_checkbox_active) # pylint disable=no-member
        #partial(self.saveDetails, 

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
        self.popup = Popup(title='Add new button editor box', content=content, auto_dismiss=False)

        # Events attach
        clrPickerTextColor.bind(color=self.on_color) # pylint: disable=no-member
        clrPickerBackgroundColor.bind(color=self.on_bgcolor) # pylint: disable=no-member
        # Open popup
        self.popup.open()

        # Bind elements
        infoBtn2 = Button(text='Add new button', on_press=lambda a:self.oAddBtn(self))
        content.add_widget(infoBtn2)


    def __add_elementar(self, localStagedElements, calculatedLabelData):

        print('add btn elemntar')
        founded = False
        for index, item in enumerate(localStagedElements):
            if item['type'] == 'LAYOUT' and item['id'] == self.currentLayout:
                print('FOUNDED')
                founded = True
                localStagedElements[index]['elements'].append(calculatedLabelData)
                break

        if founded == True:
            return True

        for index, item in enumerate(localStagedElements):
            if item['type'] == 'LAYOUT':
                print('SEARCH LAYOUT', item['id'])
                for subIndex, sub in enumerate(item['elements']):
                    if item['type'] == 'LAYOUT' and sub['id'] == self.currentLayout:
                        founded = True
                        localStagedElements[index]['elements'][subIndex].append(calculatedLabelData)
                        return founded
                        break

        print("founded return ", founded)
        return founded


    def oAddBtn(self, instance):
        ####################################################
        # Operation `Add`
        ####################################################
        print("instance on local call -> ", self.newBtnColor)

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

   
        calculatedButtonData = {
            "id": str(uuid.uuid4()),
            "name": self.buttonNameText.text,
            "type": "BUTTON",
            "text": self.buttonText.text,
            "color": self.newBtnColor,
            "bgColor": self.newBtnBgColor,
            "width": self.buttonWidthText.text,
            "height": self.buttonHeightText.text,
            "size_hint_x": str(self.buttonHintX.text),
            "size_hint_y": str(self.buttonHintY.text),
            "dimensionRole": dimensionRole
        } 

        print("calculatedButtonData on local call -> ", calculatedButtonData)
        localStagedElements = []

        if self.store.exists('renderComponentArray'):
            print('renderComponentArray exists:', self.store.get('renderComponentArray')['elements'])
            localStagedElements = self.store.get('renderComponentArray')['elements']
            if self.currentLayout == 'SCENE_ROOT':
                localStagedElements.append(calculatedButtonData)
            else:
                self.__add_elementar(localStagedElements, calculatedButtonData)

                print("AFTER ADD LEMENTAR")
 
            # store.delete('')

        # Final
        self.store.put('renderComponentArray', elements=localStagedElements)
        
        # print(">>>>>>>>>>>>>>>>>>>", calculatedElement)
        # self.currentLayout.add_widget(calculatedElement)
        
        self.popup.dismiss()

        self.engineRoot.updateScene()
        self.engineRoot.sceneGUIContainer.selfUpdate()

    # To monitor changes, we can bind to color property changes
    def on_color(self, instance, value):

        self.newBtnColor = str(value)
        # print( "RGBA = ", (value[0], value[1], value[2], 1 )) #  or instance.color
        self.newBtnColor = (value[0], value[1], value[2], 1 )
        # print( "HSV = ", str(instance.hsv))
        # print( "HEX = ", str(instance.hex_color))

    def on_bgcolor(self, instance, value):

        print( str(value) , ' ,,,,, color')
        # print( "RGBA = ", (value[0], value[1], value[2], 1 )) #  or instance.color
        self.newBtnBgColor = (value[0], value[1], value[2], 1 )
        # print( "HSV = ", str(instance.hsv))
        # print( "HEX = ", str(instance.hex_color))

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

    def on_checkbox_per_active(instance, value1, value):
        print(" input percent ", value)
        print(" acess ", instance)
        if value:
            print('The dimensions checkbox', value1, 'is active')
            instance.checkboxDim.active = False
        else:
            print('The dimensions checkbox', value1, 'is inactive')


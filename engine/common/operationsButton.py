import re
import uuid
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
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
        content = GridLayout( cols=2, padding=[150,0,150,0], spacing=1)
        clrPickerTextColor = ColorPicker(size_hint=(1, 3))
        clrPickerBackgroundColor = ColorPicker(size_hint=(1, 3))
        content.add_widget(Label(text='Button Name(Tag)', size_hint=(1,None),
                height=30))
        self.buttonNameText = TextInput(text='MyButton', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.buttonNameText)

        content.add_widget(Label(text='Text', size_hint=(1,None),
                height=30))
        self.buttonText = TextInput(text='My Button Text', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.buttonText)

        content.add_widget(Label(text='Font size',  size_hint=(1,None),
                height=30))
        self.fontSizeBtn = TextInput(text='18', halign="center",  size_hint=(1,None),
                height=30)
        content.add_widget(self.fontSizeBtn)
        
        content.add_widget(Label(text='Button background color'))
        content.add_widget(clrPickerBackgroundColor)
        content.add_widget(Label(text='Button text color'))
        content.add_widget(clrPickerTextColor)
        

        content.add_widget(Label(text='Position X in pixels', size_hint=(1,None),
                height=30))
        self.buttonPositionX = TextInput(text='0', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.buttonPositionX)
        content.add_widget(Label(text='Position Y in pixels', size_hint=(1,None),
                height=30))
        self.buttonPositionY = TextInput(text='0', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.buttonPositionY)

        content.add_widget(Label(text='Position Hint X', size_hint=(1,None),
                height=30))
        self.buttonPositionHintX = TextInput(text='0', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.buttonPositionHintX)
        content.add_widget(Label(text='Position Hint Y', size_hint=(1,None),
                height=30))
        self.buttonPositionHintY = TextInput(text='0', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.buttonPositionHintY)

        # myCheckDimSys = BoxLayout(size_hint=(1,None),
        #        height=30)
        content.add_widget(Label(text='Use Pixel Dimensions', size_hint=(1,None),
                height=30))
        # content.add_widget(myCheckDimSys)
        self.checkboxDim = CheckBox(size_hint=(1,None),
                height=30)
        content.add_widget(self.checkboxDim)

        self.checkboxDim.bind(active=self.on_checkbox_active) # pylint disable=no-member

        #content.add_widget(Label(text='Use Pixel Dimensions Width', size_hint=(1,None),
        #        height=30))

        content.add_widget(Label(text='Width', size_hint=(1,None),
                height=30))

        self.buttonWidthText = TextInput(text='200', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.buttonWidthText)

        content.add_widget(Label(text='Height', size_hint=(1,None),
        height=30))

        self.buttonHeightText = TextInput(text='100', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.buttonHeightText)

        # myCheckPerSys = BoxLayout(size_hint=(1,None),
        #        height=30)
        content.add_widget(Label(text='Use Percent Dimensions range[0-1]', size_hint=(1,None),
                height=30))
        # content.add_widget(myCheckPerSys)
        self.checkboxPer = CheckBox(active=True, size_hint=(1,None),
                height=30)
        content.add_widget(self.checkboxPer)
        self.checkboxPer.bind(active=self.on_checkbox_per_active) # pylint disable=no-member

        #content.add_widget(Label(text='Use percent dimensions. Use 0.2 is 20%\ of parent width/height ', size_hint=(1,None),
        #        height=30))

        content.add_widget(Label(text='Width in percent range[0-1]', size_hint=(1,None),
                height=30))

        self.buttonHintX = TextInput(text='1', halign="center",size_hint=(1,None),
                height=30)
        content.add_widget(self.buttonHintX)

        content.add_widget(Label(text='Height in percent range[0-1]', size_hint=(1,None),
                height=30))
        self.buttonHintY = TextInput(text='1', halign="center",size_hint=(1,None),
                height=30)
        content.add_widget(self.buttonHintY)

        self.attachEventCurrentElement = Label(
                text="print('recommended edit from details box')",
                size_hint=(1,None),
                height=30
            )
        content.add_widget(self.attachEventCurrentElement)

        content.add_widget( TextInput(
                text='print("ATTACH EVENT WORKS")',
                size_hint=(1,None),
                height=30
              ))

        # Popup
        self.popup = Popup(title='Add new button editor box', content=content, auto_dismiss=False)

        # Events attach
        clrPickerTextColor.bind(color=self.on_color) # pylint: disable=no-member
        clrPickerBackgroundColor.bind(color=self.on_bgcolor) # pylint: disable=no-member

        # Open popup
        self.popup.open()

        # Bind elements
        infoBtn2 = Button(
            text='Add new button', 
            size_hint=(1, None), height=70,
            font_size=18,
            background_normal= '',
            background_color=(self.engineRoot.engineConfig.getThemeCustomColor('engineBtnsBackground')),
            color=self.engineRoot.engineConfig.getThemeTextColor(),
            on_press=lambda a:self.oAddBtn(self))
        content.add_widget(infoBtn2)

        cancelBtn = Button(
            text='Cancel',
            font_size=18,
            size_hint=(1, None), height=70,
            background_normal= '',
            background_color=(self.engineRoot.engineConfig.getThemeCustomColor('engineBtnsBackground')),
            color=self.engineRoot.engineConfig.getThemeTextColor(),
            on_press=lambda a:self.closePopup(self))
        content.add_widget(cancelBtn)

    def closePopup(self, instance):
        self.popup.dismiss()

    def _add(self,localStagedElements, calculatedLabelData, currentLayoutId ):
        for index, item in enumerate(localStagedElements):
            if item['id'] == currentLayoutId:
                localStagedElements[index]['elements'].append(calculatedLabelData)
                return localStagedElements
                break
            if item['type'] == 'LAYOUT':
                self._add(item['elements'], calculatedLabelData, currentLayoutId )
        return False

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
            "fontSize": self.fontSizeBtn.text,
            "pos_x": self.buttonPositionX.text,
            "pos_y": self.buttonPositionY.text,
            "pos_hint_x": self.buttonPositionHintX.text,
            "pos_hint_y": self.buttonPositionHintY.text,
            "color": self.newBtnColor,
            "bgColor": self.newBtnBgColor,
            "width": self.buttonWidthText.text,
            "height": self.buttonHeightText.text,
            "size_hint_x": str(self.buttonHintX.text),
            "size_hint_y": str(self.buttonHintY.text),
            "dimensionRole": dimensionRole,
            "attacher": self.attachEventCurrentElement.text
        }

        print("calculatedButtonData call -> ", calculatedButtonData)
        localStagedElements = []

        if self.store.exists('renderComponentArray'):
            localStagedElements = self.store.get('renderComponentArray')['elements']
            if self.currentLayout == 'SCENE_ROOT':
                localStagedElements.append(calculatedButtonData)
            else:
                TEST = self._add(localStagedElements, calculatedButtonData , self.currentLayout)
                print("AFTER ADD ELEMENTAR", TEST)

        # Final
        self.store.put('renderComponentArray', elements=localStagedElements)
        self.popup.dismiss()
        self.engineRoot.updateScene()
        self.engineRoot.sceneGUIContainer.selfUpdate()
        self.engineRoot.closeWithNoSaveDetails(None)

    def on_color(self, instance, value):
        self.newBtnColor = str(value)
        self.newBtnColor = (value[0], value[1], value[2], 1 )

    def on_bgcolor(self, instance, value):
        self.newBtnBgColor = (value[0], value[1], value[2], 1 )
        # print( "RGBA = ", (value[0], value[1], value[2], 1 ))
        # print( "HSV = ", str(instance.hsv))
        # print( "HEX = ", str(instance.hex_color))

    def DissmisPopup(self, instance):
        print("Operation add.")
        self.popup.dismiss()

    def on_checkbox_active(instance, value1, value):
        if value:
            print('The dimensions checkbox', value1, 'is active')
            instance.checkboxPer.active = False
        else:
            print('The dimensions checkbox', value1, 'is inactive')

    def on_checkbox_per_active(instance, value1, value):
        if value:
            print('The dimensions checkbox', value1, 'is active')
            instance.checkboxDim.active = False
        else:
            print('The dimensions checkbox', value1, 'is inactive')


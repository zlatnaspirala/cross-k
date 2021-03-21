
import re
import uuid
from os.path import join, dirname, expanduser
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.checkbox import CheckBox
from engine.common.modifycation import AlignedTextInput
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.utils import platform

class EditorOperationPicture():

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
        content = GridLayout( cols=2, padding=[100,0,100,0])
        clrPickerTextColor = ColorPicker(size_hint=(1, 3))
        clrPickerBackgroundColor = ColorPicker(size_hint=(1, 3))
        content.add_widget(Label(text='Picture Name(Tag)', size_hint=(1,None),
                height=30))
        self.pictureNameText = TextInput(text='MyPicture', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.pictureNameText)

        if platform == 'win':
            user_path = dirname(expanduser('~')) + '\\' + 'Documents'
        else:
            user_path = expanduser('~') + '/' + 'Documents'
        browser = FileChooserListView(# select_string='Select', dirselect: True
              path=self.engineRoot.engineConfig.currentProjectName + '/data/',
              size_hint=(1,3)
           )
        content.add_widget(browser)
        browser.bind(
                    on_success=self._fbrowser_success,
                    on_canceled=self._fbrowser_canceled)

        content.add_widget(Label(text='[Over Picture] Text: empty default', size_hint=(1,None),
                height=30))
        self.pictureText = TextInput(text='', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.pictureText)

        content.add_widget(Label(text='Font size',  size_hint=(1,None),
               height=30))
        self.fontSizeBtn = TextInput(text='18', halign="center",  size_hint=(1,None),
                height=30)
        content.add_widget(self.fontSizeBtn)
        
        content.add_widget(Label(text='Picture background color'))
        content.add_widget(clrPickerBackgroundColor)
        content.add_widget(Label(text='Over Picture Text color'))
        content.add_widget(clrPickerTextColor)

        content.add_widget(Label(text='Position X in pixels', size_hint=(1,None),
                height=30))
        self.picturePositionX = TextInput(text='0', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.picturePositionX)
        content.add_widget(Label(text='Position Y in pixels', size_hint=(1,None),
                height=30))
        self.picturePositionY = TextInput(text='0', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.picturePositionY)

        content.add_widget(Label(text='Position Hint X', size_hint=(1,None),
                height=30))
        self.picturePositionHintX = TextInput(text='0', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.picturePositionHintX)
        content.add_widget(Label(text='Position Hint Y', size_hint=(1,None),
                height=30))
        self.picturePositionHintY = TextInput(text='0', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.picturePositionHintY)

        myCheckDimSys = BoxLayout(size_hint=(1,None),
                height=30)
        myCheckDimSys.add_widget(Label(text='Use Pixel Dimensions', size_hint=(1,None),
                height=30))
        content.add_widget(myCheckDimSys)
        self.checkboxDim = CheckBox(size_hint=(1,None),
                height=30)
        myCheckDimSys.add_widget(self.checkboxDim)

        self.checkboxDim.bind(active=self.on_checkbox_active) # pylint disable=no-member

        content.add_widget(Label(text='Use Pixel Dimensions', size_hint=(1,None),
                height=30))

        content.add_widget(Label(text='Width', size_hint=(1,None),
                height=30))

        self.pictureWidthText = TextInput(text='200', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.pictureWidthText)

        content.add_widget(Label(text='Height', size_hint=(1,None),
        height=30))

        self.pictureHeightText = TextInput(text='100', halign="center", size_hint=(1,None),
                height=30)
        content.add_widget(self.pictureHeightText)

        myCheckPerSys = BoxLayout(size_hint=(1,None),
                height=30)
        myCheckPerSys.add_widget(Label(text='Use Percent Dimensions range[0-1]', size_hint=(1,None),
                height=30))
        content.add_widget(myCheckPerSys)
        self.checkboxPer = CheckBox(active=True, size_hint=(1,None),
                height=30)
        myCheckPerSys.add_widget(self.checkboxPer)
        self.checkboxPer.bind(active=self.on_checkbox_per_active) # pylint disable=no-member

        content.add_widget(Label(text='Use percent dimensions. Use 0.2 is 20%\ of parent width/height ', size_hint=(1,None),
                height=30))

        content.add_widget(Label(text='Width in percent range[0-1]', size_hint=(1,None),
                height=30))

        self.pictureHintX = TextInput(text='1', halign="center",size_hint=(1,None),
                height=30)
        content.add_widget(self.pictureHintX)

        content.add_widget(Label(text='Height in percent range[0-1]', size_hint=(1,None),
                height=30))
        self.pictureHintY = TextInput(text='1', halign="center",size_hint=(1,None),
                height=30)
        content.add_widget(self.pictureHintY)

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
        self.popup = Popup(title='Add new PictureClickable editor box', content=content, auto_dismiss=False)

        # Events attach
        clrPickerTextColor.bind(color=self.on_color) # pylint: disable=no-member
        clrPickerBackgroundColor.bind(color=self.on_bgcolor) # pylint: disable=no-member

        # Open popup
        self.popup.open()

        # Bind elements
        infoBtn2 = Button(
            text='Add new picture', 
            font_size=18,
            background_normal= '',
            background_color=(self.engineRoot.engineConfig.getThemeBackgroundColor()),
            color=self.engineRoot.engineConfig.getThemeTextColor(),
            on_press=lambda a:self.oAddPicture(self))
        content.add_widget(infoBtn2)

        cancelBtn = Button(
            text='Cancel',
            font_size=18,
            background_normal= '',
            background_color=(self.engineRoot.engineConfig.getThemeBackgroundColor()),
            color=self.engineRoot.engineConfig.getThemeTextColor(),
            on_press=lambda a:self.closePopup(self))
        content.add_widget(cancelBtn)

    def _fbrowser_canceled(self, instance):
        print ('cancelled, Close self.')

    def _fbrowser_success(self, instance):
        print (instance.selection)

    def closePopup(self, instance):
        self.popup.dismiss()

    def __add_elementar(self, localStagedElements, calculatedLabelData):
        # print('add btn elemntar')
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
                        localStagedElements[index]['elements'][subIndex]['elements'].append(calculatedLabelData)
                        return founded
                        break

        # print("founded return ", founded)
        return founded

    def oAddPicture(self, instance):
        ####################################################
        # Operation `Add`
        ####################################################
        print("instance on local call -> ", self.newBtnColor)

        dimensionRole = "pixel"
        if self.checkboxDim.active == True: 
            local_size_hintX = None
            local_size_hintY = None
            print(" SET HINT NONE ")
            # self.pictureHintX.text, self.pictureHintY.text
        elif self.checkboxPer.active == True: 
            print(" SET HINT ")

            if self.pictureHintX.text == "None":
                local_size_hintX = None
            else:
                local_size_hintX = float(self.pictureHintX.text)

            if self.pictureHintY.text == "None":
                local_size_hintY = None
            else:
                local_size_hintY = self.pictureHintY.text

            dimensionRole = "hint"
        elif self.checkboxCombine.active == True: 
            print(" SET COMBINE ")
            if self.pictureHintX.text == "None":
                local_size_hintX = None
            else:
                local_size_hintX = float(self.pictureHintX.text)

            if self.pictureHintY.text == "None":
                local_size_hintY = None
            else:
                local_size_hintY = self.pictureHintY.text

            dimensionRole = "combine"

        calculatedButtonData = {
            "id": str(uuid.uuid4()),
            "name": self.pictureNameText.text,
            "type": "PICTURE_CLICKABLE",
            "image": 'engine/assets/nidzaBorder002.png',
            "text": self.pictureText.text,
            "fontSize": self.fontSizeBtn.text,
            "pos_x": self.picturePositionX.text,
            "pos_y": self.picturePositionY.text,
            "pos_hint_x": self.picturePositionHintX.text,
            "pos_hint_y": self.picturePositionHintY.text,
            "color": self.newBtnColor,
            "bgColor": self.newBtnBgColor,
            "width": self.pictureWidthText.text,
            "height": self.pictureHeightText.text,
            "size_hint_x": str(self.pictureHintX.text),
            "size_hint_y": str(self.pictureHintY.text),
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
                self.__add_elementar(localStagedElements, calculatedButtonData)

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


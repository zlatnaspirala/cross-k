import re
import uuid
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
#Anchor layout:
from kivy.uix.anchorlayout import AnchorLayout
#Box layout: 
from kivy.uix.boxlayout import BoxLayout
#Float layout:
from kivy.uix.floatlayout import FloatLayout
#Grid layout:
from kivy.uix.gridlayout import GridLayout
#Page Layout:
from kivy.uix.pagelayout import PageLayout
#Relative layout:
from kivy.uix.relativelayout import RelativeLayout
#Scatter layout:
from kivy.uix.scatterlayout import ScatterLayout
# Stack layout: 
from kivy.uix.stacklayout import StackLayout
from engine.common.modifycation import AlignedTextInput
from functools import partial

class EditorOperationBox():

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
        clrPickerTextColor = ColorPicker(size_hint=(1, 1))
        clrPickerBackgroundColor = ColorPicker(size_hint=(1, 1))
        
        content.add_widget(Label(text='Layout Name(Tag)'))
        self.buttonNameText = TextInput(text='MyBoxLayout')
        content.add_widget(self.buttonNameText)

        content.add_widget(Label(text='Layout Type(Visual type)'))
        # self.buttonNameText = AlignedTextInput(text='utton', halign="middle", valign="center")

        self.layoutTypeList = DropDown()
        self.selectBtn = Button(text='Box', on_press=self.layoutTypeList.open)
        content.add_widget(self.selectBtn)

        self.layoutTypeList.dismiss()
        
        #Anchor layout:
        #Box layout: 
        #Float layout:
        #Grid layout:
        #Page Layout:
        #Relative layout:
        #Scatter layout:
        # Stack layout: 

        self.btnBox = Button(text='Box', size_hint_y=None, height=44 )
        self.btnBox.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnBox)

        self.btnFloat = Button(text='Float', size_hint_y=None, height=44)
        self.btnFloat.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnFloat)

        self.btnGrid = Button(text='Grid', size_hint_y=None, height=44)
        self.btnGrid.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnGrid)

        self.btnPage = Button(text='Page', size_hint_y=None, height=44)
        self.btnPage.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnPage)

        self.btnRelative = Button(text='Relative', size_hint_y=None, height=44)
        self.btnRelative.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnRelative)

        self.btnScatter = Button(text='Scatter', size_hint_y=None, height=44)
        self.btnScatter.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnScatter)

        self.btnStack = Button(text='Stack', size_hint_y=None, height=44)
        self.btnStack.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnStack)

        content.add_widget(self.layoutTypeList)


        colorHolder = BoxLayout(size_hint=(1,None), height=160)
        content.add_widget(colorHolder)

        colorHolder.add_widget(Label(text='Button background color'))
        colorHolder.add_widget(clrPickerBackgroundColor)
        colorHolder.add_widget(Label(text='Button text color'))
        colorHolder.add_widget(clrPickerTextColor)


        content.add_widget(Label(text='Orientation'))
        self.orientation = TextInput(text='vertical')
        content.add_widget(self.orientation)

        content.add_widget(Label(text='Padding'))
        self.layoutPadding = TextInput(text='0')
        content.add_widget(self.layoutPadding)

        content.add_widget(Label(text='Spacing'))
        self.layoutSpacing = TextInput(text="0")
        content.add_widget(self.layoutSpacing)

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
        self.popup = Popup(title='Add new layout editor box', content=content, auto_dismiss=False)

        # Events attach
        clrPickerTextColor.bind(color=self.on_color) # pylint: disable=no-member
        clrPickerBackgroundColor.bind(color=self.on_bgcolor) # pylint: disable=no-member
        # Open popup
        self.popup.open()

        # Bind elements
        commitBtn = Button(
            text='Add new Layout',
            size_hint=(1, None),
            height=88,
            on_press=lambda a:self.oAddBox(self)
        )
        content.add_widget(commitBtn)

    def __setLayoutType(self, instance):
        print("__setLayoutType", instance)
        self.selectBtn.text = instance.text
        self.layoutTypeList.select(self.btnBox.text)

    def oAddBox(self, instance):
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
            "type": "LAYOUT",
            "layoutType": self.selectBtn.text,
            "elements": [],
            "orientation": self.orientation.text,
            "padding": self.layoutPadding.text,
            "spacing": self.layoutSpacing.text,
            "color": self.newBtnColor,
            "bgColor": self.newBtnBgColor,
            "width": self.buttonWidthText.text,
            "height": self.buttonHeightText.text,
            "size_hint_x": str(self.buttonHintX.text),
            "size_hint_y": str(self.buttonHintY.text),
            "dimensionRole": dimensionRole
        } 

        if self.checkboxPer.active == True: 
            print('what is the type of layout', self.selectBtn.text)

        # print("Attacher internal Attacher.uid ID -> ", Attacher.uid)

        localStagedElements = []

        if self.store.exists('renderComponentArray'):
            print('renderComponentArray exists:', self.store.get('renderComponentArray')['elements'])
            
            localStagedElements = self.store.get('renderComponentArray')['elements']
            
            for item in localStagedElements:
                print('A')

            localStagedElements.append(calculatedButtonData)
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


import re
import uuid
from functools import partial
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stacklayout import StackLayout
from engine.common.modifycation import AlignedTextInput

class EditorOperationBox():

    def __init__(self, **kwargs):

        # Definitions defaults - config implementation later!
        self.newBtnColor = (0, 0, 0, 1)
        self.newBtnBgColor = (1, 1, 1, 1)
        self.newBtnWidth = 200
        self.newBtnHeight = 80

        self.store = kwargs.get("store")
        self.currentLayoutId = kwargs.get("currentLayoutId")

        self.engineRoot = kwargs.get("engineRoot")
        print("Access currentLayoutId -> ", self.currentLayoutId)

        # Prepare content
        content = GridLayout(orientation="lr-tb", padding=[150,0,150,0], cols=2)
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

        self.btnAnchor = Button(text='Anchor', size_hint_y=None, height=44) 
        self.btnAnchor.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnAnchor)

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

        colorHolderT = BoxLayout(size_hint=(1,None), height=160)
        content.add_widget(colorHolderT)

        colorHolderT.add_widget(Label(text='Button text color'))
        colorHolderT.add_widget(clrPickerTextColor)

        content.add_widget(Label(text='Orientation'))
        self.orientation = TextInput(text='vertical')
        content.add_widget(self.orientation)

        content.add_widget(Label(text='cols'))
        self.colsInput = TextInput(text='6')
        content.add_widget(self.colsInput)

        content.add_widget(Label(text='rows'))
        self.rowsInput = TextInput(text='0')
        content.add_widget(self.rowsInput)


        content.add_widget(Label(text='Padding'))
        self.layoutPadding = TextInput(text='0')
        content.add_widget(self.layoutPadding)

        content.add_widget(Label(text='Spacing'))
        self.layoutSpacing = TextInput(text="0")
        content.add_widget(self.layoutSpacing)

        #myCheckDimSys = BoxLayout()
        content.add_widget(Label(text='Use Pixel Dimensions'))
        #content.add_widget(myCheckDimSys)
        self.checkboxDim = CheckBox()
        content.add_widget(self.checkboxDim)

        self.checkboxDim.bind(active=self.on_checkbox_active) # pylint disable=no-member

        content.add_widget(Label(text='Use Pixel For Width'))
        self.buttonWidthText = TextInput(text='200')
        content.add_widget(self.buttonWidthText)
        content.add_widget(Label(text='Use Pixel For Height'))
        self.buttonHeightText = TextInput(text='100')
        content.add_widget(self.buttonHeightText)

        #myCheckPerSys = BoxLayout()
        content.add_widget(Label(text='Use Percent Dimensions'))
        #content.add_widget(myCheckPerSys)
        self.checkboxPer = CheckBox(active=True)
        content.add_widget(self.checkboxPer)
        self.checkboxPer.bind(active=self.on_checkbox_per_active) # pylint disable=no-member

        content.add_widget(Label(text='Use percent dimensions range(0 - 1). Width'))
        self.buttonHintX = TextInput(text='1')
        content.add_widget(self.buttonHintX)
        content.add_widget(Label(text='Use percent dimensions range(0 - 1). Height'))
        self.buttonHintY = TextInput(text='1')
        content.add_widget(self.buttonHintY)

        content.add_widget(Label(text='Position X in pixels'))
        self.buttonPositionX = TextInput(text='0', halign="center")
        content.add_widget(self.buttonPositionX)
        content.add_widget(Label(text='Position Y in pixels'))
        self.buttonPositionY = TextInput(text='0', halign="center")
        content.add_widget(self.buttonPositionY)

        content.add_widget(Label(text='Position Hint X'))
        self.buttonPositionHintX = TextInput(text='0', halign="center")
        content.add_widget(self.buttonPositionHintX)
        content.add_widget(Label(text='Position Hint Y'))
        self.buttonPositionHintY = TextInput(text='0', halign="center")
        content.add_widget(self.buttonPositionHintY)

        # Popup
        self.popup = Popup(title='Add new Layout editor box', content=content, auto_dismiss=False)

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
            color=self.engineRoot.engineConfig.getThemeTextColor(),
            background_color=(self.engineRoot.engineConfig.getThemeCustomColor('engineBtnsBackground')),
            on_press=lambda a:self.oAddBox(self)
        )
        content.add_widget(commitBtn)

        cancelBtn = Button(
            text='Cancel',
            size_hint=(1, None),
            height=88,
            color=self.engineRoot.engineConfig.getThemeTextColor(),
            background_color=(self.engineRoot.engineConfig.getThemeCustomColor('engineBtnsBackground')),
            on_press=lambda a:self.DissmisPopup(self)
        )
        content.add_widget(cancelBtn)

    def __setLayoutType(self, instance):
        print("__setLayoutType", instance)
        self.selectBtn.text = instance.text
        self.layoutTypeList.select(self.btnBox.text)

    def _add(self,localStagedElements, calculatedButtonData, currentLayoutId ):
        for index, item in enumerate(localStagedElements):
            if item['id'] == currentLayoutId:
                localStagedElements[index]['elements'].append(calculatedButtonData)
                return localStagedElements
                break
            if item['type'] == 'LAYOUT':
                self._add(item['elements'], calculatedButtonData, currentLayoutId )
        return False

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

        #if str(detailData['layoutType']) == "Anchor" or str(detailData['layoutType']) == "Float":
            #localAnchor_x = self.selectAnchor.text
            #localAnchor_y = self.selectAnchorY.text
        #else:

        localAnchor_x = 'center'
        localAnchor_y = 'center'

        calculatedButtonData = {
            "id": str(uuid.uuid4()),
            "name": self.buttonNameText.text,
            "type": "LAYOUT",
            "cols": self.colsInput.text,
            "rows": self.rowsInput.text,
            "pos_x": self.buttonPositionX.text,
            "pos_y": self.buttonPositionY.text,
            "pos_hint_x": self.buttonPositionHintX.text,
            "pos_hint_y": self.buttonPositionHintY.text,
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
            "dimensionRole": dimensionRole,
            "anchor_x": localAnchor_x,
            "anchor_y": localAnchor_y,
            "swipe_threshold": str(0.4)
        } 

        # print('what is the type of layout', self.selectBtn.text)
        localStagedElements = []

        if self.store.exists('renderComponentArray'):
            # print('renderComponentArray exists:', self.store.get('renderComponentArray')['elements'])
            localStagedElements = self.store.get('renderComponentArray')['elements']
            #######################
            # First just root
            if self.currentLayoutId == None:
                localStagedElements.append(calculatedButtonData)
            else:
                self._add(localStagedElements, calculatedButtonData , self.currentLayoutId)

        # Final
        self.store.put('renderComponentArray', elements=localStagedElements)

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


#################################################
# Manual creation.
# Optimized editor_main.py
# 0.1.0 Beta
#################################################

from builtins import chr
import os
import threading
import uuid

import kivy
from kivy.config import Config

print(kivy.__version__)
kivy.require('2.0.0')

from functools import partial
from kivy.utils import platform
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.metrics import dp, sp, pt
from kivy.core.window import Window
from kivy.uix.image import Image, AsyncImage 
from kivy.uix.textinput import TextInput
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.storage.jsonstore import JsonStore
from kivy.app import App
from kivy.graphics import Color, Rectangle
from engine.editor.layout import EngineLayout
from engine.editor.sceneGUIContainer import SceneGUIContainer
from engine.editor.scripter import EventsEngineLayout
from engine.config import EngineConfig
from engine.common.modifycation import AlignedTextInput
from engine.common.commons import getAboutGUI, getMessageBoxYesNo
from engine.common.operationsButton import EditorOperationButton
from engine.common.operationsLabel import EditorOperationLabel
from engine.common.operationsBox import EditorOperationBox
from engine.common.enginePackage import PackagePopup

print("Current platform :", platform)
print("Application Part Running")

if (platform == 'win'):
    from win32api import GetSystemMetrics

# Editor main is only editor not inpact projects files.
class EditorMain(BoxLayout):

    def loadProjectFiles(self):

        CURRENT_PATH = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../projects/' + self.pack + '/')
        )
        if not os.path.exists(CURRENT_PATH):
            getMessageBoxYesNo(
                "Not exist project with name `' + self.pack + '`. Please look at /projects/ root folder. Subfolder name is project name.",
                "OK",
                "null"
            )
            return 0
            

        # print("LOAD PROJECT PROCEDURE")
        ###############################################################
        # App root layout instance
        ###############################################################
        self.engineLayout = EngineLayout(orientation="vertical")

        # Step : runtime setup project global data.
        # ProjectName and ProjectPath root , also setup config.
        self.engineConfig.currentProjectName = "' + self.pack + '"
        self.engineConfig.currentProjectPath = CURRENT_PATH
        self.engineLayout.currentProjectPath=self.engineConfig.currentProjectPath
        self.engineLayout.currentProjectName=self.engineConfig.currentProjectName

        # help
        self.fullProjectStorePath = self.engineLayout.currentProjectPath + '/' + self.pack + '.json'
        # print("Project name:", self.engineConfig.currentProjectName )
        # print("Project root:", self.engineConfig.currentProjectPath )
        self.add_widget(self.engineLayout)
        # Loading
        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.pack + '.json')
        loadElements = self.store.get('renderComponentArray')['elements']
        self.updateScene()

    def packageWinApp(self, instance):
        test = PackagePopup(engineConfig=self.engineConfig)
        print("Package application for windows started")

    def __init__(self, **kwargs):
        super(EditorMain, self).__init__()

        self.pack = kwargs.get("pack")
        self.MONITOR_W = 1200
        self.MONITOR_H = 780

        if (platform == 'win'):
            print("Desktop platform block.")
            self.MONITOR_W = GetSystemMetrics(0)
            self.MONITOR_H = GetSystemMetrics(1)

        ####################################################
        # Engine config , Colors Theme
        ####################################################
        self.engineConfig = EngineConfig()
        self.engineConfig.getVersion()

        Window.size = (sp(self.MONITOR_W - 10), sp(self.MONITOR_H - 70))
        Window.top = 30
        Window.left = 5
        #Window.fullscreen = True
        Window.clearcolor = self.engineConfig.getThemeBackgroundColor()

        """  # Get path to SD card Android
        try:
            Environment = autoclass('android.os.Environment')
            sdpath = Environment.getExternalStorageDirectory()
            print("Android sdpath is ", sdpath)

        # Not on Android
        except:
            sdpath = App.get_running_app().user_data_dir
            print("Not android sdpath is ", sdpath) """

        # predefined var for Details
        self.editorElementDetails = None
        self.loadProjectFiles()

    def __setLayoutType(self, instance):
        print(".....select layout type.....", instance.text)
        self.selectBtn.text = instance.text
        self.layoutTypeList.select(instance.text)

    def __deleteElementar(self, currElements, elementID):

        print("delete element in root first  ", currElements)
        isPassed = False

        for index, item in enumerate(currElements):
            print("index", index)

            if item['id'] == elementID:
                print('I FOUND REFS IN ROOT DELETE - UPDATE STORE ', item['name'])
                currElements.pop(index)
                isPassed = True
                return currElements
                break

            print("isPassed ", isPassed)
            if isPassed == False:
                for index, item in enumerate(currElements):
                    print("search subs in ", currElements)

                    if item['type'] == "LAYOUT" and len(item['elements']) > 0:
                        print('I FOUND [DELETE]  layout with elements - DEEP SEARCH ', item['name'])
                        for indexSub, itemSub in enumerate(item['elements']):
                            if itemSub['id'] == elementID:
                                currElements[index]['elements'].pop(indexSub)
                                isPassed = True
                                return currElements
                                break
        
        # DELETE DETAILS GUI BOX
        self.editorElementDetails.clear_widgets()

    def delete(self, elementID, elementType,  instance):

        # print("delete element type ", elementType)
        # print("delete element ID ", elementID)
        # print("instance ", instance)

        # updaet always
        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')
        rootElements = self.store.get('renderComponentArray')['elements']

        modifitedData = self.__deleteElementar(rootElements, elementID)
        # print(modifitedData)
        self.closeWithNoSaveDetails(None)
        self.store.put('renderComponentArray', elements=modifitedData)
        self.updateScene()
        self.sceneGUIContainer.selfUpdate()

    def _readElementar(self, currentCointainer, loadElements):

        print("read elementar current container  loadElements : ", loadElements)
        if loadElements == [None]  or loadElements == None:
            return False

        for item in loadElements:
            if item != None and item['type'] == 'BUTTON':
                local_size_hintX = None
                local_size_hintY= None

                constructedApplicationButton = None

                ##"pos_x": "0",
                #"pos_y": "0",
                #"pos_hint_x": "0",
                #"pos_hint_y": "0"

                if item['dimensionRole'] == "pixel":
                    local_size_hintX = None
                    local_size_hintY= None
                    testLocalPosHint = (float(item['pos_hint_x']), float(item['pos_hint_y']))
                    print(testLocalPosHint)
                    constructedApplicationButton = Button(
                        pos=(float(item['pos_x']), float(item['pos_y'])),
                        # pos_hint=testLocalPosHint, # maybe disable
                        pos_hint={ 'x': float(item['pos_hint_x']), 'y': float(item['pos_hint_y'])}, # maybe disable
                        text=item['text'],
                        color=item['color'],
                        background_normal= '',
                        background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY,
                        height=item['height'],
                        width=item['width'],
                        on_press=partial(self.engineLayout.attachEvent, item['attacher'] ) ) 

                elif item['dimensionRole'] == "hint":

                    if item['size_hint_x'] == "None":
                        local_size_hintX = None
                    else:
                        local_size_hintX = item['size_hint_x']

                    if item['size_hint_y'] == "None":
                        local_size_hintY = None
                    else:
                        local_size_hintY = item['size_hint_y']

                    constructedApplicationButton = Button(
                        pos=(float(item['pos_x']), float(item['pos_y'])),
                        #pos_hint=(float(item['pos_hint_x']), float(item['pos_hint_y'])), # maybe disable
                        text=item['text'],
                        color=item['color'],
                        background_normal= '',
                        background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY,
                        on_press=partial(self.engineLayout.attachEvent, item['attacher'])
                    ) 

                elif item['dimensionRole'] == "combine":
                    if item['size_hint_x'] == "None":
                        local_size_hintX = None
                    else:
                        local_size_hintX = item['size_hint_x']

                    if item['size_hint_y'] == "None":
                        local_size_hintY = None
                    else:
                        local_size_hintY = item['size_hint_y']

                    constructedApplicationButton = Button(
                        pos=(float(item['pos_x']), float(item['pos_y'])),
                        pos_hint_x=float(item['pos_hint_x']),
                        pos_hint_y=float(item['pos_hint_y']),
                        text=item['text'],
                        color=item['color'],
                        background_normal= '',
                        background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY,
                        height=item['height'],
                        width=item['width'],
                        on_press=partial(self.engineLayout.attachEvent, item['attacher'])
                    )

                currentCointainer.add_widget(constructedApplicationButton)

            if item != None and item['type'] == 'LABEL':

                local_size_hintX = None
                local_size_hintY= None

                if item['dimensionRole'] == "pixel":

                    local_size_hintX = None
                    local_size_hintY= None
                    test = Label(
                        text=item['text'],
                        color=item['color'],
                        font_size=item['fontSize'], # add
                        bold=item['bold'],    # add
                        padding_x= 0, # test
                        padding_y= 0, # test
                        center=(1,1), # test
                        font_blended= True, # test
                        pos=(float(item['pos_x']), float(item['pos_y'])),
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY,
                        height=item['height'],
                        width=item['width'])
                    with test.canvas.before:
                        Color(item['bgColor'][0],item['bgColor'][1],item['bgColor'][2],item['bgColor'][3])
                        test.rect = Rectangle(size=test.size,
                        pos=test.pos)
                    def update_rect(instance, value):
                        instance.rect.pos = instance.pos
                        instance.rect.size = instance.size
                    currentCointainer.add_widget(test)
                    test.bind(pos=update_rect, size=update_rect)

                elif item['dimensionRole'] == "hint":

                    if item['size_hint_x'] == "None":
                        local_size_hintX = None
                    else:
                        local_size_hintX = item['size_hint_x']

                    if item['size_hint_y'] == "None":
                        local_size_hintY = None
                    else:
                        local_size_hintY = item['size_hint_y']

                    test = Label(
                        text=item['text'],
                        color=item['color'],
                        font_size=item['fontSize'], # add
                        bold=item['bold'],    # add
                        padding_x= 0, # test
                        padding_y= 0, # test
                        center=(1,1), # test
                        pos=(float(item['pos_x']), float(item['pos_y'])),
                        #pos_hint=(float(item['pos_hint_x']), float(item['pos_hint_y'])), # maybe disable
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY)
                    with test.canvas.before:
                        Color(item['bgColor'][0],item['bgColor'][1],item['bgColor'][2],item['bgColor'][3])
                        test.rect = Rectangle(size=test.size,
                        pos=test.pos)
                    def update_rect(instance, value):
                        instance.rect.pos = instance.pos
                        instance.rect.size = instance.size

                    currentCointainer.add_widget(test)
                    test.bind(pos=update_rect, size=update_rect)

                elif item['dimensionRole'] == "combine":

                    if item['size_hint_x'] == "None":
                        local_size_hintX = None
                    else:
                        local_size_hintX = item['size_hint_x']

                    if item['size_hint_y'] == "None":
                        local_size_hintY = None
                    else:
                        local_size_hintY = item['size_hint_y']

                    test =  Label(
                        text=item['text'],
                        color=item['color'],
                        font_size=item['fontSize'], # add
                        bold=item['bold'],    # add
                        padding_x= 0, # test
                        padding_y= 0, # test
                        center=(1,1), # test
                        pos=(float(item['pos_x']), float(item['pos_y'])),
                        #pos_hint=(float(item['pos_hint_x']), float(item['pos_hint_y'])), # maybe disable
                        #foreground_color=item['color'],
                        #background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY,
                        height=item['height'],
                        width=item['width'])
                    with test.canvas.before:
                        Color(item['bgColor'][0],item['bgColor'][1],item['bgColor'][2],item['bgColor'][3])
                        test.rect = Rectangle(size=test.size,
                        pos=test.pos)
                    def update_rect(instance, value):
                        instance.rect.pos = instance.pos
                        instance.rect.size = instance.size

                    currentCointainer.add_widget(test)
                    test.bind(pos=update_rect, size=update_rect)

            if item != None and item['type'] == 'LAYOUT':

                local_size_hintX = None
                local_size_hintY= None

                if item['dimensionRole'] == "pixel":
                    local_size_hintX = None
                    local_size_hintY= None
                elif item['dimensionRole'] == "hint" or item['dimensionRole'] == "combine":

                    if item['size_hint_x'] == "None":
                        local_size_hintX = None
                    else:
                        local_size_hintX = item['size_hint_x']

                    if item['size_hint_y'] == "None":
                        local_size_hintY = None
                    else:
                        local_size_hintY = item['size_hint_y']

                # determinate type
                if item['layoutType'] == "Box":
                    Attacher = BoxLayout
                    print("BOX LOAD>>>>>>>>>>>>>>")
                    myAttacher = Attacher(
                        #text=item['text'],
                        orientation=item['orientation'],
                        spacing=float(item['spacing']),
                        padding=float(item['padding']),
                        #color=item['color'],
                        #background_normal= '',
                        #background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY)
                    with myAttacher.canvas.before:
                        Color(item['bgColor'][0],item['bgColor'][1],item['bgColor'][2],item['bgColor'][3])
                        myAttacher.rect = Rectangle(size=myAttacher.size,
                        pos=myAttacher.pos)
                    def update_rect(instance, value):
                        instance.rect.pos = instance.pos
                        instance.rect.size = instance.size

                    # listen to size and position changes
                    currentCointainer.add_widget(myAttacher)
                    myAttacher.bind(pos=update_rect, size=update_rect)

                    print(">>>>", item['elements'])
                    self._readElementar(myAttacher, item['elements'])

                elif item['layoutType'] == "Anchor":
                    Attacher = AnchorLayout
                    print("Anchorlayout BOX LOAD>>>>>>>>>>>>>>")
                    myAttacher = Attacher(
                        anchor_x=item['anchor_x'],
                        anchor_y=item['anchor_y'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY
                        )
                    with myAttacher.canvas.before:
                        Color(item['bgColor'][0],item['bgColor'][1],item['bgColor'][2],item['bgColor'][3])
                        myAttacher.rect = Rectangle(size=myAttacher.size,
                        pos=myAttacher.pos)
                    def update_rect(instance, value):
                        instance.rect.pos = instance.pos
                        instance.rect.size = instance.size

                    # listen to size and position changes
                    currentCointainer.add_widget(myAttacher)
                    myAttacher.bind(pos=update_rect, size=update_rect)

                    print(">>>>", item['elements'])
                    self._readElementar(myAttacher, item['elements'])

                elif item['layoutType'] == "Float":
                    Attacher = FloatLayout

                    print("BOX FloatLayout LOAD>>>>>>>>>>>>>>")
                    myAttacher = Attacher(
                        #text=item['text'],
                        size=(300, 300),
                        #orientation=item['orientation'],
                        #spacing=float(item['spacing']),
                        #padding=float(item['padding']),
                        #color=item['color'],
                        #background_normal= '',
                        #background_color= item['bgColor'],
                        #size_hint_x=local_size_hintX,
                        #size_hint_y=local_size_hintY
                        )
                    with myAttacher.canvas.before:
                        Color(item['bgColor'][0],item['bgColor'][1],item['bgColor'][2],item['bgColor'][3])
                        myAttacher.rect = Rectangle(size=myAttacher.size,
                        pos=myAttacher.pos)
                    def update_rect(instance, value):
                        instance.rect.pos = instance.pos
                        instance.rect.size = instance.size

                    # listen to size and position changes
                    currentCointainer.add_widget(myAttacher)
                    myAttacher.bind(pos=update_rect, size=update_rect)

                    print(">>>>", item['elements'])
                    self._readElementar(myAttacher, item['elements'])

                elif item['layoutType']  == "Grid":
                    Attacher = GridLayout
                    myAttacher = Attacher(
                        #text=item['text'],
                        # size=(300, 300),
                        #orientation=item['orientation'],
                        cols=2,
                        spacing=float(item['spacing']),
                        padding=float(item['padding']),
                        color=item['color'],
                        background_normal= '',
                        background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY
                        )
                    with myAttacher.canvas.before:
                        Color(item['bgColor'][0],item['bgColor'][1],item['bgColor'][2],item['bgColor'][3])
                        myAttacher.rect = Rectangle(size=myAttacher.size,
                        pos=myAttacher.pos)
                    def update_rect(instance, value):
                        instance.rect.pos = instance.pos
                        instance.rect.size = instance.size

                    # listen to size and position changes
                    currentCointainer.add_widget(myAttacher)
                    myAttacher.bind(pos=update_rect, size=update_rect)

                elif item['layoutType'] == "Page":
                    Attacher = PageLayout
                elif item['layoutType'] == "Relative":
                    Attacher = Relative
                elif item['layoutType'] == "Scatter":
                    Attacher = Scatter
                elif item['layoutType'] == "Stack":
                    Attacher = Stack

                # print('its lauout ,read sub items ->>>')
                print('its lauout ,read sub items ->>>', item["layoutType"])

    def updateScene(self):

        # self.closeWithNoSaveDetails()

        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.pack + '.json')
        loadElements = self.store.get('renderComponentArray')['elements']

        print('----------------------------------')
        print('CLEAR, UPDATE SCENE [engineLayout]')
        print('----------------------------------')
        self.engineLayout.clear_widgets()

        self._readElementar(self.engineLayout ,loadElements)

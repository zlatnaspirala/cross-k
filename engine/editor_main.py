
#########################################################
# CrossK Editor                                         #
# Version: 0.2.0 Beta/WIP                               #
# Under GPL V3  - Nikola Lukic @zlatnaspirala           #
#########################################################

#########################################################
# Python core                                           #
#########################################################
from builtins import chr
import os
import threading
import uuid

#########################################################
# Kivy dependency                                       #
#########################################################
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
from kivy.uix.pagelayout import PageLayout
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

#########################################################
# CrossK Editor dependency                              #
#########################################################
from engine.editor.layout import EngineLayout
from engine.editor.sceneGUIContainer import SceneGUIContainer
from engine.editor.resourcesGUIContainer import ResourcesGUIContainer
from engine.editor.scripter import EventsEngineLayout
from engine.common.assetsEditorOperation import AssetsEditorPopupAdd
from engine.common.assetsEditor import AssetsEditorPopup
from engine.config import EngineConfig
from engine.common.modifycation import AlignedTextInput
from engine.common.commons import getAboutGUI, getMessageBoxYesNo
from engine.common.operationsButton import EditorOperationButton
from engine.common.operationsLabel import EditorOperationLabel
from engine.common.operationsBox import EditorOperationBox
from engine.common.operationsPicture import EditorOperationPicture
from engine.common.enginePackage import PackagePopup
from kivy.utils import platform
#########################################################
# CrossK App level dependency                           #
#########################################################
from engine.common.crossk.imageClickable import PictureClickable

print("Current platform :", platform)
print("Editor Engine Running rigth now.")

if (platform == 'win'):
    from win32api import GetSystemMetrics

# Storage/Files operations
# from jnius import autoclass  # SDcard Android


# Editor main is only editor not inpact projects files.
class EditorMain(BoxLayout):

    def CreateLoadInstanceGUIBox(self, instance):

        if self.programStatus != 'FREE':
            return None

        print("CreateLoadInstanceGUIBox ..." )
        #self.rows = 2  row_force_default=True, row_default_height=10

        self.createLoadProjectLayoutEditor = GridLayout(spacing = 1,
                                                        rows=8,
                                                        row_force_default=True,
                                                        row_default_height=50)
        self.add_widget(self.createLoadProjectLayoutEditor)

        self.createLoadProjectLayoutEditor.add_widget(
                         Label(
                           text='', markup=True, font_size="30sp",
                           size=(1,50), size_hint=(1,None)
                        ))

        self.createLoadProjectLayoutEditor.add_widget(Label(text='CROSS[b]K[/b]', markup=True, font_size="30sp" ))

        self.createLoadProjectLayoutEditor.add_widget(Label(text='[b]Multiplatform App-Game Engine Tool[/b]', markup=True, bold=True, font_size="20sp" ))
        self.createLoadProjectLayoutEditor.add_widget(Label(text='[b]Based on powerful kivy 2.0 [opengles2]. Running with Python3.[/b] ', markup=True, bold=True, font_size="10sp" ))

        self.newProjectBtn = Button(
            markup=True,
            text='[b]Load project[/b]',
            size_hint=(1, .2),
            color=self.engineConfig.getThemeTextColor(),
            background_normal= '',
            background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
            on_press=self.loadProjectFiles)

        self.newProjectTitle = Label(text='Project name:')
        self.createLoadProjectLayoutEditor.add_widget(self.newProjectTitle)
        self.projectName = TextInput(text='Project1', halign='center', font_size=22)

        self.createLoadProjectLayoutEditor.add_widget(self.projectName)
        self.createLoadProjectLayoutEditor.add_widget(self.newProjectBtn)

        self.createLoadProjectLayoutEditor.add_widget(
            Button(
                markup=True,
                text='[b]Cancel[/b]',
                size_hint=(1, 0.2),
                color=self.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                on_press=self.loadNewProjectGUICancel))

    def loadProjectFiles(self, instance):

        CURRENT_PATH = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../projects/' + self.projectName.text + "/")
        )
        if not os.path.exists(CURRENT_PATH):
            getMessageBoxYesNo(
                "Not exist project with name `" + self.projectName.text + "`. Please look at /projects/ root folder. Subfolder name is project name.",
                "OK",
                "null"
            )
            return 0

        CURRENT_ASSET_PATH = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../projects/' + self.projectName.text + "/data/")
        )
        if not os.path.exists(CURRENT_ASSET_PATH):
            getMessageBoxYesNo(
                "Not exist project with name `" + self.projectName.text + "`. Please look at /projects/ root folder. Subfolder name is project name.",
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
        self.engineConfig.currentProjectName = self.projectName.text
        self.engineConfig.currentProjectPath = CURRENT_PATH
        self.engineConfig.currentProjectAssetPath = CURRENT_ASSET_PATH
        self.engineLayout.currentProjectPath=self.engineConfig.currentProjectPath
        self.engineLayout.currentProjectName=self.engineConfig.currentProjectName

        # help
        self.fullProjectStorePath = self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json'
        print("Project name:", self.engineConfig.currentProjectName )
        print("Project root:", self.engineConfig.currentProjectPath )

        ###############################################################
        # Project files loading definition
        ###############################################################
        # copyfile("./engine/editor/layout.py", "./projects/test1.py")
        # Clear and remove engine editor widget
        # self.createNewProjectLayoutEditor.clear_widgets()

        self.remove_widget(self.createLoadProjectLayoutEditor)
        self.add_widget(self.engineLayout)

        # Loading
        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')
        loadElements = self.store.get('renderComponentArray')['elements']

        self.updateScene()

        # Sync call SceneGUIContainer constructor
        # pass store path like arg to get clear updated data intro sceneGUIContainer...
        self.sceneGUIContainer = SceneGUIContainer(
            storePath=self.fullProjectStorePath,
            orientation='vertical',
            engineRoot=self,
            size_hint=(1, 1),
        )
        # orientation="vertical"
        self.editorMenuLayout.add_widget(self.sceneGUIContainer)

        # Sync call GUIContainer constructor
        # pass store path like arg to get clear updated data intro ResourcesGUIContainer...
        self.resourceGUIContainer = ResourcesGUIContainer(
            assetsPath=self.engineConfig.currentProjectAssetPath,
            orientation='vertical',
            engineRoot=self,
            size_hint=(1, 1),
        )
        # orientation="vertical"
        self.editorMenuLayout.add_widget(self.resourceGUIContainer)

        # print(" >>self.engineLayout.currentProjectName>> ", self.engineLayout.currentProjectPath)
        # error
        # put some values , date=datetime.now()
        # get a value using a index key and key
        # print('tito is', store.get('tito')['age'])
        # or guess the key/entry for a part of the key
        #for item in store.find(name='Gabriel'):
        #    print('tshirtmans index key is', item[0])
        #    print('his key value pairs are', str(item[1]))
        print("CrossK project with name -> ", self.projectName.text, " -> loaded.")
        self.programStatus = 'IN_USE'

    def createProjectFiles(self, instance):

        if self.programStatus != 'FREE':
            return None

        CURRENT_PATH = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../projects/' + self.projectName.text + "/")
        )
        if not os.path.exists(CURRENT_PATH):
            os.mkdir(CURRENT_PATH)
        else:
            getMessageBoxYesNo(
                "Already exist project with name `" + self.projectName.text + "`. Please change project name.",
                "OK",
                "null"
            )
            return 0

        CURRENT_ASSET_PATH = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../projects/' + self.projectName.text + "/data")
        )
        if not os.path.exists(CURRENT_ASSET_PATH):
            print('Asset data folder created.')
            os.mkdir(CURRENT_ASSET_PATH)


        ###############################################################
        # App root layout instance
        ###############################################################
        self.engineLayout = EngineLayout()

        # Step : runtime setup project global data.
        # ProjectName and ProjectPath root , also setup config.
        self.engineConfig.currentProjectName = self.projectName.text
        self.engineConfig.currentProjectPath = CURRENT_PATH
        self.engineConfig.currentProjectAssetPath = CURRENT_ASSET_PATH
        self.engineLayout.currentProjectPath=self.engineConfig.currentProjectPath
        self.engineLayout.currentProjectName=self.engineConfig.currentProjectName

        # help
        self.fullProjectStorePath = self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json'

        print("Project name:", self.engineConfig.currentProjectName )
        print("Project root:", self.engineConfig.currentProjectPath )

        ###############################################################
        # Project files definition
        ###############################################################

        # copyfile("./engine/editor/layout.py", "./projects/test1.py")

        # Clear and remove engine widget
        self.createNewProjectLayoutEditor.clear_widgets()
        self.remove_widget(self.createNewProjectLayoutEditor)
        self.add_widget(self.engineLayout)

        # Creating
        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')

        self.assetsStore = JsonStore(self.engineLayout.currentProjectPath + '/data/assets.json')

        print(" >>self.engineLayout.currentProjectName>> ", self.engineLayout.currentProjectPath)
        # error
        # put some values , date=datetime.now()

        self.store.put('projectInfo', name=self.projectName.text, version='beta')
        self.store.put('defaultLayout', layoutType='boxLayout', orientation='horizontal')
        self.store.put('renderComponentArray', elements=[])
        self.assetsStore.put('assetsComponentArray', elements=[])

        # Sync call SceneGUIContainer constructor
        # pass store path like arg to get clear updated data intro sceneGUIContainer...
        self.sceneGUIContainer = SceneGUIContainer(
            storePath=self.fullProjectStorePath,
            orientation='vertical',
            engineRoot=self,
            size_hint=(1, 1),
        )
        # orientation="vertical"
        self.editorMenuLayout.add_widget(self.sceneGUIContainer)

        # Sync call GUIContainer constructor
        # pass store path like arg to get clear updated data intro sceneGUIContainer...
        self.resourceGUIContainer = ResourcesGUIContainer(
            assetsPath=self.engineConfig.currentProjectAssetPath,
            orientation='vertical',
            engineRoot=self,
            size_hint=(1, 1),
        )
        # orientation="vertical"
        self.editorMenuLayout.add_widget(self.resourceGUIContainer)

        # or guess the key/entry for a part of the key
        #for item in store.find(name='Gabriel'):
        #    print('tshirtmans index key is', item[0])
        #    print('his key value pairs are', str(item[1]))
        self.programStatus = 'IN_USE'
        print("CrossK project with name -> ", self.projectName.text, " -> created.")

    def CreateNewInstanceGUIBox(self, instance):

        if self.programStatus != 'FREE':
            return None
            
        print("CreateNewInstanceGUIBox ..." )
        self.createNewProjectLayoutEditor = GridLayout(padding= 0,
                                                       spacing=1,
                                                       rows=8,
                                                       row_force_default=True,
                                                       row_default_height=50)
        self.add_widget(self.createNewProjectLayoutEditor)

        self.createNewProjectLayoutEditor.add_widget(
                         Label(
                           text='', markup=True, font_size="30sp",
                           size=(1,50), size_hint=(1,None)
                        ))

        self.createNewProjectLayoutEditor.add_widget(
                         Label(
                           text='CROSS[b]K[/b]', markup=True, font_size="30sp",
                           size=(1,50), size_hint=(1,None)
                        ))

        self.createNewProjectLayoutEditor.add_widget(Label(text='[b]Multiplatform App-Game Engine Tool[/b]', markup=True, bold=True, font_size="20sp",
                                   size=(1,10), size_hint=(1,None) ))
        self.createNewProjectLayoutEditor.add_widget(Label(
            text='[b]Based on powerful kivy 2.0 [opengles2]. Running with Python3.[/b]',
            markup=True, bold=True, font_size="10sp",
            size_hint=(1, None),
            size=(1, 30) ))

        self.newProjectBtn = Button(markup=True,
                                    text='[b]Create new[/b]',
                                    size_hint=(1, None),
                                    size=(1, 50),
                                    color=self.engineConfig.getThemeTextColor(),
                                    background_normal= '',
                                    background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                                    on_press=self.createProjectFiles)

        self.newProjectTitle = Label(markup=True, text='[b]Project name:[/b]')
        self.createNewProjectLayoutEditor.add_widget(self.newProjectTitle)
        self.projectName =  TextInput(text='Project1',
                                      font_size=22,
                                      halign='center',
                                      #valign='middle',
                                      size_hint=(1, None),
                                      height=50)

        self.createNewProjectLayoutEditor.add_widget(self.projectName)
        self.createNewProjectLayoutEditor.add_widget(self.newProjectBtn)

        self.createNewProjectLayoutEditor.add_widget(
            Button(markup=True,
                   text='[b]Cancel[b]',
                   size=(1,50),
                   size_hint=(1, None),
                   color=self.engineConfig.getThemeTextColor(),
                   background_normal= '',
                   background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                   on_press=self.createNewProjectGUICancel 
                   ))

    def createNewProjectGUICancel(self, instance):
        self.remove_widget(self.createNewProjectLayoutEditor)

    def loadNewProjectGUICancel(self, instance):
        self.remove_widget(self.createLoadProjectLayoutEditor)

    def showAssetsEditorAdd(self, instance):

        if self.programStatus == 'FREE':
            return None

        local = AssetsEditorPopupAdd(
                engineConfig=self.engineConfig,
                engineRoot=self,
                currentAsset=None
            )
        print("Assets Editor for engine started.")

    def showCurrentAssetsEditor(self, asset, instance):

        if self.programStatus == 'FREE':
            return None

        local = AssetsEditorPopup(
                engineConfig=self.engineConfig,
                currentAsset=asset,
                engineRoot=self
            )
        print("Assets Editor for engine started. asset" , asset , ' instance ', instance)

    def packageWinApp(self, instance):

        if self.programStatus == 'FREE':
            return None

        local = PackagePopup(engineConfig=self.engineConfig)
        print("Package application for engine started.")

    def __init__(self, **kwargs):
        super(EditorMain, self).__init__(**kwargs)

        ####################################################
        # Engine config , Colors Theme
        ####################################################
        self.engineConfig = EngineConfig()
        self.engineConfig.getVersion()

        # Prevent action flag
        self.programStatus = 'FREE'

        self.MONITOR_W = self.engineConfig.platformRoles['win']['initialWidth']
        self.MONITOR_H = self.engineConfig.platformRoles['win']['initialHeight']

        if (platform == 'win'):
            print("Current platform: windows")
            self.MONITOR_W = GetSystemMetrics(0)
            self.MONITOR_H = GetSystemMetrics(1)
            Window.size = (sp(self.MONITOR_W - 10), sp(self.MONITOR_H - 70))
            Window.top = 30
            Window.left = 5
            if self.engineConfig.platformRoles['win']['fullscreen'] == True:
                Window.fullscreen = True
            
        # define details scripter property
        self.scripter = None

        # Initial call for aboutGUI
        if self.engineConfig.platformRoles['showAboutBoxOnLoad'] == True:
            getAboutGUI()

        Window.clearcolor = self.engineConfig.getThemeBackgroundColor()
       
        # Run time schortcut vars
        # self.orientation='vertical'
        # self.cols = 1
        """  # Get path to SD card Android
        try:
            Environment = autoclass('android.os.Environment')
            sdpath = Environment.getExternalStorageDirectory()
            print("Android sdpath is ", sdpath)

        # Not on Android
        except:
            sdpath = App.get_running_app().user_data_dir
            print("Not android sdpath is ", sdpath) """

        ################################################################
        # Main Editor Layout (left) menu.
        ################################################################
        self.editorMenuLayout = BoxLayout(orientation='vertical', size_hint=(None, 1), width=300)
        self.add_widget(self.editorMenuLayout)

        # predefined var for Details
        self.editorElementDetails = None

        self.assetsDropdown = DropDown()
        self.assetsDropdown.dismiss()

        self.packageDropdown = DropDown()
        self.packageDropdown.dismiss()

        packWindows = Button(text='Make package for windows',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(1, None),  height=30, width=300,
                      background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                      on_press=self.packageWinApp)
        packLinux = Button(text='Make package for Linux',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(1, None),  height=30, width=300,
                      background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                      on_press=self.packageWinApp)
        self.packageDropdown.add_widget(packWindows)
        self.packageDropdown.add_widget(packLinux)
        self.editorMenuLayout.add_widget(self.packageDropdown)

        # Assets
        assetEditorTool = Button(text='Add Assets',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(1, None),  height=30, width=300,
                      #background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                      on_press=self.showAssetsEditorAdd)
        sep = Button(text='Edit assets',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(1, None),  height=30, width=300,
                      #background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                      on_press=partial(self.showCurrentAssetsEditor, None)
                      )
        self.assetsDropdown.add_widget(assetEditorTool)
        self.assetsDropdown.add_widget(sep)
        self.editorMenuLayout.add_widget(self.assetsDropdown)

        self.currentProjectMenuDropdown = DropDown()
        self.currentProjectMenuDropdown.dismiss()
        
        toolsAddBox = Button(text='Add Box',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(None, None),  height=30, width=300,
                      #background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                      on_press=self.addNewBoxGUI)
        toolsAddBtn = Button(text='Add Button',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(None, None),  height=30, width=300,
                      #background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                      on_press=self.addNewButtonGUI)
        toolsAddText = Button(text='Add Text',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(None, None),  height=30, width=300,
                      #background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                      on_press=self.addNewLabelGUI)
        toolsAddPicture = Button(text='Add Picture',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(None, None),  height=30, width=300,
                      #background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                      on_press=self.addNewPictureGUI)

        self.currentProjectMenuDropdown.add_widget(toolsAddBox)
        self.currentProjectMenuDropdown.add_widget(toolsAddBtn)
        self.currentProjectMenuDropdown.add_widget(toolsAddText)
        self.currentProjectMenuDropdown.add_widget(toolsAddPicture)

        self.editorMenuLayout.add_widget(self.currentProjectMenuDropdown)

        # Application Menu Drop menu
        self.appMenuDropdown = DropDown()
        self.appMenuDropdown.dismiss()

        btn = Button(markup=True, text='Create new project',
                     color=(self.engineConfig.getThemeTextColor()),
                     size_hint=(1, None), height=30, width=300, 
                     # background_normal= '',
                     background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground'))
                    )
        self.appMenuDropdown.add_widget(btn)

        loadBtn = Button(markup=True, text='Load project',
                     color=(self.engineConfig.getThemeTextColor()),
                     size_hint=(1, None), height=30, width=300,
                     # background_normal= '',
                     background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground'))
                     )

        self.appMenuDropdown.add_widget(loadBtn)

        aboutBtn = Button(markup=True,
                     text='About CrossK Engine',
                     color=(self.engineConfig.getThemeTextColor()),
                     size_hint=(1, None), height=30, width=300,
                     # background_normal= '',
                     background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground'))
                     )

        self.appMenuDropdown.add_widget(aboutBtn)

        aboutBtn.bind(on_press=getAboutGUI)
        loadBtn.bind(on_press=self.CreateLoadInstanceGUIBox)

        self.editorMenuLayout.add_widget(self.appMenuDropdown)

        btn.bind(on_press=self.CreateNewInstanceGUIBox)

        MakePackageBtn = Button(markup=True, text='[b]Make package[/b]',
                     color=(self.engineConfig.getThemeTextColor()),
                     size_hint=(None, None), height=30, width=300,
                     background_normal= '',
                     background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground'))
                     )
        MakePackageBtn.bind(on_release=self.packageDropdown.open)
        self.editorMenuLayout.add_widget(MakePackageBtn)

        AssetsBtn = Button(markup=True, text='[b]Project Assets[/b]',
                     color=(self.engineConfig.getThemeTextColor()),
                     size_hint=(None, None), height=30, width=300,
                     background_normal= '',
                     background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground'))
                     )
        AssetsBtn.bind(on_release=self.assetsDropdown.open)
        self.editorMenuLayout.add_widget(AssetsBtn)

        editorTools = Button(
                             markup=True, text='[b]Tools[/b]',
                             color=(self.engineConfig.getThemeTextColor()),
                             size_hint=(None, None), height=30, width=300,
                             background_normal= '',
                             background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground'))
                           )
        editorTools.bind(on_release=self.currentProjectMenuDropdown.open)
        self.editorMenuLayout.add_widget(editorTools)

        mainbutton = Button(markup=True , text='[b]Application[/b]',
                            color=(self.engineConfig.getThemeTextColor()), 
                            size_hint=(None, None), height=30, width=300,
                            background_normal= '',
                            background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')))
        mainbutton.bind(on_release=self.appMenuDropdown.open)
        self.editorMenuLayout.add_widget(mainbutton)

    def get_input(self, v, h):
        return AlignedTextInput(text='Project1', halign=h, valign=v, height=44)

    def addNewButtonGUI(self, instance):
        print('BUTTON.....................................')
        operationAddTest = EditorOperationButton(
            store=self.store,
            currentLayout='SCENE_ROOT',
            engineRoot=self
        )

    def addNewBoxGUI(self, instance):
        print('LAYOUT.....................................')
        operationAddTest = EditorOperationBox(
            store=self.store,
            currentLayout='SCENE_ROOT',
            engineRoot=self
        )

    def addNewLabelGUI(self, instance):
        print('LABEL.....................................')
        operationAddTest = EditorOperationLabel(
            store=self.store,
            currentLayout='SCENE_ROOT',
            engineRoot=self
        )

    def addNewPictureGUI(self, instance):
        print('PICTURE.....................................')
        operationAddTest = EditorOperationPicture(
            store=self.store,
            currentLayout='SCENE_ROOT',
            engineRoot=self
        )

    # Button Label block
    def showCommonDetails(self, detailData, instance):
        print("DETAILS.................................... ", detailData)
        # Clear
        try: self.editorElementDetails
        except NameError: self.editorElementDetails = None

        if self.editorElementDetails is None:
            print(".first time.")
        else:
            self.remove_widget(self.editorElementDetails)
            print(".clear.")
        
        currentType = str(detailData['type']).lower().capitalize()

        # DETAILS BOX BTN 
        self.editorElementDetails = GridLayout( orientation='lr-tb')
        self.editorElementDetails.cols = 2

        # Type
        self.editorElementDetails.add_widget(
            Button(
                text="Type " + str(detailData['type']),
                size_hint=(1,None),
                background_normal= '',
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=30 )
        )
        # ID
        self.editorElementDetails.add_widget(
            Button(
                text=str(detailData['id']),
                size_hint=(1,None),
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=30 )
        )
        # name - tag
        self.editorElementDetails.add_widget(
            Button(
                text="Name(Tag) " + detailData['name'],
                size_hint=(1,None),
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=30 )
            )
        self.commonDetailsNameText = TextInput(
            text=detailData['name'],
            size_hint=(1, None),
            height=30
        )
        self.editorElementDetails.add_widget(self.commonDetailsNameText)
        # text
        self.editorElementDetails.add_widget(
            Button(
                text= "[Over picture] Text",
                size_hint=(1,None),
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=30 )
            )
        # half common btn , label 
        if "text" in detailData:
            print("detailData['text'] sure, it was defined.")
            if (detailData['text'] != None ):
                self.detailsCommonText = TextInput(text=detailData['text'], size_hint=(1, None), height=30)
                self.editorElementDetails.add_widget(self.detailsCommonText)
        else:
            print("detailData['text'] NOT defined.")

        if "pos_x" in detailData:
            print("detailData['pos_x'] sure, it was defined.")
            if (detailData['pos_x'] != None ):
                self.detailsCommonPositionX = TextInput(text=detailData['pos_x'], size_hint=(1, None), height=30)
                self.editorElementDetails.add_widget(Label(text="Position X (pixel):", size_hint=(1, None), height=30))
                self.editorElementDetails.add_widget(self.detailsCommonPositionX)
        else:
            print("detailData['pos'] NOT defined.")

        if "pos_y" in detailData:
            print("detailData['pos_y'] sure, it was defined.")
            if (detailData['pos_y'] != None ):
                self.detailsCommonPositionY = TextInput(text=detailData['pos_y'], size_hint=(1, None), height=30)
                self.editorElementDetails.add_widget(Label(text="Position Y (pixel):", size_hint=(1, None), height=30))
                self.editorElementDetails.add_widget(self.detailsCommonPositionY)
        else:
            print("detailData['pos_y'] NOT defined.")

        # pos Hint
        if "pos_hint_x" in detailData:
            print("detailData['pos_hint_x'] sure, it was defined.")
            if (detailData['pos_hint_x'] != None ):
                self.detailsCommonPositionXHint = TextInput(text=detailData['pos_hint_x'], size_hint=(1, None), height=30)
                self.editorElementDetails.add_widget(Label(text="Position X (hint):", size_hint=(1, None), height=30))
                self.editorElementDetails.add_widget(self.detailsCommonPositionXHint)
        else:
            print("detailData['pos'] NOT defined.")

        if "pos_hint_y" in detailData:
            print("detailData['pos_hint_y'] sure, it was defined.")
            if (detailData['pos_hint_y'] != None ):
                self.detailsCommonPositionYHint = TextInput(text=detailData['pos_hint_y'], size_hint=(1, None), height=30)
                self.editorElementDetails.add_widget(Label(text="Position Y (hint):", size_hint=(1, None), height=30))
                self.editorElementDetails.add_widget(self.detailsCommonPositionYHint)
        else:
            print("detailData['pos_y'] NOT defined.")

        # Checkbox use pixel dimesion system
        self.editorElementDetails.add_widget(Label(
            text='Use Pixel Dimensions', size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'))
            )
       
        if detailData['dimensionRole'] == "pixel":
            _isActiveCheckBoxPix = True
            _isActiveCheckBoxPer = False
            _isActiveCheckBoxCombine = False

        elif detailData['dimensionRole'] == "hint":
            _isActiveCheckBoxPix = False
            _isActiveCheckBoxPer = True
            _isActiveCheckBoxCombine = False

        else:
            _isActiveCheckBoxPix = False
            _isActiveCheckBoxPer = False
            _isActiveCheckBoxCombine = True

        # Checkbox Pixel dimensions
        self.checkboxDim = CheckBox(active=_isActiveCheckBoxPix,size_hint=(1,None),
                height=30 )
        self.editorElementDetails.add_widget(self.checkboxDim)

        self.editorElementDetails.add_widget(
            Button(
                text=currentType + " Width",
                size_hint=(1,None),
                height=30,
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                )
            )
        self.detailsCommonWidth = TextInput(text=str(detailData['width']), size_hint=(1, None), height=30)
        self.editorElementDetails.add_widget(self.detailsCommonWidth)

        self.editorElementDetails.add_widget(
            Button(
                text= currentType + " Height",
                size_hint=(1,None),
                height=30,
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'))
            )
        self.detailsCommonHeight = TextInput(text=detailData['height'], size_hint=(1, None), height=30)
        self.editorElementDetails.add_widget(self.detailsCommonHeight)

        # Percent dimensions
        loc1 = Label(text='Use Percent Dimensions', 
                     color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                     size_hint=(1,None),
                     height=30)
        self.editorElementDetails.add_widget(loc1)
        #loc1.bind(pos=update_rect, size=update_rect)

        self.checkboxPer = CheckBox(active=_isActiveCheckBoxPer, size_hint=(1,None),
                height=30)
        self.editorElementDetails.add_widget(self.checkboxPer)

        # Combine dimensions
        self.editorElementDetails.add_widget(
            Label(text='Use Combine Dimensions (None for disable)', 
                  color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                  size_hint=(1,None),
                  height=30))
        self.checkboxCombine = CheckBox(active=_isActiveCheckBoxCombine, size_hint=(1,None),
                height=30)
        self.editorElementDetails.add_widget(self.checkboxCombine)

        # Bind checkboxs for details box
        self.checkboxPer.bind(active=self.on_checkbox_per_active) # pylint disable=no-member
        self.checkboxDim.bind(active=self.on_checkbox_pixel_active) # pylint disable=no-member
        self.checkboxCombine.bind(active=self.on_checkbox_combine_active) # pylint disable=no-member
 
        self.commonHintXDetail = TextInput(text=str(detailData['size_hint_x']), size_hint=(1,None),
                height=30)
        self.editorElementDetails.add_widget(self.commonHintXDetail)
        self.commonHintYDetail = TextInput(text=str(detailData['size_hint_y']), size_hint=(1,None),
                height=30)
        self.editorElementDetails.add_widget(self.commonHintYDetail)
 
        # Colors elements
        clrPickerTextColor = ColorPicker(color=(detailData['color']))
        clrPickerBackgroundColor = ColorPicker(color=(detailData['bgColor']))

        self.editorElementDetails.add_widget(clrPickerBackgroundColor)
        self.editorElementDetails.add_widget(clrPickerTextColor)

        # Add all
        self.add_widget(self.editorElementDetails)

        # Bind
        clrPickerTextColor.bind(color=self.on_details_color) # pylint: disable=no-member
        clrPickerBackgroundColor.bind(color=self.on_details_bgcolor) # pylint: disable=no-member

        # Specific elemetn props
        if str(detailData['type']) == "BUTTON":
            self.showButtonDetails(detailData)
        elif  str(detailData['type']) == "LABEL":
            self.showLabelDetails(detailData)
        elif  str(detailData['type']) == "PICTURE_CLICKABLE":
            self.showPictureDetails(detailData)

    def showPictureDetails(self, detailData):

        # FontSize
        self.editorElementDetails.add_widget(
            Button(
                text="Image",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                background_normal= '',
                background_color=self.engineConfig.getThemeBackgroundColor()
            ))

        self.detailsPictureImage = TextInput(
            text=detailData['image'],
            size_hint=(1, None),
            height=30
        )
        self.editorElementDetails.add_widget(self.detailsPictureImage)

        
        # FontSize
        self.editorElementDetails.add_widget(
            Button(
                text="Over Text Font size ",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                background_normal= '',
                background_color=self.engineConfig.getThemeBackgroundColor()
            ))

        self.buttonDetailsFontSize = TextInput(
            text=detailData['fontSize'],
            size_hint=(1, None),
            height=30
        )
        self.editorElementDetails.add_widget(self.buttonDetailsFontSize)

        localScripterGUIBox = BoxLayout()
        localScripterGUIBox.add_widget(Button(
                text="Simulate event",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                on_press=partial(self.engineLayout.attachEvent, detailData['attacher'])
            ))

        localScripterGUIBox.add_widget(Button(
                text="Open Scripter Editor",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                on_press=partial(self.showScripter, detailData)
            ))

        self.editorElementDetails.add_widget(localScripterGUIBox)

        self.attachEventCurrentElement = TextInput(
                text=str(detailData['attacher']),
                size_hint=(1,None),
                height=30,
                # color=self.engineConfig.getThemeCustomColor('engineBtnsColor')
                # background_normal= '',
                # background_color=(self.engineConfig.getThemeCustomColor('warn')),
              )
        self.editorElementDetails.add_widget(self.attachEventCurrentElement)

        self.editorElementDetails.add_widget(
            Label(
                text="Delete picture '" + detailData['name'] + "' ",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor')
                # on_press=partial(self.saveDetails, str(detailData['id']), str(detailData['type']) ))
            ))

        self.editorElementDetails.add_widget(
            Button(
                text="Delete picture",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('warn')),
                on_press=partial(self.delete, str(detailData['id']), str(detailData['type']) ))
            )

        self.editorElementDetails.add_widget(
            Button(
                border=(3,3,3,3),
                markup=True,
                text="[b]Save changes[/b]",
                font_size=18,
                size_hint=(1,None),
                height=100,
                color=self.engineConfig.getThemeTextColor(),
                # color=(1,1,1,0.1),
                # background_normal='engine/assets/nidzaBorder002.png',
                # background_down='engine/assets/nidzaBorder001-250x250_yellow_black_Over.png',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                # background_color=(1,1,1,0.8),
                on_release=partial(self.savePictureDetails, str(detailData['id']), str(detailData['type']) ))
            )

        self.editorElementDetails.add_widget(
            Button(
                border=(10,10,10,10),
                markup=True,
                font_size=18,
                text="[b]Cancel[/b]",
                size_hint=(1,None),
                height=100,
                #background_normal='engine/assets/nidzaBorder001-250x250_yellow_black.png',
                #background_down='engine/assets/nidzaBorder001-250x250_yellow_black_Over.png',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                #background_color=(0.1,0.1,0,0.5),
                on_release=self.closeWithNoSaveDetails
            ))


    # def showButtonDetails(self, detailData, instance):
    def showButtonDetails(self, detailData):

        self.editorElementDetails.add_widget(
            Label(
                text="Button background image:",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor')
            ))

        if 'image' in detailData:
            collectImageData = detailData['image']
        else:
            collectImageData = ''

        self.detailsPictureImage = TextInput(
            text=collectImageData,
            size_hint=(1, None),
            height=30
        )
        self.editorElementDetails.add_widget(self.detailsPictureImage)


        # FontSize
        self.editorElementDetails.add_widget(
            Button(
                text="Font size ",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                background_normal= '',
                background_color=self.engineConfig.getThemeBackgroundColor()
            ))

        self.buttonDetailsFontSize = TextInput(
            text=detailData['fontSize'],
            size_hint=(1, None),
            height=30
        )
        self.editorElementDetails.add_widget(self.buttonDetailsFontSize)

        localScripterGUIBox = BoxLayout()
        localScripterGUIBox.add_widget(Button(
                text="Simulate event",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                on_press=partial(self.engineLayout.attachEvent, detailData['attacher'])
            ))

        localScripterGUIBox.add_widget(Button(
                text="Open Scripter Editor",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                on_press=partial(self.showScripter, detailData)
            ))

        self.editorElementDetails.add_widget(localScripterGUIBox)

        self.attachEventCurrentElement = TextInput(
                text=str(detailData['attacher']),
                size_hint=(1,None),
                height=30,
                # color=self.engineConfig.getThemeCustomColor('engineBtnsColor')
                # background_normal= '',
                # background_color=(self.engineConfig.getThemeCustomColor('warn')),
              )
        self.editorElementDetails.add_widget(self.attachEventCurrentElement)

        self.editorElementDetails.add_widget(
            Label(
                text="Delete button '" + detailData['name'] + "' ",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor')
                # on_press=partial(self.saveDetails, str(detailData['id']), str(detailData['type']) ))
            ))

        self.editorElementDetails.add_widget(
            Button(
                text="Delete button",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('warn')),
                on_press=partial(self.delete, str(detailData['id']), str(detailData['type']) ))
            )

        self.editorElementDetails.add_widget(
            Button(
                border=(3,3,3,3),
                markup=True,
                text="[b]Save changes[/b]",
                font_size=18,
                size_hint=(1,None),
                height=100,
                color=self.engineConfig.getThemeTextColor(),
                # color=(1,1,1,0.1),
                # background_normal='engine/assets/nidzaBorder002.png',
                # background_down='engine/assets/nidzaBorder001-250x250_yellow_black_Over.png',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                # background_color=(1,1,1,0.8),
                on_release=partial(self.savePictureDetails, str(detailData['id']), str(detailData['type']) ))
            )

        self.editorElementDetails.add_widget(
            Button(
                border=(10,10,10,10),
                markup=True,
                font_size=18,
                text="[b]Cancel[/b]",
                size_hint=(1,None),
                height=100,
                #background_normal='engine/assets/nidzaBorder001-250x250_yellow_black.png',
                #background_down='engine/assets/nidzaBorder001-250x250_yellow_black_Over.png',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                #background_color=(0.1,0.1,0,0.5),
                on_release=self.closeWithNoSaveDetails
            ))

    def showScripter(self, arg, instance):
        if self.scripter == None:
            self.scripter = EventsEngineLayout(
                engineRoot=self,
                currentScript=self.attachEventCurrentElement.text)
            self.add_widget(self.scripter)

    # LABEL Block
    def showLabelDetails(self, detailData):
 

        print("LABEL detailData-> ", detailData)
        self.editorElementDetails.add_widget(Label(text='Use Bold', 
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                size_hint=(1,None), height=30))

        self.checkboxIsBold = CheckBox(active=False, size_hint=(1,None),
                height=30)
        self.editorElementDetails.add_widget(self.checkboxIsBold)

        # FontSize
        self.editorElementDetails.add_widget(
            Button(
                text="Font size ",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                background_normal= '',
                background_color=self.engineConfig.getThemeBackgroundColor()
            ))

        self.labelDetailsFontSize = TextInput(
            text=detailData['fontSize'],
            size_hint=(1, None),
            height=30
        )
        self.editorElementDetails.add_widget(self.labelDetailsFontSize)


        self.editorElementDetails.add_widget(
            Label(
                text="Delete Label '" + detailData['name'] + "' ",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor')
                # on_press=partial(self.saveDetails, str(detailData['id']), str(detailData['type']) ))
            ))

        self.editorElementDetails.add_widget(
            Button(
                text="Delete Label",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeCustomColor('engineBtnsColor'),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('warn')),
                on_press=partial(self.delete, str(detailData['id']), str(detailData['type']) ))
            )

        self.editorElementDetails.add_widget(
            Button(
                markup=True,
                text="[b]Save changes[/b]",
                size_hint=(1,None),
                height=120,
                on_press=partial(self.saveLabelDetails, str(detailData['id']), str(detailData['type']) ),
                color=self.engineConfig.getThemeTextColor(),
                #background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
            ))

        self.editorElementDetails.add_widget(
            Button(
                markup=True,
                text="[b]Cancel[/b]",
                size_hint=(1,None),
                height=120,
                color=self.engineConfig.getThemeTextColor(),
                #background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                on_press=self.closeWithNoSaveDetails
            ))

    # End of Label block

    def showBoxLayoutDetails(self, detailData):

        #selectAnchor
        #if detailData['layoutType'] == 'Anchor' or detailData['layoutType'] == 'Float':
        if "pos_x" in detailData:
            print("detailData['pos_x'] sure, it was defined.")
            if (detailData['pos_x'] != None ):
                self.detailsCommonPositionX = TextInput(text=detailData['pos_x'], size_hint=(1, None), height=30)
                self.editorElementDetails.add_widget(Label(text="Position X (pixel):",size_hint=(1, None), height=30))
                self.editorElementDetails.add_widget(self.detailsCommonPositionX)
        else:
            print("detailData['pos'] NOT defined.")

        if "pos_y" in detailData:
            print("detailData['pos_y'] sure, it was defined.")
            if (detailData['pos_y'] != None ):
                self.detailsCommonPositionY = TextInput(text=detailData['pos_y'], size_hint=(1, None), height=30)
                self.editorElementDetails.add_widget(Label(text="Position Y (pixel):", size_hint=(1, None), height=30))
                self.editorElementDetails.add_widget(self.detailsCommonPositionY)
        else:
            print("detailData['pos_y'] NOT defined.")

        # pos Hint
        if "pos_hint_x" in detailData:
            print("detailData['pos_hint_x'] sure, it was defined.")
            if (detailData['pos_hint_x'] != None ):
                self.detailsCommonPositionXHint = TextInput(text=detailData['pos_x'], size_hint=(1, None), height=30)
                self.editorElementDetails.add_widget(Label(text="Position X (hint):", size_hint=(1, None), height=30))
                self.editorElementDetails.add_widget(self.detailsCommonPositionXHint)
        else:
            print("detailData['pos'] NOT defined.")

        if "pos_hint_y" in detailData:
            print("detailData['pos_hint_y'] sure, it was defined.")
            if (detailData['pos_hint_y'] != None ):
                self.detailsCommonPositionYHint = TextInput(text=detailData['pos_hint_y'], size_hint=(1, None), height=30)
                self.editorElementDetails.add_widget(Label(text="Position Y (hint):", size_hint=(1, None), height=30))
                self.editorElementDetails.add_widget(self.detailsCommonPositionYHint)
        else:
            print("detailData['pos_y'] NOT defined.")

        localBox = BoxLayout()
        self.editorElementDetails.add_widget(localBox)
        localBox.add_widget(Button(
                markup=True,
                text="[b]Add Btn[/b]",
                size_hint=(0.2,None),
                height=30,
                color=self.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('warn')),
                on_press=partial(self.callAddNewElementGUIBox, detailData))
            )
        
        localBox.add_widget(
            Button(
                markup=True,
                text="[b]Add Label[/b]",
                size_hint=(0.2,None),
                height=30,
                color=self.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('warn')),
                on_press=partial(self.callAddNewLabelGUIBox, detailData))
            )

        localBox.add_widget(
            Button(
                markup=True,
                text="[b]Add Layout[/b]",
                size_hint=(0.2,None),
                height=30,
                color=self.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('warn')),
                on_press=partial(self.callAddNewLayoutGUIBox, detailData))
            )

        ## ANCHOR 
        # anchor_x='right', anchor_y='bottom'

        self.editorElementDetails.add_widget(
            Button(
                markup=True,
                text="[b]Delete Layout[/b]",
                size_hint=(1,None),
                height=30,
                color=self.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('warn')),
                on_press=partial(self.delete, str(detailData['id']), str(detailData['type']) ))
            )

        self.colsInput = TextInput(text=detailData['cols'],size_hint=(1, None), height=30 )
        self.rowsInput = TextInput(text=detailData['rows'],size_hint=(1, None), height=30 )

        if str(detailData['layoutType']) == "Grid": # or str(detailData['layoutType']) == "Float":
            self.editorElementDetails.add_widget(
                Label(
                    text="The Grid Layout - num of columns:",
                    size_hint=(1,None),
                    height=30,
                    color=self.engineConfig.getThemeCustomColor('engineBtnsColor')
                ))
            self.editorElementDetails.add_widget(self.colsInput)

            self.editorElementDetails.add_widget(
                Label(
                    text="The Grid Layout - number of rows:",
                    size_hint=(1,None),
                    height=30,
                    color=self.engineConfig.getThemeCustomColor('engineBtnsColor')
                ))
            self.editorElementDetails.add_widget(self.rowsInput)

        self.swipeThresholdPageLayout = None
        if 'swipe_threshold' in detailData:
            self.swipeThresholdPageLayout = TextInput(text=str(detailData['swipe_threshold']), size_hint=(1, None), height=30)
        else:
            self.swipeThresholdPageLayout = TextInput(text='0.4', size_hint=(1, None), height=30)

        if str(detailData['layoutType']) == "Page":
            self.editorElementDetails.add_widget(
                Label(
                    text="The Page Layout swipe Threshold: ",
                    size_hint=(1,None),
                    height=30,
                    color=self.engineConfig.getThemeCustomColor('engineBtnsColor')
                    # on_press=partial(self.saveDetails, str(detailData['id']), str(detailData['type']) ))
                ))
            self.editorElementDetails.add_widget(self.swipeThresholdPageLayout)


        if str(detailData['layoutType']) == "Anchor" or str(detailData['layoutType']) == "Float":
            self.editorElementDetails.add_widget(
                Label(
                    text="The Anchor/Float Layout aligns left, right or center.",
                    size_hint=(1,None),
                    height=30,
                    color=self.engineConfig.getThemeCustomColor('engineBtnsColor')
                    # on_press=partial(self.saveDetails, str(detailData['id']), str(detailData['type']) ))
                ))

            self.layoutAnchorX = DropDown()
            self.selectAnchor = Button(
                text='center',
                size_hint=(1, None),
                height=30,
                on_press=self.layoutAnchorX.open)

            self.btnAnchor_xL = Button(text='left', size_hint_y=None, height=44 )
            self.btnAnchor_xL.bind(on_release=partial(self.__setLayoutAnchorX))
            self.layoutAnchorX.add_widget(self.btnAnchor_xL)

            self.btnAnchor_xC = Button(text='center', size_hint_y=None, height=44) 
            self.btnAnchor_xC.bind(on_release=partial(self.__setLayoutAnchorX))
            self.layoutAnchorX.add_widget(self.btnAnchor_xC)

            self.btnAnchor_xR = Button(text='right', size_hint_y=None, height=44)
            self.btnAnchor_xR.bind(on_release=partial(self.__setLayoutAnchorX))
            self.layoutAnchorX.add_widget(self.btnAnchor_xR)

            self.editorElementDetails.add_widget(self.layoutAnchorX)
            self.layoutAnchorX.dismiss()

            self.editorElementDetails.add_widget(self.selectAnchor)
            

            self.editorElementDetails.add_widget(
                Label(
                    text="The AnchorLayout aligns top, bottom or center",
                    size_hint=(1,None),
                    height=30,
                    color=self.engineConfig.getThemeCustomColor('engineBtnsColor')
                    # on_press=partial(self.saveDetails, str(detailData['id']), str(detailData['type']) ))
                ))

            self.layoutAnchorY = DropDown()
            self.selectAnchorY = Button(
                text='center',
                size_hint=(1, None),
                height=30,
                on_press=self.layoutAnchorY.open)

            self.btnAnchor_yL = Button(text='top', size_hint_y=None, height=44 )
            self.btnAnchor_yL.bind(on_release=partial(self.__setLayoutAnchorY))
            self.layoutAnchorY.add_widget(self.btnAnchor_yL)

            self.btnAnchor_yC = Button(text='center', size_hint_y=None, height=44) 
            self.btnAnchor_yC.bind(on_release=partial(self.__setLayoutAnchorY))
            self.layoutAnchorY.add_widget(self.btnAnchor_yC)

            self.btnAnchor_yR = Button(text='buttom', size_hint_y=None, height=44)
            self.btnAnchor_yR.bind(on_release=partial(self.__setLayoutAnchorY))
            self.layoutAnchorY.add_widget(self.btnAnchor_yR)

            self.editorElementDetails.add_widget(self.layoutAnchorY)
            self.layoutAnchorY.dismiss()

            self.editorElementDetails.add_widget(self.selectAnchorY)

        # SAVE BUTTON
        self.editorElementDetails.add_widget(
            Button(
                markup=True,
                text="[b]Save changes[/b]",
                size_hint=(1,1),
                #height=120,
                color=self.engineConfig.getThemeTextColor(),
                # background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                on_press=partial(self.saveLayoutDetails, detailData)
            ))

        self.editorElementDetails.add_widget(
            Button(
                markup=True,
                text="[b]Cancel[/b]",
                size_hint=(1,1),
                #height=120,
                color=self.engineConfig.getThemeTextColor(),
                # background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                on_press=self.closeWithNoSaveDetails
            ))

    # LAYOUTS BTN FRIST BLOCK
    def callAddNewElementGUIBox(self, currentData, instance):
        operationAddTest = EditorOperationButton(
            store=self.store,
            currentLayout=currentData['id'], # works
            engineRoot=self,
        )

    def callAddNewLabelGUIBox(self, currentData, instance):
        operationAddTest = EditorOperationLabel(
            store=self.store,
            currentLayout=currentData['id'],
            engineRoot=self,
        )

    def callAddNewLayoutGUIBox(self, currentData, instance):
        print('ADD SUB ELEMENT LAYOUT......................[object]...............', currentData['id'])
        print('ADD SUB ELEMENT LAYOUT......................type...............', currentData['type'])
        print('ADD SUB ELEMENT LAYOUT......................elements...............', currentData['elements'])
        # NEED PARENT LAYOUT REAL REFERENCE INSTANCE
        operationAddTest = EditorOperationBox(
            store=self.store,
            currentLayoutId=currentData['id'],
            engineRoot=self,  # currentData['id']
        )

    def __setLayoutType(self, instance):
        print(".....select layout type.....", instance.text)
        self.selectBtn.text = instance.text
        self.layoutTypeList.select(instance.text)

    def __setLayoutAnchorX(self, instance):
        print(".....select layout type.....", instance.text)
        self.selectAnchor.text = instance.text
        self.layoutAnchorX.select(instance.text)

    def __setLayoutAnchorY(self, instance):
        print(".....select layout type.....", instance.text)
        self.selectAnchorY.text = instance.text
        self.layoutAnchorY.select(instance.text)

    def showCommonLayoutDetails(self, detailData, instance):
        # print("COMMON.DETAILS.LAYOUT......... ", detailData)
        # Clear
        try: self.editorElementDetails
        except NameError: self.editorElementDetails = None

        if self.editorElementDetails is None:
            print(".")
        else:
            self.remove_widget(self.editorElementDetails)
            print(".")

        currentType = str(detailData['type']).lower().capitalize()

        # DETAILS BOX BTN
        self.editorElementDetails = GridLayout( orientation='lr-tb', spacing=1, padding=1)
        self.editorElementDetails.cols = 2

        # Type
        self.editorElementDetails.add_widget(
            Button(
                text="Type " + str(detailData['type']),
                size_hint=(1,None),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=30 )
        )
        # ID
        self.editorElementDetails.add_widget(
            Button(
                text=str(detailData['id']),
                size_hint=(1,None),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=30 )
        )
        # name - tag
        self.editorElementDetails.add_widget(
            Button(
                text="Name(Tag) " + detailData['name'],
                size_hint=(1,None),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=30 )
            )
        self.commonDetailsNameText = TextInput(
            text=detailData['name'],
            size_hint=(1, None),
            height=30
        )
        self.editorElementDetails.add_widget(self.commonDetailsNameText)

        
        self.editorElementDetails.add_widget(Label(text='Layout type',size_hint=(1, None),
            height=30))

        self.layoutTypeList = DropDown()
        self.selectBtn = Button(
            text=detailData['layoutType'],
            size_hint=(1, None),
            height=30,
            on_press=self.layoutTypeList.open)

        self.editorElementDetails.add_widget(self.selectBtn)
        
        #Anchor layout:
        #Box layout: 
        #Float layout:
        #Grid layout:
        #Page Layout:
        #Relative layout:
        #Scatter layout:
        # Stack layout: 

        self.btnBox = Button(text='Box', size_hint_y=None, height=30)
        self.btnBox.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnBox)

        self.btnAnchor = Button(text='Anchor', size_hint_y=None, height=30) 
        self.btnAnchor.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnAnchor)

        self.btnFloat = Button(text='Float', size_hint_y=None, height=30)
        self.btnFloat.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnFloat)

        self.btnGrid = Button(text='Grid', size_hint_y=None, height=30)
        self.btnGrid.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnGrid)

        self.btnPage = Button(text='Page', size_hint_y=None, height=30)
        self.btnPage.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnPage)

        self.btnRelative = Button(text='Relative', size_hint_y=None, height=30)
        self.btnRelative.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnRelative)

        self.btnScatter = Button(text='Scatter', size_hint_y=None, height=30)
        self.btnScatter.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnScatter)

        self.btnStack = Button(text='Stack', size_hint_y=None, height=30)
        self.btnStack.bind(on_release=partial(self.__setLayoutType))
        self.layoutTypeList.add_widget(self.btnStack)

        self.editorElementDetails.add_widget(self.layoutTypeList)
        self.layoutTypeList.dismiss()

        # text
        self.editorElementDetails.add_widget(
            Button(
                text= currentType + " Orientation",
                size_hint=(1,None),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=30)
            )

        # half common btn , label 
        self.detailsCommonLayoutOrientation = TextInput(text=detailData['orientation'], size_hint=(1, None), height=30)
        self.editorElementDetails.add_widget(self.detailsCommonLayoutOrientation)

        self.editorElementDetails.add_widget(Label(text='Padding',size_hint=(1, None), height=30))
        self.layoutPadding = TextInput(text=detailData['padding'],size_hint=(1, None), height=30 )
        self.editorElementDetails.add_widget(self.layoutPadding)

        self.editorElementDetails.add_widget(Label(text='Spacing',size_hint=(1, None), height=30))
        self.layoutSpacing = TextInput(text=detailData['spacing'], size_hint=(1, None), height=30)
        self.editorElementDetails.add_widget(self.layoutSpacing)

        # Checkbox use pixel dimesion system
        self.editorElementDetails.add_widget(Label(
            text='Use Pixel Dimensions', size_hint=(1,None),
                height=30, color=self.engineConfig.getThemeTextColor()))
       
        if detailData['dimensionRole'] == "pixel":
            _isActiveCheckBoxPix = True
            _isActiveCheckBoxPer = False
            _isActiveCheckBoxCombine = False

        elif detailData['dimensionRole'] == "hint":
            _isActiveCheckBoxPix = False
            _isActiveCheckBoxPer = True
            _isActiveCheckBoxCombine = False

        else:
            _isActiveCheckBoxPix = False
            _isActiveCheckBoxPer = False
            _isActiveCheckBoxCombine = True

        # Checkbox Pixel dimensions
        self.checkboxDim = CheckBox(active=_isActiveCheckBoxPix,size_hint=(1,None),
                height=30 )
        self.editorElementDetails.add_widget(self.checkboxDim)

        self.editorElementDetails.add_widget(
            Button(
                text=currentType + " Width",
                size_hint=(1,None),
                height=30,
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                color=self.engineConfig.getThemeTextColor()
                )
            )
        self.detailsCommonWidth = TextInput(text=str(detailData['width']),
            size_hint=(1, None), height=30)
        self.editorElementDetails.add_widget(self.detailsCommonWidth)

        self.editorElementDetails.add_widget(
            Button(
                text= currentType + " Height",
                size_hint=(1,None),
                height=30,
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                color=self.engineConfig.getThemeTextColor() )
            )
        self.detailsCommonHeight = TextInput(text=detailData['height'], size_hint=(1, None), height=30)
        self.editorElementDetails.add_widget(self.detailsCommonHeight)

        # Percent dimensions
        self.editorElementDetails.add_widget(Label(text='Use Percent Dimensions', 
                color=self.engineConfig.getThemeTextColor(), size_hint=(1,None), height=30))
        self.checkboxPer = CheckBox(active=_isActiveCheckBoxPer, size_hint=(1,None),
                height=30)
        self.editorElementDetails.add_widget(self.checkboxPer)

        # Combine dimensions
        self.editorElementDetails.add_widget(Label(text='Use Combine Dimensions (None for disable)', 
                color=self.engineConfig.getThemeTextColor(), size_hint=(1,None), height=30))
        self.checkboxCombine = CheckBox(active=_isActiveCheckBoxCombine, size_hint=(1,None),
                height=30)
        self.editorElementDetails.add_widget(self.checkboxCombine)

        # Bind checkboxs for details box
        self.checkboxPer.bind(active=self.on_checkbox_per_active) # pylint disable=no-member
        self.checkboxDim.bind(active=self.on_checkbox_pixel_active) # pylint disable=no-member
        self.checkboxCombine.bind(active=self.on_checkbox_combine_active) # pylint disable=no-member

        # Hint
        self.commonHintXDetail = TextInput(text=str(detailData['size_hint_x']), size_hint=(1,None),
                height=30)
        self.editorElementDetails.add_widget(self.commonHintXDetail)
        self.commonHintYDetail = TextInput(text=str(detailData['size_hint_y']), size_hint=(1,None),
                height=30)
        self.editorElementDetails.add_widget(self.commonHintYDetail)

        # Colors elements
        clrPickerTextColor = ColorPicker(color=(detailData['color']), size_hint=(1,None),
                height=200)
        clrPickerBackgroundColor = ColorPicker(color=(detailData['bgColor']), size_hint=(1,None),
                height=200)

        self.editorElementDetails.add_widget(clrPickerBackgroundColor)
        self.editorElementDetails.add_widget(clrPickerTextColor)

        # Add all
        self.add_widget(self.editorElementDetails)

        # Bind
        clrPickerTextColor.bind(color=self.on_details_color) # pylint: disable=no-member
        clrPickerBackgroundColor.bind(color=self.on_details_bgcolor) # pylint: disable=no-member

        # Specific elemetn props
        #if str(detailData['layoutType']) == "Box" or str(detailData['layoutType']) == "Select layout type":
        self.showBoxLayoutDetails(detailData)
        #elif str(detailData['layoutType']) == "Grid":
        #    self.showBoxLayoutDetails(detailData)
        #elif str(detailData['layoutType']) == "Anchor":
        #    self.showBoxLayoutDetails(detailData)
        #elif str(detailData['layoutType']) == "Float":
        #    self.showBoxLayoutDetails(detailData)

    # Save details fast solution for now BUTTON
    def savePictureDetails(self, elementID, elementType,  instance):
        print("Save detail for ->" , elementID)
        # predefinition
        dimensionRole = "pixel"
        if self.checkboxDim.active == True: 
            local_size_hintX = None
            local_size_hintY = None
            # print("SET HINT NONE")
        elif self.checkboxPer.active == True:
            # print(" SET HINT ")
            if self.commonHintXDetail.text == "None":
                local_size_hintX = None
            else:
                local_size_hintX = float(self.commonHintXDetail.text)
            if self.commonHintYDetail.text == "None":
                local_size_hintY = None
            else:
                local_size_hintY = float(self.commonHintYDetail.text)
            dimensionRole = "hint"
        elif self.checkboxCombine.active == True:
            print(" SET COMBINE ")
            if self.commonHintXDetail.text == "None":
                local_size_hintX = None
            else:
                local_size_hintX = float(self.commonHintXDetail.text)
            if self.commonHintYDetail.text == "None":
                local_size_hintY = None
            else:
                local_size_hintY = float(self.commonHintYDetail.text)
            dimensionRole = "combine"
        # CrossK Element Data Interface
        calculatedButtonData = {
            "id": elementID,
            "name": self.commonDetailsNameText.text, # tag
            "type": elementType,
            "image": self.detailsPictureImage.text,
            "text": self.detailsCommonText.text,
            "fontSize": self.buttonDetailsFontSize.text,
            "color": self.newDetailsColor,
            "bgColor": self.newDetailsBgColor,
            "width": self.detailsCommonWidth.text,
            "height": self.detailsCommonHeight.text,
            "size_hint_x": self.commonHintXDetail.text,
            "size_hint_y": self.commonHintYDetail.text,
            "dimensionRole": dimensionRole,
            "attacher": self.attachEventCurrentElement.text,
            "pos_x": self.detailsCommonPositionX.text,
            "pos_y": self.detailsCommonPositionY.text,
            "pos_hint_x": self.detailsCommonPositionXHint.text,
            "pos_hint_y": self.detailsCommonPositionYHint.text,
        }
        # Collect data
        print(" CONSTRUCTED " , calculatedButtonData)
        # Load fresh data then replace for specific id and save it
        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')
        loadElements = self.store.get('renderComponentArray')['elements']
        self._add(loadElements, calculatedButtonData, elementID)

        print("SAVE -> " , loadElements)
        self.store.put('renderComponentArray', elements=loadElements )

        self.updateScene()
        self.sceneGUIContainer.selfUpdate()

        self.remove_widget(self.editorElementDetails)
        self.currentProjectMenuDropdown.open(self)

    ##############################################################################
    def _add(self,localStagedElements, calculatedLabelData, currentLayoutId):
        for index, item in enumerate(localStagedElements):
            if item['id'] == currentLayoutId:
                localStagedElements[index] = calculatedLabelData
                return localStagedElements
                break
            if item['type'] == 'LAYOUT':
                self._add(item['elements'], calculatedLabelData, currentLayoutId)
        return False
    ##############################################################################

    # Save details fast solution for now
    def saveLabelDetails(self, elementID, elementType,  instance):

        print("Save detail for ->" , elementID)
        # predefinition
        dimensionRole = "pixel"
        if self.checkboxDim.active == True: 
            local_size_hintX = None
            local_size_hintY = None
            # print("SET HINT NONE")
        elif self.checkboxPer.active == True:
            # print(" SET HINT ")
            if self.commonHintXDetail.text == "None":
                local_size_hintX = None
            else:
                local_size_hintX = float(self.commonHintXDetail.text)
            if self.commonHintYDetail.text == "None":
                local_size_hintY = None
            else:
                local_size_hintY = float(self.commonHintYDetail.text)
            dimensionRole = "hint"
        elif self.checkboxCombine.active == True:
            print(" SET COMBINE ")
            if self.commonHintXDetail.text == "None":
                local_size_hintX = None
            else:
                local_size_hintX = float(self.commonHintXDetail.text)
            if self.commonHintYDetail.text == "None":
                local_size_hintY = None
            else:
                local_size_hintY = float(self.commonHintYDetail.text)
            dimensionRole = "combine"

        # CrossK Element Data Interface
        calculatedLabelData = {
            "id": elementID,
            "name": self.commonDetailsNameText.text, # tag
            "type": elementType,
            "text": self.detailsCommonText.text,
            "fontSize": self.labelDetailsFontSize.text,
            "bold": str(self.checkboxIsBold.active),
            "color": self.newDetailsColor,
            "bgColor": self.newDetailsBgColor,
            "width": self.detailsCommonWidth.text,
            "height": self.detailsCommonHeight.text,
            "size_hint_x": self.commonHintXDetail.text,
            "size_hint_y": self.commonHintYDetail.text,
            "dimensionRole": dimensionRole,
            "pos_x": self.detailsCommonPositionX.text,
            "pos_y": self.detailsCommonPositionY.text,
            "pos_hint_x": self.detailsCommonPositionXHint.text,
            "pos_hint_y": self.detailsCommonPositionYHint.text,
        }

        # Collect data
        print(" CONSTRUCTED " , calculatedLabelData)

        # Load fresh data then replace for specific id and save it
        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')
        loadElements = self.store.get('renderComponentArray')['elements']
        
        TEST = self._add(loadElements, calculatedLabelData , elementID)
        print("AFTER ADD SAVE DETAIL S ELEMENTAR", TEST)

        print("SAVE -> " , loadElements)
        self.store.put('renderComponentArray', elements=loadElements)

        self.updateScene()
        self.sceneGUIContainer.selfUpdate()

        self.remove_widget(self.editorElementDetails)
        self.currentProjectMenuDropdown.open(self)

    # Save details fast solution for now
    def saveLayoutDetails(self, detailData,  instance):
        print("Save detail layout for " , detailData['type'])
        # predefinition
        dimensionRole = "pixel"
        if self.checkboxDim.active == True: 
            local_size_hintX = None
            local_size_hintY = None
            # print("SET HINT NONE")
        elif self.checkboxPer.active == True:
            # print(" SET HINT ")
            if self.commonHintXDetail.text == "None":
                local_size_hintX = None
            else:
                local_size_hintX = float(self.commonHintXDetail.text)
            if self.commonHintYDetail.text == "None":
                local_size_hintY = None
            else:
                local_size_hintY = float(self.commonHintYDetail.text)
            dimensionRole = "hint"
        elif self.checkboxCombine.active == True:
            print(" SET COMBINE ")
            if self.commonHintXDetail.text == "None":
                local_size_hintX = None
            else:
                local_size_hintX = float(self.commonHintXDetail.text)
            if self.commonHintYDetail.text == "None":
                local_size_hintY = None
            else:
                local_size_hintY = float(self.commonHintYDetail.text)
            dimensionRole = "combine"

        if str(detailData['layoutType']) == "Anchor" or str(detailData['layoutType']) == "Float":
            localAnchor_x = self.selectAnchor.text
            localAnchor_y = self.selectAnchorY.text
        else:
            localAnchor_x = 'center'
            localAnchor_y = 'center'

        # CrossK Element Data Interface
        calculatedButtonData = {
            "id": detailData['id'],
            "name": self.commonDetailsNameText.text,
            "type": "LAYOUT",
            "layoutType": self.selectBtn.text,
            "cols": self.colsInput.text,
            "rows": self.rowsInput.text,
            "elements": detailData['elements'],
            "orientation": self.detailsCommonLayoutOrientation.text,
            "padding": self.layoutPadding.text,
            "spacing": self.layoutSpacing.text,
            "color": self.newDetailsColor,
            "bgColor": self.newDetailsBgColor,
            "width": self.detailsCommonWidth.text,
            "height": self.detailsCommonHeight.text,
            "size_hint_x": self.commonHintXDetail.text,
            "size_hint_y": self.commonHintYDetail.text,
            "dimensionRole": dimensionRole,
            "anchor_x": localAnchor_x,
            "anchor_y": localAnchor_y,
            "pos_x": self.detailsCommonPositionX.text,
            "pos_y": self.detailsCommonPositionY.text,
            "pos_hint_x": self.detailsCommonPositionXHint.text,
            "pos_hint_y": self.detailsCommonPositionYHint.text,
            "swipe_threshold": self.swipeThresholdPageLayout.text
        }
        # ? maybe
        # Collect data
        print(" CONSTRUCTED " , calculatedButtonData)

        # Load fresh data then replace for specific id and save it
        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')
        loadElements = self.store.get('renderComponentArray')['elements']
        self._add(loadElements, calculatedButtonData, detailData['id'])

        print("SAVE -> " , loadElements)
        self.store.put('renderComponentArray', elements=loadElements )

        self.updateScene()
        self.sceneGUIContainer.selfUpdate()

        self.remove_widget(self.editorElementDetails)
        self.currentProjectMenuDropdown.open(self)

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

    def on_details_color(self, instance, value):
        self.newDetailsColor = (value[0], value[1], value[2], 1 )

    def on_details_bgcolor(self, instance, value):
        self.newDetailsBgColor = (value[0], value[1], value[2], 1 )

    def on_checkbox_pixel_active(instance, value1, value):
        # print(" 1 : ", instance) print(" 2 ", value1) print(" 3 ", value)
        if value:
            print('The dimensions pixel', value1, 'is active')
            instance.checkboxPer.active = False
            instance.checkboxCombine.active = False
        else:
            print('The dimensions pixel', value1, 'is inactive')

    def on_checkbox_per_active(instance, value1, value):
        # print(" input percent ", value) print(" acess ", instance)
        if value:
            print('The dimensions percent', value1, 'is active')
            instance.checkboxDim.active = False
            instance.checkboxCombine.active = False
        else:
            print('The dimensions percent', value1, 'is inactive')

    def on_checkbox_combine_active(instance, value1, value):
        # print(" input percent ", value) print(" acess ", instance)
        if value:
            print('The dimensions checkbox', value1, 'is active')
            instance.checkboxDim.active = False
            instance.checkboxPer.active = False
        else:
            print('The dimensions checkbox', value1, 'is inactive')

    def closeWithNoSaveDetails(self, instance):
        # self.currentProjectMenuDropdown.open(self)
        if self.editorElementDetails is None:
            return 0
        self.remove_widget(self.editorElementDetails)
        # self.currentProjectMenuDropdown.open(self)

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
                        font_size=item['fontSize'],
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
                        font_size=item['fontSize'],
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
                        font_size=item['fontSize'],
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
                        multiline=True,
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
                        cols=int(item['cols']),
                        rows=int(item['rows']),
                        spacing=float(item['spacing']),
                        padding=float(item['padding']),
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
                    self._readElementar(myAttacher, item['elements'])

                elif item['layoutType'] == "Page":
                    # PageLayout does not currently honor the 
                    # size_hint, size_hint_min, size_hint_max, or pos_hint properties.
                    # page: 3
                    # border: 120
                    # swipe_threshold: .4
                    Attacher = PageLayout
                    myAttacher = Attacher(
                        page=1,
                        border=120,
                        swipe_threshold=float(item['swipe_threshold'])
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
                    self._readElementar(myAttacher, item['elements'])

                elif item['layoutType'] == "Relative":
                    Attacher = Relative
                elif item['layoutType'] == "Scatter":
                    Attacher = Scatter
                elif item['layoutType'] == "Stack":
                    Attacher = Stack

                # print('its lauout ,read sub items ->>>')

            if item != None and item['type'] == 'PICTURE_CLICKABLE':
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
                        font_size=item['fontSize'],
                        pos_hint={ 'x': float(item['pos_hint_x']), 'y': float(item['pos_hint_y'])}, # maybe disable
                        text=item['text'],
                        color=item['color'],
                        background_normal= item['image'],
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
                        font_size=item['fontSize'],
                        color=item['color'],
                        background_normal= item['image'],
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
                        #pos=(float(item['pos_x']), float(item['pos_y'])),
                        #pos_hint_x=float(item['pos_hint_x']),
                        #pos_hint_y=float(item['pos_hint_y']),
                        #font_size=item['fontSize'],
                        text=item['text'],
                        color=item['color'],
                        background_normal= item['image'],
                        background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY,
                        height=item['height'],
                        width=item['width'],
                        # on_press=partial(self.engineLayout.attachEvent, item['attacher'])
                    )

                currentCointainer.add_widget(constructedApplicationButton)

    def updateScene(self):

        # self.closeWithNoSaveDetails()

        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')
        loadElements = self.store.get('renderComponentArray')['elements']

        print('----------------------------------')
        print('CLEAR, UPDATE SCENE [engineLayout]')
        print('----------------------------------')
        self.engineLayout.clear_widgets()

        self._readElementar(self.engineLayout ,loadElements)

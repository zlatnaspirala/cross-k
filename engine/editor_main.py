import kivy
from kivy.config import Config

print(kivy.__version__)
kivy.require('2.0.0')

from functools import partial
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.metrics import dp, sp, pt
from kivy.core.window import Window
from engine.editor.layout import EngineLayout
from engine.editor.sceneGUICOntainer import SceneGUIContainer
from engine.config import EngineConfig
from engine.common.modifycation import AlignedTextInput
from engine.common.commons import getAboutGUI, getMessageBoxYesNo
from engine.common.operationsButton import EditorOperationButton
from engine.common.operationsLabel import EditorOperationLabel
from engine.common.operationsBox import EditorOperationBox
from engine.common.enginePackage import PackagePopup
from kivy.uix.image import Image, AsyncImage 
from kivy.uix.textinput import TextInput
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown

from kivy.storage.jsonstore import JsonStore
from kivy.app import App

# from datetime import datetime

import os
import threading
import uuid


# Selected source
#from win32api import GetSystemMetrics
#print("Width =", GetSystemMetrics(0))
#print("Height =", GetSystemMetrics(1))

# Storage/Files operations
# from jnius import autoclass  # SDcard Android
from shutil import copyfile
# copyfile(src, dst)

# Editor main is only editor not inpact projects files.
class EditorMain(BoxLayout):

    def CreateLoadInstanceGUIBox(self, instance):
        print("CreateLoadInstanceGUIBox ..." )
        #self.rows = 2  row_force_default=True, row_default_height=10

        self.createLoadProjectLayoutEditor = GridLayout(padding= 0 , rows=5, row_force_default=True, row_default_height=50)
        self.add_widget(self.createLoadProjectLayoutEditor)

        self.createLoadProjectLayoutEditor.add_widget(Label(text='CROSS[b]K[/b]', markup=True, font_size="30sp" ))
        self.createLoadProjectLayoutEditor.add_widget(Button(text='0.1.0', size=(60, 100), size_hint=(None, None) ))

        self.newProjectBtn = Button(text='Load project', size_hint=(.1, .2),
          on_press=self.loadProjectFiles)

        self.newProjectTitle = Label(text='Project name:')
        self.createLoadProjectLayoutEditor.add_widget(self.newProjectTitle)
        # self.projectName = TextInput(multiline=False, size_hint=(.1, .05) )
        self.projectName = self.get_input('middle', 'center')

        self.createLoadProjectLayoutEditor.add_widget(self.projectName)
        self.createLoadProjectLayoutEditor.add_widget(self.newProjectBtn)

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

        # print("LOAD PROJECT PROCEDURE")
        ###############################################################
        # App root layout instance
        ###############################################################
        self.engineLayout = EngineLayout(orientation="vertical")

        # Step : runtime setup project global data.
        # ProjectName and ProjectPath root , also setup config.
        self.engineConfig.currentProjectName = self.projectName.text
        self.engineConfig.currentProjectPath = CURRENT_PATH
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

        self.updateScene(loadElements)

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

    def createProjectFiles(self, instance):

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

        print("NEW PROJECT PROCEDURE")

        ###############################################################
        # App root layout instance
        ###############################################################
        self.engineLayout = EngineLayout()

        # Step : runtime setup project global data.
        # ProjectName and ProjectPath root , also setup config.
        self.engineConfig.currentProjectName = self.projectName.text
        self.engineConfig.currentProjectPath = CURRENT_PATH
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

        # Loading RENDER ELEMETS

        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')

        print(" >>self.engineLayout.currentProjectName>> ", self.engineLayout.currentProjectPath)
        # error
        # put some values , date=datetime.now()

        self.store.put('projectInfo', name=self.projectName.text, version='beta')
        self.store.put('defaultLayout', layoutType='boxLayout', orientation='horizontal')
        self.store.put('renderComponentArray', elements=[])

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

        # or guess the key/entry for a part of the key
        #for item in store.find(name='Gabriel'):
        #    print('tshirtmans index key is', item[0])
        #    print('his key value pairs are', str(item[1]))
        print("CrossK project with name -> ", self.projectName.text, " -> created.")

    def CreateNewInstanceGUIBox(self, instance):
        print("CreateNewInstanceGUIBox ..." )
        #self.rows = 2  row_force_default=True, row_default_height=10

        self.createNewProjectLayoutEditor = GridLayout(padding= 0 , rows=5, row_force_default=True, row_default_height=50)
        self.add_widget(self.createNewProjectLayoutEditor)

        self.createNewProjectLayoutEditor.add_widget(Label(text='CROSS[b]K[/b]', markup=True, font_size="30sp" ))
        self.createNewProjectLayoutEditor.add_widget(Button(text='Cancel', size=(70, 70), size_hint=(None, None), on_press=self.createNewProjectGUICancel ))

        self.newProjectBtn = Button(text='Create new', size_hint=(.1, .2),
          on_press=self.createProjectFiles)

        self.newProjectTitle = Label(text='Project name:')
        self.createNewProjectLayoutEditor.add_widget(self.newProjectTitle)
        # self.projectName = TextInput(multiline=False, size_hint=(.1, .05) )
        self.projectName = self.get_input('middle', 'center')

        self.createNewProjectLayoutEditor.add_widget(self.projectName)
        self.createNewProjectLayoutEditor.add_widget(self.newProjectBtn)

    def createNewProjectGUICancel(self, instance):
        self.remove_widget(self.createNewProjectLayoutEditor)

    def packageWinApp(self, instance):
        test = PackagePopup(engineConfig=self.engineConfig)
        print("Package application for windows started")
        
    def __init__(self, **kwargs):
        super(EditorMain, self).__init__(**kwargs)

        ####################################################
        # Engine config , Colors Theme
        ####################################################
        self.engineConfig = EngineConfig()
        self.engineConfig.getVersion()

        # self.packageWinApp()

        # Initial call for aboutGUI
        getAboutGUI()

        Window.size = (sp(1200), sp(768))
        # Window.size = (1200, 768)
        # print("WHAT IS P S " , Window.size[0] )
        #Window.top = 10
        #Window.left = 500
        #Window.fullscreen = True
        Window.clearcolor = (0, 0, 0, 1)
       
        # Run time schortcut vars
        #self.orientation='vertical'
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
        self.editorMenuLayout = BoxLayout(orientation='vertical', size_hint=(None, 1), width=300 )
        self.add_widget(self.editorMenuLayout)

        # predefined var for Details
        self.editorElementDetails = None
        
        self.packageDropdown = DropDown()
        self.packageDropdown.dismiss()

        # 
        packWindows = Button(text='Make package for windows',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(None, None),  height=30, width=200,
                      on_press=self.packageWinApp)
        packLinux = Button(text='Make package for Linux',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(None, None),  height=30, width=200,
                      on_press=self.packageWinApp)
        self.packageDropdown.add_widget(packWindows)
        self.packageDropdown.add_widget(packLinux)
        self.editorMenuLayout.add_widget(self.packageDropdown)

        #
        self.currentProjectMenuDropdown = DropDown()
        self.currentProjectMenuDropdown.dismiss()
        
        toolsAddBox = Button(text='Add Box',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(None, None),  height=30, width=200,
                      on_press=self.addNewBoxGUI)
        toolsAddBtn = Button(text='Add Button',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(None, None),  height=30, width=200,
                      on_press=self.addNewButtonGUI)
        toolsAddText = Button(text='Add Text',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(None, None),  height=30, width=200,
                      on_press=self.addNewLabelGUI)
        self.currentProjectMenuDropdown.add_widget(toolsAddBox)
        self.currentProjectMenuDropdown.add_widget(toolsAddBtn)
        self.currentProjectMenuDropdown.add_widget(toolsAddText)

        self.editorMenuLayout.add_widget(self.currentProjectMenuDropdown)

        # Application Menu Drop menu
        self.appMenuDropdown = DropDown()
        self.appMenuDropdown.dismiss()

        btn = Button(text='Create new project',
                     color=(self.engineConfig.getThemeTextColor()),
                     size_hint=(None, None), height=30, width=200)
        self.appMenuDropdown.add_widget(btn)

        loadBtn = Button(text='Load project',
                     color=(self.engineConfig.getThemeTextColor()),
                     size_hint=(None, None), height=30, width=200)
        self.appMenuDropdown.add_widget(loadBtn)
        loadBtn.bind(on_press=self.CreateLoadInstanceGUIBox)

        self.editorMenuLayout.add_widget(self.appMenuDropdown)
 
        #btn.bind(on_release=lambda btn: appMenuDropdown.select(btn.text))
        btn.bind(on_press=self.CreateNewInstanceGUIBox)
 
        MakePackageBtn = Button(text='Make package',
                     color=(self.engineConfig.getThemeTextColor()),
                     size_hint=(None, None), height=30, width=200)
        MakePackageBtn.bind(on_release=self.packageDropdown.open)
        self.editorMenuLayout.add_widget(MakePackageBtn)


        editorTools = Button(text='Tools', color=(self.engineConfig.getThemeTextColor()), size_hint=(None, None), height=30, width=200)
        editorTools.bind(on_release=self.currentProjectMenuDropdown.open)
        self.editorMenuLayout.add_widget(editorTools)

        mainbutton = Button(markup=True , text='[b][color=ff3333]A[/color]pplication[/b]', color=(self.engineConfig.getThemeTextColor()), size_hint=(None, None), height=30, width=200)
        # mainbutton.bind(on_release=lambda mainbutton:self.openApplicationMenuBtn(self))
        mainbutton.bind(on_release=self.appMenuDropdown.open)
        self.editorMenuLayout.add_widget(mainbutton)

    def openApplicationMenuBtn(self, instance):
        #self.appMenuDropdown.open(self)
        print("test >!>>!, self.appMenuDropdown", self.appMenuDropdown)

    def get_input(self, v, h):
        # Test stage for this
        return AlignedTextInput(text='Project1', halign=h, valign=v, height=100)

    def addNewButtonGUI(self, instance):
        print('BUTTON.....................................')
        operationAddTest = EditorOperationButton(
            store=self.store,
            engineLayout=self.engineLayout,
            engineRoot=self
        )

    def addNewBoxGUI(self, instance):
        print('LAYOUT.....................................')
        operationAddTest = EditorOperationBox(
            store=self.store,
            engineLayout=self.engineLayout,
            engineRoot=self
        )

    def addNewLabelGUI(self, instance):
        print('LABEL.....................................')
        operationAddTest = EditorOperationLabel(
            store=self.store,
            engineLayout=self.engineLayout,
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
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=50 )
        )
        # ID
        self.editorElementDetails.add_widget(
            Button(
                text=str(detailData['id']),
                size_hint=(1,None),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=50 )
        )
        # name - tag
        self.editorElementDetails.add_widget(
            Button(
                text="Name(Tag) " + detailData['name'],
                size_hint=(1,None),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=50 )
            )
        self.commonDetailsNameText = TextInput(
            text=detailData['name'],
            size_hint=(1, None),
            height=50
        )
        self.editorElementDetails.add_widget(self.commonDetailsNameText)
        # text
        self.editorElementDetails.add_widget(
            Button(
                text= currentType + " Text",
                size_hint=(1,None),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=50 )
            )


        # half common btn , label 
        if "text" in detailData:
            print("detailData['text'] sure, it was defined.")
            if (detailData['text'] != null ):
                self.detailsCommonText = TextInput(text=detailData['text'], size_hint=(1, None), height=50)
                self.editorElementDetails.add_widget(self.detailsCommonText)
        else:
            print("detailData['text'] NOT defined.")

        # Checkbox use pixel dimesion system
        self.editorElementDetails.add_widget(Label(
            text='Use Pixel Dimensions', size_hint=(1,None),
                height=50, color=self.engineConfig.getThemeTextColor()))
       
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
                height=50 )
        self.editorElementDetails.add_widget(self.checkboxDim)

        self.editorElementDetails.add_widget(
            Button(
                text=currentType + " Width",
                size_hint=(1,None),
                height=50,
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                color=self.engineConfig.getThemeTextColor()
                )
            )
        self.detailsCommonWidth = TextInput(text=str(detailData['width']), size_hint=(1, None), height=50)
        self.editorElementDetails.add_widget(self.detailsCommonWidth)

        self.editorElementDetails.add_widget(
            Button(
                text= currentType + " Height",
                size_hint=(1,None),
                height=50,
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                color=self.engineConfig.getThemeTextColor() )
            )
        self.detailsCommonHeight = TextInput(text=detailData['height'], size_hint=(1, None), height=50)
        self.editorElementDetails.add_widget(self.detailsCommonHeight)

        # Percent dimensions
        self.editorElementDetails.add_widget(Label(text='Use Percent Dimensions', 
                color=self.engineConfig.getThemeTextColor(), size_hint=(1,None), height=50))
        self.checkboxPer = CheckBox(active=_isActiveCheckBoxPer, size_hint=(1,None),
                height=50)
        self.editorElementDetails.add_widget(self.checkboxPer)

        # Combine dimensions
        self.editorElementDetails.add_widget(Label(text='Use Combine Dimensions (None for disable)', 
                color=self.engineConfig.getThemeTextColor(), size_hint=(1,None), height=50))
        self.checkboxCombine = CheckBox(active=_isActiveCheckBoxCombine, size_hint=(1,None),
                height=50)
        self.editorElementDetails.add_widget(self.checkboxCombine)

        # Bind checkboxs for details box
        self.checkboxPer.bind(active=self.on_checkbox_per_active) # pylint disable=no-member
        self.checkboxDim.bind(active=self.on_checkbox_pixel_active) # pylint disable=no-member
        self.checkboxCombine.bind(active=self.on_checkbox_combine_active) # pylint disable=no-member
 
        self.commonHintXDetail = TextInput(text=str(detailData['size_hint_x']), size_hint=(1,None),
                height=50)
        self.editorElementDetails.add_widget(self.commonHintXDetail)
        self.commonHintYDetail = TextInput(text=str(detailData['size_hint_y']), size_hint=(1,None),
                height=50)
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

    # def showButtonDetails(self, detailData, instance):
    def showButtonDetails(self, detailData):
                

        self.editorElementDetails.add_widget(
            Label(
                text="Delete button '" + detailData['name'] + "' ",
                size_hint=(1,None),
                height=40,
                color=self.engineConfig.getThemeTextColor(),
                on_press=partial(self.saveDetails, str(detailData['id']), str(detailData['type']) ))
            )

        self.editorElementDetails.add_widget(
            Button(
                text="delete button",
                size_hint=(1,None),
                height=40,
                color=self.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('warn')),
                on_press=partial(self.delete, str(detailData['id']), str(detailData['type']) ))
            )


        self.editorElementDetails.add_widget(
            Button(
                text="Save changes",
                size_hint=(1,None),
                height=120,
                color=self.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                on_press=partial(self.saveDetails, str(detailData['id']), str(detailData['type']) ))
            )

        self.editorElementDetails.add_widget(
            Button(
                text="Cancel",
                size_hint=(1,None),
                height=120,
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                on_press=self.cloaseWithNoSaveDetails
            ))

    # Button end block

    # label Block

    def showLabelDetails(self, detailData):
        print("LABEL detailData-> ", detailData)
        # Clear

        self.editorElementDetails.add_widget(Label(text='Use Bold', 
                color=self.engineConfig.getThemeTextColor(), size_hint=(1,None), height=50))

        self.checkboxIsBold = CheckBox(active=False, size_hint=(1,None),
                height=50)
        self.editorElementDetails.add_widget(self.checkboxIsBold)

        # name - tag
        self.editorElementDetails.add_widget(
            Button(
                text="Font size ",
                size_hint=(1,None),
                height=50 )
            )

        self.labelDetailsFontSize = TextInput(
            text=detailData['fontSize'],
            size_hint=(1, None),
            height=50
        )
        self.editorElementDetails.add_widget(self.labelDetailsFontSize)

        self.editorElementDetails.add_widget(
            Button(
                text="Save changes",
                size_hint=(1,None),
                height=120,
                color=self.engineConfig.getThemeTextColor(),
                on_press=partial(self.saveLabelDetails, str(detailData['id']), str(detailData['type']) ))
            )

        self.editorElementDetails.add_widget(
            Button(
                text="Cancel",
                size_hint=(1,None),
                height=120,
                on_press=self.cloaseWithNoSaveDetails
            ))

    # End of Label block

    ####################

    def showBoxLayoutDetails(self, detailData):

        self.editorElementDetails.add_widget(
            Label(
                text="Delete button '" + detailData['name'] + "' ",
                size_hint=(1,None),
                height=40,
                color=self.engineConfig.getThemeTextColor(),
                on_press=partial(self.saveLayoutDetails, str(detailData['id']), str(detailData['type']) ))
            )

        self.editorElementDetails.add_widget(
            Button(
                text="delete button",
                size_hint=(1,None),
                height=40,
                color=self.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('warn')),
                on_press=partial(self.delete, str(detailData['id']), str(detailData['type']) ))
            )


        self.editorElementDetails.add_widget(
            Button(
                text="Save changes",
                size_hint=(1,None),
                height=120,
                color=self.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                on_press=partial(self.saveLayoutDetails, str(detailData['id']), str(detailData['type']) ))
            )

        self.editorElementDetails.add_widget(
            Button(
                text="Cancel",
                size_hint=(1,None),
                height=120,
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                on_press=self.cloaseWithNoSaveDetails
            ))


        # Buttonblock



    ### LAYOUTS 
    def __setLayoutType(self, instance):
        print("..........", instance)
        self.selectBtn.text = instance.text
        self.layoutTypeList.select(self.btnBox.text)

    def showCommonLayoutDetails(self, detailData, instance):
        print("COMMON.DETAILS.LAYOUT......... ", detailData)
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
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=50 )
        )
        # ID
        self.editorElementDetails.add_widget(
            Button(
                text=str(detailData['id']),
                size_hint=(1,None),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=50 )
        )
        # name - tag
        self.editorElementDetails.add_widget(
            Button(
                text="Name(Tag) " + detailData['name'],
                size_hint=(1,None),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=50 )
            )
        self.commonDetailsNameText = TextInput(
            text=detailData['name'],
            size_hint=(1, None),
            height=50
        )
        self.editorElementDetails.add_widget(self.commonDetailsNameText)
        # text
        self.editorElementDetails.add_widget(
            Button(
                text= currentType + " Orientation",
                size_hint=(1,None),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                height=50 )
            )

        # half common btn , label 
        self.detailsCommonLayoutOrientation = TextInput(text=detailData['orientation'], size_hint=(1, None), height=50)
        self.editorElementDetails.add_widget(self.detailsCommonLayoutOrientation)

        self.editorElementDetails.add_widget(Label(text='Padding'))
        self.padding = AlignedTextInput(text='vertical', halign="middle", valign="center")
        self.editorElementDetails.add_widget(self.padding)

        self.editorElementDetails.add_widget(Label(text='Spacing'))
        self.spacing = AlignedTextInput(text='vertical', halign="middle", valign="center")
        self.editorElementDetails.add_widget(self.spacing)


        self.layoutTypeList = DropDown()
        self.selectBtn = Button(text='Select layout type', on_press=self.layoutTypeList.open)
        self.editorElementDetails.add_widget(self.selectBtn)
        
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

        self.editorElementDetails.add_widget(self.layoutTypeList)


        # Checkbox use pixel dimesion system
        self.editorElementDetails.add_widget(Label(
            text='Use Pixel Dimensions', size_hint=(1,None),
                height=50, color=self.engineConfig.getThemeTextColor()))
       
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
                height=50 )
        self.editorElementDetails.add_widget(self.checkboxDim)

        self.editorElementDetails.add_widget(
            Button(
                text=currentType + " Width",
                size_hint=(1,None),
                height=50,
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                color=self.engineConfig.getThemeTextColor()
                )
            )
        self.detailsCommonWidth = TextInput(text=str(detailData['width']), size_hint=(1, None), height=50)
        self.editorElementDetails.add_widget(self.detailsCommonWidth)

        self.editorElementDetails.add_widget(
            Button(
                text= currentType + " Height",
                size_hint=(1,None),
                height=50,
                background_normal= '',
                background_color=(self.engineConfig.getThemeBackgroundColor()),
                color=self.engineConfig.getThemeTextColor() )
            )
        self.detailsCommonHeight = TextInput(text=detailData['height'], size_hint=(1, None), height=50)
        self.editorElementDetails.add_widget(self.detailsCommonHeight)

        # Percent dimensions
        self.editorElementDetails.add_widget(Label(text='Use Percent Dimensions', 
                color=self.engineConfig.getThemeTextColor(), size_hint=(1,None), height=50))
        self.checkboxPer = CheckBox(active=_isActiveCheckBoxPer, size_hint=(1,None),
                height=50)
        self.editorElementDetails.add_widget(self.checkboxPer)

        # Combine dimensions
        self.editorElementDetails.add_widget(Label(text='Use Combine Dimensions (None for disable)', 
                color=self.engineConfig.getThemeTextColor(), size_hint=(1,None), height=50))
        self.checkboxCombine = CheckBox(active=_isActiveCheckBoxCombine, size_hint=(1,None),
                height=50)
        self.editorElementDetails.add_widget(self.checkboxCombine)

        # Bind checkboxs for details box
        self.checkboxPer.bind(active=self.on_checkbox_per_active) # pylint disable=no-member
        self.checkboxDim.bind(active=self.on_checkbox_pixel_active) # pylint disable=no-member
        self.checkboxCombine.bind(active=self.on_checkbox_combine_active) # pylint disable=no-member
 
        self.commonHintXDetail = TextInput(text=str(detailData['size_hint_x']), size_hint=(1,None),
                height=50)
        self.editorElementDetails.add_widget(self.commonHintXDetail)
        self.commonHintYDetail = TextInput(text=str(detailData['size_hint_y']), size_hint=(1,None),
                height=50)
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
        if str(detailData['layoutType']) == "Box":
            self.showBoxLayoutDetails(detailData)
        elif str(detailData['layoutType']) == "Grid":
            self.showBoxLayoutDetails(detailData)

    ####################

    # Save details fast solution for now
    def saveDetails(self, elementID, elementType,  instance):

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
            "text": self.detailsCommonText.text,
            "color": self.newDetailsColor,
            "bgColor": self.newDetailsBgColor,
            "width": self.detailsCommonWidth.text,
            "height": self.detailsCommonHeight.text,
            "size_hint_x": self.commonHintXDetail.text,
            "size_hint_y": self.commonHintYDetail.text,
            "dimensionRole": dimensionRole
        }

        # Collect data
        print(" CONSTRUCTED " , calculatedButtonData)

        # Load fresh data then replace for specific id and save it
        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')
        loadElements = self.store.get('renderComponentArray')['elements']
        for index, item in enumerate(loadElements):
            print("index", index)
            if item['id'] == elementID:
                print('I FOUND REFS REPLACE UPDATE STORE ', item['dimensionRole'])
                loadElements[index] = calculatedButtonData

        print("SAVE -> " , loadElements)
        self.store.put('renderComponentArray', elements=loadElements )

        self.updateScene(loadElements)
        self.sceneGUIContainer.selfUpdate()

        self.remove_widget(self.editorElementDetails)
        self.currentProjectMenuDropdown.open(self)

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
        calculatedButtonData = {
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
            "dimensionRole": dimensionRole
        }

        # Collect data
        print(" CONSTRUCTED " , calculatedButtonData)

        # Load fresh data then replace for specific id and save it
        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')
        loadElements = self.store.get('renderComponentArray')['elements']
        for index, item in enumerate(loadElements):
            print("index", index)
            if item['id'] == elementID:
                print('I FOUND REFS REPLACE UPDATE STORE ', item['dimensionRole'])
                loadElements[index] = calculatedButtonData

        print("SAVE -> " , loadElements)
        self.store.put('renderComponentArray', elements=loadElements )

        self.updateScene(loadElements)
        self.sceneGUIContainer.selfUpdate()

        self.remove_widget(self.editorElementDetails)
        self.currentProjectMenuDropdown.open(self)



    ####################

    # Save details fast solution for now
    def saveLayoutDetails(self, elementID, elementType,  instance):

        print("Save detail layout for ->" , elementID)
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
            "name": self.commonDetailsNameText.text,
            "type": "LAYOUT",
            "layoutType": self.selectBtn.text,
            "items": "[1,2,3]",
            "orientation": self.detailsCommonLayoutOrientation.text,
            "padding": self.padding.text,
            "spacing": self.spacing.text,
            "color": self.newBtnColor,
            "bgColor": self.newBtnBgColor,
            "width": self.buttonWidthText.text,
            "height": self.buttonHeightText.text,
            "size_hint_x": str(self.buttonHintX.text),
            "size_hint_y": str(self.buttonHintY.text),
            "dimensionRole": dimensionRole
        } 

        # Collect data
        print(" CONSTRUCTED " , calculatedButtonData)

        # Load fresh data then replace for specific id and save it
        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')
        loadElements = self.store.get('renderComponentArray')['elements']
        for index, item in enumerate(loadElements):
            print("index", index)
            if item['id'] == elementID:
                print('I FOUND REFS REPLACE UPDATE STORE ', item['dimensionRole'])
                loadElements[index] = calculatedButtonData

        print("SAVE -> " , loadElements)
        self.store.put('renderComponentArray', elements=loadElements )

        self.updateScene(loadElements)
        self.sceneGUIContainer.selfUpdate()

        self.remove_widget(self.editorElementDetails)
        self.currentProjectMenuDropdown.open(self)

#######################

    # Delete button action
    def delete(self, elementID, elementType,  instance):
        print("delete element !")
        # updaet always
        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')
        loadElements = self.store.get('renderComponentArray')['elements']

    # Details box
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

    def cloaseWithNoSaveDetails(self, instance):
        self.remove_widget(self.editorElementDetails)
        self.currentProjectMenuDropdown.open(self)

    def _readElementar(self, currentCointainer, loadElements):

        print("read elementar current container : ", currentCointainer)
        # print("read elementar current loadElements ARRAY : ", loadElements)

        for item in loadElements:
        # print("......", item['type'])
            if item['type'] == 'BUTTON':
                # print('its button , coming from root editor layout , list in root also in sceneGUIContainer.->>>')
                local_size_hintX = None
                local_size_hintY= None

                if item['dimensionRole'] == "pixel":
                    local_size_hintX = None
                    local_size_hintY= None
                    self.engineLayout.add_widget( Button(
                        text=item['text'],
                        color=item['color'],
                        background_normal= '',
                        background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY,
                        height=item['height'],
                        width=item['width'])
                    )
                elif item['dimensionRole'] == "hint":

                    if item['size_hint_x'] == "None":
                        local_size_hintX = None
                    else:
                        local_size_hintX = item['size_hint_x']

                    if item['size_hint_y'] == "None":
                        local_size_hintY = None
                    else:
                        local_size_hintY = item['size_hint_y']


                    self.engineLayout.add_widget( Button(
                        text=item['text'],
                        color=item['color'],
                        background_normal= '',
                        background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY)
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

                    self.engineLayout.add_widget( Button(
                        text=item['text'],
                        color=item['color'],
                        background_normal= '',
                        background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY,
                        height=item['height'],
                        width=item['width'])
                    )

            if item['type'] == 'LABEL':
                # print('its button , coming from root editor layout , list in root also in sceneGUIContainer.->>>')
                local_size_hintX = None
                local_size_hintY= None

                if item['dimensionRole'] == "pixel":
                    local_size_hintX = None
                    local_size_hintY= None
                    self.engineLayout.add_widget( Label(
                        text=item['text'],
                        color=item['color'],
                        font_size=item['fontSize'], # add
                        bold=item['bold'],    # add
                        padding_x= 0, # test
                        padding_y= 0, # test
                        center=(1,1), # test
                        font_blended= True, # test
                        #background_normal= '',
                        #background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY,
                        height=item['height'],
                        width=item['width'])
                    )
                elif item['dimensionRole'] == "hint":

                    if item['size_hint_x'] == "None":
                        local_size_hintX = None
                    else:
                        local_size_hintX = item['size_hint_x']

                    if item['size_hint_y'] == "None":
                        local_size_hintY = None
                    else:
                        local_size_hintY = item['size_hint_y']


                    self.engineLayout.add_widget( Label(
                        text=item['text'],
                        color=item['color'],
                        font_size=item['fontSize'], # add
                        bold=item['bold'],    # add
                        padding_x= 0, # test
                        padding_y= 0, # test
                        center=(1,1), # test
                        #background_normal= '',
                        #background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY)
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

                    self.engineLayout.add_widget( Label(
                        text=item['text'],
                        color=item['color'],
                        font_size=item['fontSize'], # add
                        bold=item['bold'],    # add
                        padding_x= 0, # test
                        padding_y= 0, # test
                        center=(1,1), # test
                        #background_normal= '',
                        #background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY,
                        height=item['height'],
                        width=item['width'])
                    )

            if item['type'] == 'LAYOUT':

                # determinate type
                if item['layoutType'] == "Box":

                    ###############################
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

                    ###############################

                    Attacher = BoxLayout
                    print("BOX_>>>>>>>>>>>>>>>>>>>")
                    currentCointainer.add_widget( Attacher(
                        #text=item['text'],
                        orientation=item['orientation'],
                        spacing=float(item['spacing']),
                        padding=float(item['padding']),
                        #color=item['color'],
                        #background_normal= '',
                        #background_color= item['bgColor'],
                        size_hint_x=local_size_hintX,
                        size_hint_y=local_size_hintY)
                    )

                elif item['layoutType'] == "Anchor":
                    Attacher = AnchorLayout
                elif item['layoutType'] == "Float":
                    Attacher = FloatLayout
                elif item['layoutType']  == "Grid":
                    Attacher = GridLayout
                elif item['layoutType'] == "Page":
                    Attacher = PageLayout
                elif item['layoutType'] == "Relative":
                    Attacher = Relative
                elif item['layoutType'] == "Scatter":
                    Attacher = Scatter
                elif item['layoutType'] == "Stack":
                    Attacher = Stack

                print('its lauout ,read sub items ->>>')
                print('its lauout ,read sub items ->>>', item["layoutType"])
                # _readElementar

    def updateScene(self, loadElements):

        print('CLEAR, UPDATE SCENE [engineLayout]')
        print('----------------------------------')
        self.engineLayout.clear_widgets()
        self.engineLayout.clear_widgets()

        self._readElementar(self.engineLayout ,loadElements)

 
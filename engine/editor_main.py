import kivy
from kivy.config import Config

print(kivy.__version__)
kivy.require('2.0.0')

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
from engine.common.operations import EditorOperationAdd
from kivy.uix.image import Image, AsyncImage 

from kivy.storage.jsonstore import JsonStore
from kivy.app import App
#from datetime import datetime
import os



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

        print("LOAD PROJECT PROCEDURE")

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
        # Clear and remove engine editor widget
        # self.createNewProjectLayoutEditor.clear_widgets()

        self.remove_widget(self.createLoadProjectLayoutEditor)
        self.add_widget(self.engineLayout)

        # Loading RENDER ELEMETS
        self.store = JsonStore(self.engineLayout.currentProjectPath + '/' + self.projectName.text + '.json')
        loadElements = self.store.get('renderComponentArray')['elements']

        for item in loadElements:
            # print("......", item['type'])
            if item['type'] == 'BUTTON':
                # print('its button , coming from root editor layout , list in root also in sceneGUIContainer.->>>')
                self.engineLayout.add_widget( Button(
                    text=item['text'],
                    color=item['color'],
                    size_hint=(None, None),
                    height=item['height'],
                    width=item['width'])
                )
        
        # Sync call SceneGUIContainer constructor
        # pass store path like arg to get clear updated data intro sceneGUIContainer...
        self.sceneGUIContainer = SceneGUIContainer(
            storePath=self.fullProjectStorePath,
            orientation='vertical',
            engineRoot=self
            #size=(100, 300) 
        )
        # orientation="vertical"
        self.editorMenuLayout.add_widget(self.sceneGUIContainer)

        # print(" >>self.engineLayout.currentProjectName>> ", self.engineLayout.currentProjectPath)
        # error
        # put some values , date=datetime.now()
        
        # self.store.put('projectInfo', name=self.projectName.text, version='beta')
        # self.store.put('defaultLayout', layoutType='boxLayout', orientation='horizontal')
        # self.store.put('renderComponentArray', elements=[])

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

    def __init__(self, **kwargs):
        super(EditorMain, self).__init__(**kwargs)

        ####################################################
        # Engine config , Colors Theme
        ####################################################
        self.engineConfig = EngineConfig()
        self.engineConfig.getVersion()
       
        # Initial call for aboutGUI
        getAboutGUI()

        #Window.size = (sp(1200), sp(768))
        #Window.fullscreen = True
        Window.clearcolor = (0, 0, 0, 1)
       
        # Run time schortcut vars
        txtColor = (self.engineConfig.getThemeTextColor()["r"] , self.engineConfig.getThemeTextColor()["b"], self.engineConfig.getThemeTextColor()["g"], 1)

        #self.orientation='vertical'
        # self.cols = 2

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
        
        currentProjectMenuDropdown = DropDown()
        currentProjectMenuDropdown.dismiss()
        
        toolsAddBtn = Button(text='Add button',
                      color=(txtColor),
                      size_hint=(None, None),  height=30, width=200,
                      on_press=self.addNewButtonGUI)
        toolsAddText = Button(text='Add text',
                      color=(txtColor),
                      size_hint=(None, None),  height=30, width=200)
        currentProjectMenuDropdown.add_widget(toolsAddBtn)
        currentProjectMenuDropdown.add_widget(toolsAddText)

        self.editorMenuLayout.add_widget(currentProjectMenuDropdown)

        # Application Menu Drop menu
        self.appMenuDropdown = DropDown()
        self.appMenuDropdown.dismiss()

        btn = Button(text='Create new project',
                     color=(txtColor),
                     size_hint=(None, None), height=30, width=200)
        self.appMenuDropdown.add_widget(btn)

        loadBtn = Button(text='Load project',
                     color=(txtColor),
                     size_hint=(None, None), height=30, width=200)
        self.appMenuDropdown.add_widget(loadBtn)

        loadBtn.bind(on_press=self.CreateLoadInstanceGUIBox)

        self.editorMenuLayout.add_widget(self.appMenuDropdown)
 
        #btn.bind(on_release=lambda btn: appMenuDropdown.select(btn.text))
        btn.bind(on_press=self.CreateNewInstanceGUIBox)

        editorTools = Button(text='Tools', color=(txtColor), size_hint=(None, None), height=30, width=200)
        editorTools.bind(on_release=currentProjectMenuDropdown.open)
        self.editorMenuLayout.add_widget(editorTools)

        mainbutton = Button(markup=True , text='[b][color=ff3333]A[/color]pplication[/b]', color=(txtColor), size_hint=(None, None), height=30, width=200)
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
        # for item in self.store.find(name='renderComponentArray'):
        #    print('Looking data intro project files .... ', item)
        # print('..................................... ', self.store.get('renderComponentArray')['elements'] )
        operationAddTest = EditorOperationAdd(store=self.store, engineLayout=self.engineLayout)

    def showDetails(self, engineRoot):
        print("TEST DETAILS")
        ## TEST DETAILS
        self.editorElementDetails = FloatLayout()
        self.editorElementDetails.add_widget(
            Button(
                text="COOL",
                size_hint=(.4, 1),
                pos_hint={'x': 0.6, 'y':.0})
            )
        engineRoot.add_widget(self.editorElementDetails)
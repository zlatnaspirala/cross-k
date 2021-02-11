import kivy
from kivy.config import Config

print(kivy.__version__)
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.metrics import dp, sp, pt
from kivy.core.window import Window
from engine.editor.layout import EngineLayout
from engine.config import EngineConfig
from engine.common.modifycation import AlignedTextInput
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

    def createProjectFiles(self, instance):
        print("Good project name : ", self.projectName.text, " is created.")
        # input_filter from shutil import copyfile

        # copyfile("./engine/editor/layout.py", "./projects/test1.py")
        ###############################################################
        # Project files definition
        ###############################################################

        # Clear and remove 
        self.createNewProjectLayoutEditor.clear_widgets()
        self.remove_widget(self.createNewProjectLayoutEditor)
        self.engineLayout = EngineLayout(size=(1048, 768))
        self.add_widget(self.engineLayout)

        PROJECT_FOLDER_NAME = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../projects/' + self.projectName.text + "/")
        )

        if not os.path.exists(PROJECT_FOLDER_NAME):
            os.mkdir(PROJECT_FOLDER_NAME)

        # CROSSK_PROJECTS_PATH = App.user_data_dir
        store = JsonStore(PROJECT_FOLDER_NAME + '/' + self.projectName.text + '.json')

        # put some values , date=datetime.now()
        store.put('projectInfo', name=self.projectName.text, version='beta')
        store.put('defaultLayout', layoutType='boxLayout', orientation='horizontal')
        store.put('appInstanceRenderComponentArray', elements= ['horizontal'])
        # get a value using a index key and key
        # print('tito is', store.get('tito')['age'])

        # or guess the key/entry for a part of the key
        #for item in store.find(name='Gabriel'):
        #    print('tshirtmans index key is', item[0])
        #    print('his key value pairs are', str(item[1]))
            

    def CreateNewInstanceGUIBox(self, instance):
        print("CreateNewInstanceGUIBox ..." )
        #self.rows = 2  row_force_default=True, row_default_height=10

        self.createNewProjectLayoutEditor = GridLayout(padding= 0 , rows=5, row_force_default=True, row_default_height=50)
        self.add_widget(self.createNewProjectLayoutEditor)

        self.createNewProjectLayoutEditor.add_widget(Label(text='CROSS[b]K[/b]', markup=True, font_size="30sp" ))
        self.createNewProjectLayoutEditor.add_widget(Button(text='0.1.0', size=(60, 100), size_hint=(None, None) ))

        self.newProjectBtn = Button(text='Create new', size_hint=(.1, .2),
          on_press=self.createProjectFiles)

        self.newProjectTitle = Label(text='Project name:')
        self.createNewProjectLayoutEditor.add_widget(self.newProjectTitle)
        # self.projectName = TextInput(multiline=False, size_hint=(.1, .05) )
        self.projectName = self.get_input('middle', 'center')

        self.createNewProjectLayoutEditor.add_widget(self.projectName)
        self.createNewProjectLayoutEditor.add_widget(self.newProjectBtn)
        
    def __init__(self, **kwargs):
        super(EditorMain, self).__init__(**kwargs)

        ####################################################
        # Engine config , Colors Theme
        ####################################################
        self.engineConfig = EngineConfig()
        self.engineConfig.getVersion()
        #Window.size = (sp(1200), sp(768))
        #Window.fullscreen = True
        Window.clearcolor = (0, 0, 0.5, 1)
        # Run time schortcut vars
        txtColor = (self.engineConfig.getThemeTextColor()["r"] , self.engineConfig.getThemeTextColor()["b"], self.engineConfig.getThemeTextColor()["g"], 1)

        #self.orientation='vertical'

        self.cols = 1

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
                      size_hint=(None, None),  height=30, width=200)
        toolsAddText = Button(text='Add text',
                      color=(txtColor),
                      size_hint=(None, None),  height=30, width=200)
        currentProjectMenuDropdown.add_widget(toolsAddBtn)
        currentProjectMenuDropdown.add_widget(toolsAddText)

        self.editorMenuLayout.add_widget(currentProjectMenuDropdown)

        # Application Menu Drop menu
        appMenuDropdown = DropDown()
        appMenuDropdown.dismiss()

        btn = Button(text='Create new project',
                     color=(1, 0, 0.2, 1),
                     size_hint=(None, None), height=30, width=200)
        appMenuDropdown.add_widget(btn)

        self.editorMenuLayout.add_widget(appMenuDropdown)

        #btn.bind(on_release=lambda btn: appMenuDropdown.select(btn.text))
        btn.bind(on_press=self.CreateNewInstanceGUIBox)

        editorTools = Button(text='Tools',  size_hint=(None, None), height=30, width=200)
        editorTools.bind(on_release=currentProjectMenuDropdown.open)
        self.editorMenuLayout.add_widget(editorTools)

        mainbutton = Button(text='Application', size_hint=(None, None), height=30, width=200)
        mainbutton.bind(on_release=appMenuDropdown.open)
        self.editorMenuLayout.add_widget(mainbutton)
        
    def get_input(self, v, h):
        # Test stage for this
        return AlignedTextInput(text='Project1', halign=h, valign=v, height=100)

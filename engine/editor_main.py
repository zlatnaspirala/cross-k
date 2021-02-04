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

class EditorMain(BoxLayout):

    def createProjectFiles(self, instance):
        print("Good")
        # input_filter
        self.mylayout.clear_widgets()
        self.remove_widget(self.mylayout)
        self.add_widget(EngineLayout(size=(1048, 768)))

    def CreateNewInstance(self, instance):
        print("CreateNewInstance ..." )
        #self.rows = 2  row_force_default=True, row_default_height=10

        self.mylayout = GridLayout(padding= 0 , rows=5, row_force_default=True, row_default_height=50)
        self.add_widget(self.mylayout)

        self.mylayout.add_widget(Label(text='CROSS[b]K[/b]', markup=True, font_size="30sp" ))
        
        self.mylayout.add_widget(Button(text='0.1.0', size=(60, 100), size_hint=(None, None) ))


        self.newProjectBtn = Button(text='Create new', size_hint=(.1, .2),
          on_press=self.createProjectFiles)
        
        self.newProjectTitle = Label(text='Project name:')
         
        self.mylayout.add_widget(self.newProjectTitle)
        self.projectName = TextInput(multiline=False, size_hint=(.1, .1))
        self.mylayout.add_widget(self.projectName)

        self.mylayout.add_widget(self.newProjectBtn)
        
    def __init__(self, **kwargs):
        super(EditorMain, self).__init__(**kwargs)

        self.engineConfig = EngineConfig()
        self.engineConfig.getVersion()
        #Window.size = (sp(1200), sp(768))
        #Window.fullscreen = True
        Window.clearcolor = (1, 0, 0.5, 1)

        self.cols = 1

        dropdown = DropDown()
        dropdown.dismiss()

        btn = Button(text='Create new project',
                     color=(1, 0, 0.2, 1),
                     size_hint=(None, None), height=30, width=200)
        dropdown.add_widget(btn)
        self.add_widget(dropdown)

        #btn.bind(on_release=lambda btn: dropdown.select(btn.text))
        btn.bind(on_press=self.CreateNewInstance)
        
        mainbutton = Button(text='Application', size_hint=(None, None), height=30, width=200)

        mainbutton.bind(on_release=dropdown.open)
        self.add_widget(mainbutton)
        



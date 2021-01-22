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

class CreateProject(BoxLayout):

    def createProjectFiles(self, instance):
        print("Good")
        self.mylayout.clear_widgets()
        self.remove_widget(self.mylayout)

    def CreateNewInstance(self, instance):
        print("CreateNewInstance   BLAB BLAB" )
        #self.rows = 2

        self.mylayout = GridLayout(padding= 50, cols=3, row_force_default=True, row_default_height=40)
        self.add_widget(self.mylayout)

        self.newProjectBtn = Button(text='Create', size_hint=(.5, 0.5), height=30, width=200,
          on_press=self.createProjectFiles)
        self.mylayout.add_widget(self.newProjectBtn)
        self.newProjectTitle = Label(text='Project name:', height=30, width=200)
        self.mylayout.add_widget(self.newProjectTitle)
        self.projectName = TextInput(multiline=False, height=30, width=200)
        self.mylayout.add_widget(self.projectName)
        
    def __init__(self, **kwargs):
        super(CreateProject, self).__init__(**kwargs)
        Window.size = (sp(1200), sp(768))
        Window.fullscreen = True
        self.cols = 1

        dropdown = DropDown()
        dropdown.dismiss()

        # When adding widgets, we need to specify the height manually
        # (disabling the size_hint_y) so the dropdown can calculate
        # the area it needs.
        btn = Button(text='Create new project', size_hint=(None, None), height=30, width=200)
        dropdown.add_widget(btn)
        self.add_widget(dropdown)

        # for each button, attach a callback that will call the select() method
        # on the dropdown. We'll pass the text of the button as the data of the
        # selection.
        #btn.bind(on_release=lambda btn: dropdown.select(btn.text))
        btn.bind(on_press=self.CreateNewInstance)
        
        
        # then add the button inside the dropdown
        


        mainbutton = Button(text='Application', size_hint=(None, None), height=30, width=200)

        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open.).
        mainbutton.bind(on_release=dropdown.open)
        self.add_widget(mainbutton)
        



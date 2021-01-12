import kivy

print(kivy.__version__)

kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

class CreateProject(GridLayout):

    def CreateNewInstance(self, instance):
        print("CreateNewInstance")
        
    def __init__(self, **kwargs):
        super(CreateProject, self).__init__(**kwargs)

        dropdown = DropDown()
    
        # When adding widgets, we need to specify the height manually
        # (disabling the size_hint_y) so the dropdown can calculate
        # the area it needs.

        btn = Button(text='Value', size_hint_y=None, height=44)

        # for each button, attach a callback that will call the select() method
        # on the dropdown. We'll pass the text of the button as the data of the
        # selection.
        btn.bind(on_release=lambda btn: dropdown.select(btn.text))
        
        # then add the button inside the dropdown
        dropdown.add_widget(btn)


        mainbutton = Button(text='Hello', size_hint=(None, None))

        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open.).
        mainbutton.bind(on_release=dropdown.open)
        self.add_widget(mainbutton)

        self.add_widget(dropdown)

        self.cols = 1
        self.add_widget(Label(text='Project name:'))
        self.projectName = TextInput(multiline=False)
        self.add_widget(self.projectName)

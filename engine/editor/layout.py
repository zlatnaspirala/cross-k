from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class LoginScreen(GridLayout):

    def action_engine_create_project(self, instance):
        print("create project")

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        self.cols = 1
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        self.button = Button(size_hint=(None, None), text='plop', on_press=self.action_engine_create_project)
        self.add_widget(self.button)

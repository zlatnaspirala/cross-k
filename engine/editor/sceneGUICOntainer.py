from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty

class SceneGUIContainer(BoxLayout):

    currentProjectPath = StringProperty('null')
    currentProjectName = StringProperty('null')

    def __init__(self, **kwargs):
        super(SceneGUIContainer, self).__init__()
        self.storePath = kwargs.get("storePath", "null")
        self.myStore = JsonStore(self.storePath)
        print("Testing myStore: ", self.myStore )

        loadElements = self.myStore.get('renderComponentArray')['elements']
        for item in loadElements:
            print("......", item['type'])
            if item['type'] == 'BUTTON1':
                print('its button , coming from root editor layout , list in root also in sceneGUIContainer.->>>')

                self.add_widget( Button(
                    text=item['text'],
                    color=item['color'],
                    size_hint=(None, None),
                    height=item['height'],
                    width=item['width'])
                )
        ######################################################
        # Test loader 
 
        # CROSSK_PROJECTS_PATH = App.user_data_dir
        #store = JsonStore('projects/Project1/Project1.json')

        #for item in store.find(name='renderComponentArray'):
        #    print('tshirtmans index key is', item[0])
        #    print('his key value pairs are', str(item[1]))

        ######################################################

        #self.appRenderElementsArray = [Label(text='TEXT COMPONENT', size_hint=(.5, .1), color=(1,0,1,1) )]

        #for i in range(len(self.appRenderElementsArray)):
        #    self.add_widget(self.appRenderElementsArray[i])

        # self.engineTitle = 

        # self.add_widget(self.engineTitle)
         
        #self.button = Button(text='plop', pos=(1,1),size_hint=(.5, .1), on_press=self.action_engine_create_project)
        #self.add_widget(self.button)

        #with self.canvas.before:
        #    Color(0.3, 0.1, 0.6, 1)
        #    self.rect = Rectangle(size=self.size, pos=self.pos)

        #self.bind(size=self._update_rect, pos=self._update_rect)


    # Update render elements 
    def updateScene(self):
        self.clear_widgets()

    # Definition for update call bg
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

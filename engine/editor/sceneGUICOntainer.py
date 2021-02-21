from kivy.app import App
from functools import partial
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
# pylint: disable=no-name-in-module
from kivy.properties import StringProperty, ObjectProperty 

class SceneGUIContainer(ScrollView):

    currentProjectPath = StringProperty('null')
    currentProjectName = StringProperty('null')

    def selfUpdate(self):

        self.clear_widgets()

        self.myStore = JsonStore(self.storePath)
        print("Testing myStore: ", self.myStore)

        # call theme, improve aplha arg
 
        self.sceneScroller = BoxLayout(size_hint=(1, None) , height=300)
        

        self.sceneScroller.cols = 1
        self.sceneScroller.size_hint_y= None
        self.sceneScroller.spacing = 10
        self.sceneScroller.orientation = 'vertical'
        # Title box label
        # print(self.engineRoot.engineConfig.getThemeBgSceneBoxColor() , "<<<<<<<<<<<")
        self.sceneScroller.add_widget( Button(
                    markup=True,
                    text='[Scene-Root]',
                    color=self.engineRoot.engineConfig.getThemeTextColor(),
                    size_hint=(1, None),
                    background_normal= '',
                    background_color=(self.engineRoot.engineConfig.getThemeBackgroundColor()),
                    height=35
                    )
                )

 
        self.add_widget(self.sceneScroller)
        loadElements = self.myStore.get('renderComponentArray')['elements']
        for item in loadElements:
            print("......", item['type'])
            if item['type'] == 'BUTTON':
                # print('its button , coming from root editor layout , list in root also in sceneGUIContainer.->>>')
                # pass it
                self.sceneScroller.add_widget(Button(
                    markup=True,
                    text='[Button] [b]' + item['name'] + '[b]',
                    color=self.engineRoot.engineConfig.getThemeTextColor(),
                    background_normal= '',
                    background_color=(self.engineRoot.engineConfig.getThemeBgSceneBtnColor()),
                    # on_press=lambda *args: self.engineRoot.showDetails(nameLoc, idLoc, *args),  # self.engineRoot.showDetails(item),
                    on_press=partial(self.engineRoot.showDetails, item),
                    size_hint=(1, None),
                    height=30
                ))

        self.sceneScroller.add_widget( Button(
            markup=True,
            text='[Scene space]',
            color=self.engineRoot.engineConfig.getThemeTextColor(),
            size_hint=(1, 1)
            )
        )
    
    def __init__(self, **kwargs):
        super(SceneGUIContainer, self).__init__()

        self.storePath = kwargs.get("storePath", "null")
        self.engineRoot = kwargs.get("engineRoot")

        # Reset
        self.orientation = 'horizontal'
        self.cols = 1

        self.size_hint = (1,1)
        self.pos_hint = {'center_x':0.5,'top': 1}

        self.selfUpdate()
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

    # Definition for update call bg
    #def _update_rect(self, instance, value):
    #    self.rect.pos = instance.pos
    #    self.rect.size = instance.size

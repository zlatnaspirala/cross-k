from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty
# from kivy.cache.cache import Cache

class ResourcesGUIContainer(ScrollView):
    currentProjectPath = StringProperty('null')
    currentProjectName = StringProperty('null')
    def __init__(self, **kwargs):
        super(ResourcesGUIContainer, self).__init__()

        self.assetsPath = kwargs.get("assetsPath", "null")
        self.engineRoot = kwargs.get("engineRoot")

        # Reset
        self.orientation = 'horizontal'
        self.cols = 1
        self.size_hint = (1,1)
        self.pos_hint = {'center_x':0.5,'top': 1}

        self.selfUpdate()

    def access(self):
        print("ATTACH")

    def _update(self, loadElements, container, parentName):

        for _index, item in enumerate(loadElements):
            print("update _index ", _index)
            test = Button(
                markup=True,
                halign="left", valign="middle",
                padding_x= self.deepTest * 10,
                font_size=15,
                text='[b] RESOURCE NAME' + item['name'] + '[/b][i]['+ str(_index) + '][/i] [u]Asset[/u]',
                color=self.engineRoot.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineRoot.engineConfig.getThemeBgSceneBtnColor()),
                on_press=partial(self.engineRoot.showCommonDetails, item),
                size_hint=(1, None),
                height=30
            )
            container.add_widget(test)
            test.bind(size=test.setter('text_size'))

            if (_index==len(loadElements)-1):
                self.deepTest=0

    def selfUpdate(self):

        self.clear_widgets()
        self.assetsPath = JsonStore(self.assetsPath)

        # call theme, improve aplha arg
        self.sceneScroller = GridLayout(
            orientation='lr-tb',
            size_hint=(1, None),
            height=600
        )

        self.sceneScroller.cols = 1
        self.sceneScroller.size_hint_y= None
        self.sceneScroller.spacing = 1

        self.sceneScroller.add_widget( Button(
                    markup=True,
                    text='[Assets-Root]',
                    color=self.engineRoot.engineConfig.getThemeTextColor(),
                    size_hint=(1, None),
                    background_normal= '',
                    background_color=(self.engineRoot.engineConfig.getThemeBackgroundColor()),
                    height=35
                    )
                )

        self.add_widget(self.sceneScroller)
        loadElements = self.assetsPath.get('assetsComponentArray')['elements']

        self._update( loadElements, self.sceneScroller, 'rootScene')

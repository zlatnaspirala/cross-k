
from functools import partial
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

#######################################
# JSON Nidza Layout Class
# alias JSONN
# Created 4/3/2021
# GPL v3
#######################################

class JsonN(ScrollView):
    currentProjectPath = StringProperty('null')
    currentProjectName = StringProperty('null')
    def __init__(self, **kwargs):
        super(JsonN, self).__init__()

        # props assetsPath
        # inject path
        self.assetsPath = kwargs.get("assetsPath", "null")
        self.currentContainer = kwargs.get("currentContainer")
        self.engineRoot = kwargs.get("engineRoot")

        # Reset
        self.orientation = 'horizontal'
        self.cols = 1
        self.size_hint = (1,1)
        self.pos_hint = {'center_x':0.5,'top': 1}

        self.selfUpdate()

        self.currentContainer.add_widget(self)

    def access(self):
        print("ATTACH")

    def _update(self, loadElements, container, parentName):

        for _index, item in enumerate(loadElements):
            localBox = BoxLayout(size_hint=(1, None), height=30)
            test = Button(
                markup=True,
                halign="left", valign="middle",
                padding_x= 10,
                font_size=15,
                text='[b]' + item['name'] + '[/b][u][i] Image[/i][/u]',
                color=self.engineRoot.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineRoot.engineConfig.getThemeBgSceneBtnColor()),
                on_press=partial(self.engineRoot.showCurrentAssetsEditor, item),
                size_hint=(1, None),
                height=30
            )
            localBox.add_widget(test)

            deleteAssetBtn = Button(
                markup=True,
                halign="left", valign="middle",
                padding_x= 10,
                font_size=15,
                text='[b]Delete[/b]',
                color=(self.engineRoot.engineConfig.getThemeCustomColor("alert")),
                background_normal= '',
                background_color=(self.engineRoot.engineConfig.getThemeCustomColor('background')),
                on_press=partial(self.engineRoot.showCurrentAssetsEditor, item),
                size_hint=(0.2, None),
                height=30
            )
            localBox.add_widget(deleteAssetBtn)

            container.add_widget(localBox)
            test.bind(size=test.setter('text_size'))

            if (_index==len(loadElements)-1):
                self.deepTest=0

    def selfUpdate(self):

        self.clear_widgets()
        self.assetsStore = JsonStore(self.assetsPath)

        # call theme, improve aplha arg
        self.sceneScroller = GridLayout(
            orientation='lr-tb',
            size_hint=(1, None),
            height=400
        )

        self.sceneScroller.cols = 1
        self.sceneScroller.size_hint_y= None
        self.sceneScroller.spacing = 1

        self.sceneScroller.add_widget( Button(
                    markup=True,
                    text='[b]JSONN Explorer[/b]',
                    color=self.engineRoot.engineConfig.getThemeTextColor(),
                    size_hint=(1, None),
                    background_normal= '',
                    background_color=(self.engineRoot.engineConfig.getThemeBackgroundColor()),
                    height=35
                    )
                )

        for _n_ in self.assetsStore.find():
            print('nidza explore:', _n_)
            for _nsub_ in _n_:
                print('nidza sub explore:', _n_)


        self.add_widget(self.sceneScroller)

        # loadElements = self.assetsStore.get('assetsComponentArray')['elements']

        # self._update( loadElements, self.sceneScroller, 'rootScene')

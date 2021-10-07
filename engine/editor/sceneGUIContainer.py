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

    def checkDeepNidza(self, loadElements, sumOfElements):
        for _index, item in enumerate(loadElements):
            self.local += 1
            if item['type'] == 'LAYOUT':
                self.checkDeepNidza(item['elements'], self.local)
        return self.local

    def _update(self, loadElements, container, parentName):

        if parentName == "rootScene":
            parentName = ""
        else:
            parentName = "[" + parentName + "]"

        for _index, item in enumerate(loadElements):
            # print("update _index ", _index)
            if item['type'] == 'BUTTON':
                test = Button(
                    markup=True,
                    halign="left", valign="middle",
                    padding_x= self.deepTest * 10,
                    font_size=15,
                    text='[b]' + item['name'] + '[/b][i]['+ str(_index) + '][/i] [u]Button[/u]',
                    color=self.engineRoot.engineConfig.getThemeTextColor(),
                    background_normal= '',
                    background_color=(self.engineRoot.engineConfig.getThemeBgSceneBtnColor()),
                    on_press=partial(self.engineRoot.showCommonDetails, item),
                    size_hint=(1, None),
                    height=30
                )
                container.add_widget(test)
                test.bind(size=test.setter('text_size'))

            if item['type'] == 'LABEL':
                test = Button(
                    markup=True,
                    halign="left", valign="middle",
                    padding_x= self.deepTest * 10,
                    font_size=15,
                    text='[b]' + item['name'] + '[/b][i]['+ str(_index) + '][/i] [u]Label[/u]',
                    color=self.engineRoot.engineConfig.getThemeTextColor(),
                    background_normal= '',
                    background_color=(self.engineRoot.engineConfig.getThemeCustomColor('sceneGUIbgLabel')),
                    on_press=partial(self.engineRoot.showCommonDetails, item),
                    size_hint=(1, None),
                    height=30
                    )

                test.bind(size=test.setter('text_size'))
                container.add_widget(test)

            if item['type'] == 'LAYOUT':
                #self.localGrid = GridLayout(
                #    cols=1,
                #    size_hint=(1, 1) ,
                #    height=30 * (len(item['elements']) + 1) + self.checkDeepNidza(item['elements'], 0) * 30 + 30)
                localTest = Button(
                    markup=True,
                    halign="left", valign="middle",
                    padding_x= self.deepTest * 10,
                    font_size=15,
                    text='[b]' + item['name'] + '[/b][i]['+ str(_index) + '][/i] [u]' + item['layoutType'] + '[/u]',
                    color=self.engineRoot.engineConfig.getThemeTextColor(),
                    background_normal= '',
                    background_color=(self.engineRoot.engineConfig.getThemeBgSceneBoxColor()),
                    on_press=partial(self.engineRoot.showCommonLayoutDetails, item),
                    size_hint=(1, None),
                    height=30
                )
                localTest.bind(size=localTest.setter('text_size'))
                #self.localGrid.add_widget(localTest)

                container.add_widget( localTest )
                if len(item['elements']) > 0:
                    self.deepTest=self.deepTest+1
                    self._update(  item['elements'] , container, item['name'])

            if item['type'] == 'PICTURE_CLICKABLE':
                test = Button(
                    markup=True,
                    halign="left", valign="middle",
                    padding_x= self.deepTest * 10,
                    font_size=15,
                    text='[b]' + item['name'] + '[/b][i]['+ str(_index) + '][/i] [u]Picture[/u]',
                    color=self.engineRoot.engineConfig.getThemeTextColor(),
                    background_normal= item['image'],
                    background_color=(self.engineRoot.engineConfig.getThemeBgSceneBtnColor()),
                    on_press=partial(self.engineRoot.showCommonDetails, item),
                    size_hint=(1, None),
                    height=30
                )
                container.add_widget(test)
                test.bind(size=test.setter('text_size'))


            if (_index==len(loadElements)-1):
                self.deepTest=0

    def getAbsoluteSUmElements(self, elements):
        return self.checkDeepNidza(elements, len(elements) )

    def selfUpdate(self):

        self.clear_widgets()
        self.myStore = JsonStore(self.storePath)
        loadElements = self.myStore.get('renderComponentArray')['elements']

        self.local = 0
        determinateNumberOfElements = self.getAbsoluteSUmElements(loadElements)

        # call theme, improve aplha arg
        self.sceneScroller = GridLayout(
            orientation='lr-tb',
            size_hint=(1, None),
            height=(determinateNumberOfElements + 3 )* 30
        )

        self.sceneScroller.cols = 1
        self.sceneScroller.size_hint_y= None
        self.sceneScroller.spacing = 1

        self.sceneScroller.add_widget( Button(
                    markup=True,
                    text='[Scene-Root]',
                    color=self.engineRoot.engineConfig.getThemeBgSceneBoxColor(),
                    size_hint=(1, None),
                    background_normal= '',
                    background_color=(self.engineRoot.engineConfig.getThemeTextColor()),
                    height=35
                    )
                )

        self.add_widget(self.sceneScroller)
        self._update( loadElements, self.sceneScroller, 'rootScene')

    def __init__(self, **kwargs):
        super(SceneGUIContainer, self).__init__()

        self.storePath = kwargs.get("storePath", "null")
        self.engineRoot = kwargs.get("engineRoot")

        self.local = 0

        self.deepTest = 0

        # Reset
        self.orientation = 'horizontal'
        self.cols = 1

        self.size_hint = (1,1)
        self.pos_hint = {'center_x':0.5,'top': 1}

        self.selfUpdate()

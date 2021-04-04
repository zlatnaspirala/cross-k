
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
from kivy.uix.image import Image, AsyncImage
from engine.common.commons import PictureAPath
# from kivy.cache.cache import Cache

class ResourcesGUIContainer(ScrollView):
    currentProjectPath = StringProperty('null')
    currentProjectName = StringProperty('null')
    def __init__(self, **kwargs):
        super(ResourcesGUIContainer, self).__init__()

        self.assetsPath = kwargs.get("assetsPath", "null")
        self.engineRoot = kwargs.get("engineRoot")

        # Reset
        self.size_hint = (1,1)
        self.pos_hint = {'center_x':0.5,'top': 1}

        self.selfUpdate()

    def access(self):
        print("ATTACH")

    def _update(self, loadElements, container, parentName):

        for _index, item in enumerate(loadElements):
            localBox = BoxLayout(size_hint=(1, None), height=99, orientation='horizontal')
            test = Button(
                markup=True,
                halign="left", valign="middle",
                padding_x= 10,
                font_size=15,
                text='[b]' + item['name'] + '[/b][u][i]' + item['type'] + '[/i][/u]',
                color=self.engineRoot.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineRoot.engineConfig.getThemeBgSceneBtnColor()),
                on_press=partial(self.engineRoot.showCurrentAssetsEditor, item),
                size_hint=(0.55, None),
                height=99
            )
            localBox.add_widget(test)

            # test__ = PictureAPath(injectWidget=localBox, source=item['path'])
            if item['type'] == 'ImageResource':
                picture1 = Button(background_normal=item['path'], size_hint=(0.3, None), height=99)
            elif item['type'] == 'FontResource':
                picture1 = Button(font_name=item['path'], text='Font', font_size=28, size_hint=(0.3, None), height=99)

            with picture1.canvas.before:
                Color(0.3,0.3,0.4,1)
                picture1.rect = Rectangle(size=picture1.size,
                                                    pos=picture1.pos)
            def update_rect(instance, value):
                instance.rect.pos = instance.pos
                instance.rect.size = instance.size

            localBox.add_widget(picture1)
            picture1.bind(pos=update_rect, size=update_rect)
            container.add_widget(localBox)

            test.bind(size=test.setter('text_size'))

            if (_index==len(loadElements)-1):
                self.deepTest=0

    def selfUpdate(self):

        self.clear_widgets()
        self.assetsStore = JsonStore('projects/' + self.engineRoot.engineConfig.currentProjectName + '/data/assets.json')
        loadElements = self.assetsStore.get('assetsComponentArray')['elements']

        # call theme, improve aplha arg
        self.sceneScroller = BoxLayout(
            # cols=2,
            orientation='vertical',
            size_hint=(1, None),
            height=len(loadElements) * 99 + 35
        )

        # self.sceneScroller.cols = 2
        self.sceneScroller.size_hint_y= None
        self.sceneScroller.spacing = 0

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

        self._update( loadElements, self.sceneScroller, 'rootScene')

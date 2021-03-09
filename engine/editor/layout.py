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
# from engine.editor.events import EngineLayoutEvents

class EngineLayout(BoxLayout):
    # This is root app class container. I need to pass all needed staff
    # from main-editor or make copy of main-editor and remove unused code.
    # Must be done before package feature
    # currentProjectPath = StringProperty('null')
    # currentProjectName = StringProperty('null')

    def getSceneSize(self):
        return len(self.children)

    def getAppSceneElements(self):
        return self.children

    def getSceneElementByIndex(self, index):
        return self.children[index]

    def deepSearch(self, currContainer, index):
        print("test currContainer.children ", currContainer.children)
        res =  currContainer.children[::-1]
        return res[index]

    def getElementByIndexArray(self, crossKAccess):
        testContainer = 0
        deepSize = len(crossKAccess)
        print("deep is", len(crossKAccess))

        if deepSize == 1:
            return self
            
        for index, item in enumerate(crossKAccess):
            print("index", index)
            if (index == 0):
                testContainer = self.deepSearch(self, item)
            else:
                # check if l;ast last
                #  two ways !!!
                if len(crossKAccess) - 1 == index:
                    print("[last]", testContainer)
                    res =  testContainer.children[::-1]
                    return res[item]
                else:
                    print("test next deep Container", testContainer)
                    testContainer = self.deepSearch(testContainer.children[item], item)

    def __init__(self, **kwargs):
        super(EngineLayout, self).__init__(**kwargs)
        # print("Testing layout size: ", self.size)
        # print("Testing layout pos: ", self.pos)

        # self.appEvents = EngineLayoutEvents()
        with self.canvas.before:
            Color(0.3, 0.1, 0.6, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    # Definition for update call bg
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def attachEvent(self, arg1, liveInstance):
        print("ATTACH EVENT", arg1, liveInstance)
        # liveInstance.text = 'blabla'
        print( self.getElementByIndexArray([1,0]).text , "  Look at 0 1 ")
        exec(arg1)

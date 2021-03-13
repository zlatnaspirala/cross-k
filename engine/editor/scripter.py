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
from engine.editor.networking import Networking
from functools import partial

class EventsEngineLayout(FloatLayout):

    def mypos(self, ins, touch2):
        print('test mypos ', touch2)
    

    def on_touch_down(self, touch2, test):
        print('test on_touch_down ', touch2.pos)
        return super(EventsEngineLayout, self).on_touch_down(touch2)

    def mypos2(self, ins, touch2):
        print('test the best')
        #if self.collide_point(*touch2.pos):
        #    if touch2.button == 'left':
        #        print('Scripter touchDown pos: ', touch2.pos)
                # Hold value of touch downed pos
        #        self.last_touch = touch2.pos # Need this line

        # return super(EventsEngineLayout, self).on_touch_down(touch2)
        
    def __init__(self, **kwargs):
        super(EventsEngineLayout, self).__init__()
        self.engineRoot = kwargs.get("engineRoot")

        self.net = Networking()
        # self.net.getJson()

        
        print("EventsEngineLayout loaded -> ")

        self.add_widget(
            Button(
                border=(3,3,3,3),
                pos_hint={'x': 0, 'y': 0.95},
                markup=True,
                text="[b]Save[/b]",
                font_size=18,
                size_hint=(0.5,0.05),
                color=self.engineRoot.engineConfig.getThemeTextColor(),
                # color=(1,1,1,0.1),
                # background_normal='engine/assets/nidzaBorder002.png',
                # background_down='engine/assets/nidzaBorder001-250x250_yellow_black_Over.png',
                background_color=(self.engineRoot.engineConfig.getThemeCustomColor('engineBtnsBackground'))
                # background_color=(1,1,1,0.8),
                # on_release=partial(self.saveDetails, str(detailData['id']), str(detailData['type']) ))
            ))

        self.add_widget(
            Button(
                pos_hint={'x': 0.5, 'y': 0.95},
                border=(10,10,10,10),
                markup=True,
                font_size=18,
                text="[b]Cancel[/b]",
                size_hint=(0.5,0.05),
                #background_normal='engine/assets/nidzaBorder001-250x250_yellow_black.png',
                #background_down='engine/assets/nidzaBorder001-250x250_yellow_black_Over.png',
                background_color=(self.engineRoot.engineConfig.getThemeCustomColor('engineBtnsBackground'))
                #background_color=(0.1,0.1,0,0.5),
                # on_release=self.closeWithNoSaveDetails
            ))


        # self.appEvents = EngineLayoutEvents()
        with self.canvas.before:
            Color(0.6, 0.2, 0.6, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(on_touch_down=self.on_touch_down)
        self.bind(pos=self.mypos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    # Definition for update call bg
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        

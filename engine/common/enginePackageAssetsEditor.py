import os
import io
import threading
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from engine.common.commons import Picture

import string

class AssetsEditorPopup():

    def __init__(self, **kwargs):
        self.engineConfig = kwargs.get("engineConfig")
        self.isFreeRigthBox = True
        self.box = BoxLayout(orientation="horizontal")
        self.leftBox = BoxLayout(orientation="vertical")
        self.rightBox = BoxLayout(orientation="vertical")

        # Strong check needed
        drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]

        self.browser = FileChooserListView(# select_string='Select', dirselect: True
              # path='projects/' + self.engineConfig.currentProjectName + '/data/',
              path= drives[1] + '/',
              size_hint=(1,3)
           )
        self.rightBox.add_widget(self.browser)
        self.rightBox.add_widget(Label(text='Application assets pack path'))
        self.selectedPathLabel = Label(text='...')
        self.rightBox.add_widget(self.selectedPathLabel)

        self.rightBox.add_widget( Button(text='Add selected image',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(1, None),  height=30,
                      background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground'))
                      #on_press=self.packageWinApp
                      ) )

        self.leftBox.add_widget(Label(text='Application assets package operation.'))
        self.cancelBtn = Button(text='Cancel',
                                color=(self.engineConfig.getThemeTextColor()),
                                size_hint=(1, None),  height=70,
                                background_normal= '',
                                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')))

        # Picture(injectWidget=box, accessAssets="logo")
        self.box.add_widget(self.leftBox)

        # self.engineConfig.currentProjectName
        # self.engineConfig.currentProjectPath

        self.addImageRes = Button(markup=True, text='[b]Add ImageResource[b]',
                                color=(self.engineConfig.getThemeTextColor()),
                                size_hint=(1, None),  height=80,
                                background_normal= '',
                                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')))

        self.leftBox.add_widget(self.addImageRes)
        self.leftBox.add_widget(self.cancelBtn)
        # self.box.add_widget(self.infoBtn)

        _local = 'CrossK ' + self.engineConfig.getVersion() + ' Assets Editor'
        popup = Popup(title=_local , content=self.box, auto_dismiss=False)

        self.cancelBtn.bind(on_press=popup.dismiss)
        self.addImageRes.bind(on_press=lambda a:self.showImageAssetGUI())

        popup.open()

    def showImageAssetGUI(self):
        if self.isFreeRigthBox == True:
            self.box.add_widget(self.rightBox)
            self.isFreeRigthBox = False

    def addImageAssetPack(self):

        CURRENT_ASSETPACK_PATH = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../../projects/' + self.engineConfig.currentProjectName + "/data/")
        )
        if not os.path.exists(CURRENT_ASSETPACK_PATH):
            print("MAKE ASSETS PACK DIR")
            os.mkdir(CURRENT_ASSETPACK_PATH)
        else:
            print("PACK DIR EXIST...")
        print("Assets pack read meta data.")



 
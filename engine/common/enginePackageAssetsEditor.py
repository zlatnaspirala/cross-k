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

class AssetsEditorPopup():

    def __init__(self, **kwargs):
        self.engineConfig = kwargs.get("engineConfig")

        self.box = BoxLayout(orientation="horizontal")

        self.rightBox = BoxLayout(orientation="vertical")

        self.browser = FileChooserListView(# select_string='Select', dirselect: True
              path='projects/' + self.engineConfig.currentProjectName + '/data/',
              size_hint=(1,3)
           )
        self.rightBox.add_widget(self.browser)

        self.rightBox.add_widget( Button(text='Add selected image',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(1, None),  height=30, width=300,
                      background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground'))
                      #on_press=self.packageWinApp
                      ) )

        self.infoBtn = Button(text='Cancel')
        # Picture(injectWidget=box, accessAssets="logo")
        self.box.add_widget(Label(text='Application assets package operation.'))

        # self.engineConfig.currentProjectName
        # self.engineConfig.currentProjectPath

        self.addImageRes = Button(markup=True, text='[b]Add ImageResource[b]')

        self.box.add_widget(self.addImageRes)
        self.box.add_widget(self.infoBtn)

        _local = 'CrossK ' + self.engineConfig.getVersion() + ' Assets Editor'
        popup = Popup(title=_local , content=self.box, auto_dismiss=False)

        self.infoBtn.bind(on_press=popup.dismiss)
        self.addImageRes.bind(on_press=lambda a:self.showImageAssetGUI())

        popup.open()

    def showImageAssetGUI(self):
        self.box.add_widget(self.rightBox)


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



 
import os
import io
import threading
import string
from shutil import copyfile
from functools import partial
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image, AsyncImage
from kivy.graphics import Color, Rectangle
from kivy.storage.jsonstore import JsonStore
from engine.common.commons import PictureAPath

class AssetsEditorPopupAdd():

    def __init__(self, **kwargs):

        self.engineConfig = kwargs.get("engineConfig")
        self.currentAsset = kwargs.get("currentAsset")

        # self.currentAsset is flag for editor Assets Details fomrs
        # if self.currentAsset == None:  -> it is strick add procedure
        if self.currentAsset != None:
            print('current asset need load')

        self.isFreeRigthBox = True

        self.box = BoxLayout(orientation="horizontal")
        self.leftBox = BoxLayout(orientation="vertical")
        self.imageResourceGUIBox = BoxLayout(orientation="vertical")

        drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]

        self.drivesChooseBox = BoxLayout(size_hint=(1, None),  height=40,)
        for item in drives:
            self.drivesChooseBox.add_widget(Button(
                text=item + '/',
                on_press=partial(self.setFileBrowserPath),
                        color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(1, None),  height=65,
                      background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground'))
            ))
            print(" drive: ", item)

        self.imageResourceGUIBox.add_widget(self.drivesChooseBox)

        self.fileBrowser = FileChooserListView(# select_string='Select', dirselect: True
              # path='projects/' + self.engineConfig.currentProjectName + '/data/',
              filters=['*.png', '*.jpg'],
              path= drives[1] + '/',
              size_hint=(1,3),
              dirselect= True,
              on_submit=self.load_from_filechooser
           )
        self.imageResourceGUIBox.add_widget(self.fileBrowser)
        self.fileBrowser.bind(selection=partial(self.load_from_filechooser))

        self.imageResourceGUIBox.add_widget(Label(text='Application assets pack path'))
        self.selectedPathLabel = Label(text='...')
        self.imageResourceGUIBox.add_widget(self.selectedPathLabel)

        self.assetName = TextInput( text='MyAssets1',
                                    size_hint=(1, None),  height=65)
        with self.assetName.canvas.before:
            Color(self.engineConfig.getThemeCustomColor('engineBtnsBackground'))
            self.assetName.rect = Rectangle(size=self.assetName.size,
            pos=self.assetName.pos)
            # self.engineConfig.getThemeTextColor()
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        self.imageResourceGUIBox.add_widget(self.assetName)

        self.imageResourceGUIBox.add_widget( Button(text='Add selected image',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(1, None),  height=65,
                      background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                      on_press=partial(self.createImageAssets))
            )

        self.leftBox.add_widget(Label(text='Application assets package operation.'))
        self.cancelBtn = Button(text='Cancel',
                                color=(self.engineConfig.getThemeTextColor()),
                                size_hint=(1, None),  height=70,
                                background_normal= '',
                                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')))

        self.previewBox = BoxLayout(size_hint=(1,None), height=250)
        self.previewPicture = AsyncImage(source="", size_hint=(1, 1))
        self.previewBox.add_widget(Label(text='Preview Box'))
        self.previewBox.add_widget(self.previewPicture)

        self.imageResourceGUIBox.add_widget(self.previewBox)

        self.box.add_widget(self.leftBox)

        # Add button  - ImageResource
        self.addImageRes = Button(markup=True, text='[b]Add Image Resource[b]',
                                color=(self.engineConfig.getThemeTextColor()),
                                size_hint=(1, None),  height=80,
                                background_normal= '',
                                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')))

        self.leftBox.add_widget(self.addImageRes)

        # Others  - Fonts
        self.addFontRes = Button(markup=True, text='[b]Add Font Resource[b]',
                                color=(self.engineConfig.getThemeTextColor()),
                                size_hint=(1, None),  height=80,
                                background_normal= '',
                                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')))

        self.leftBox.add_widget(self.addFontRes)

        self.leftBox.add_widget(self.cancelBtn)
        # self.box.add_widget(self.infoBtn)

        _local = 'CrossK ' + self.engineConfig.getVersion() + ' Assets Editor'
        self.popup = Popup(title=_local , content=self.box, auto_dismiss=False)

        self.cancelBtn.bind(on_press=self.popup.dismiss)
        self.addImageRes.bind(on_press=lambda a:self.showImageAssetGUI())

        self.popup.open()

    def showImageAssetGUI(self):
        if self.isFreeRigthBox == True:
            self.box.add_widget(self.imageResourceGUIBox)
            self.isFreeRigthBox = False

    def resolvePathFolder(self):
        ASSETPACK_PATH = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../../projects/' + self.engineConfig.currentProjectName + "/data/")
        )
        if not os.path.exists(ASSETPACK_PATH):
            print("MAKE_ASSETPACK_PATH")
            os.mkdir(ASSETPACK_PATH)
        else:
            print('ASSETPACK_EXIST')

    def resolveAssetPathFolder(self):

        CURRENT_ASSETPACK_PATH = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../../projects/' + self.engineConfig.currentProjectName + "/data/" + self.assetName.text)
        )

        collectExt = ''
        print("Create Image Resource ->")
        local = self.fileBrowser.selection[0][::-1]
        for item in local:
            if item == '.':
                print("Create Image Resource -> Break EXT = ", collectExt)
                break
            else:
                collectExt += item;
        collectExt = collectExt[::-1]
        print(collectExt)


        if not os.path.exists(CURRENT_ASSETPACK_PATH):
            print("MAKE ASSETS PACK DIR")
            os.mkdir(CURRENT_ASSETPACK_PATH)
        else:
            if self.currentAsset == None:
                print('current asset need load')
                print("SOMETHIND WRONG - ASSETS ALREADY EXIST")
                return None

        print("Assets pack write meta data.")

        copyfile(self.fileBrowser.selection[0], CURRENT_ASSETPACK_PATH + '/' + str(self.assetName.text) + '.' + collectExt)
        self.assetsStore = JsonStore(self.engineConfig.currentProjectAssetPath+ '/assets.json')
        localElements = self.assetsStore.get('assetsComponentArray')['elements']

        ########################
        # Must be detail show
        if self.currentAsset != None:
            print('# Must be detail show')

        ########################
        asset = {
            'name': self.assetName.text,
            'type': 'ImageResource',
            'ext': collectExt,
            'source': CURRENT_ASSETPACK_PATH + '/' + str(self.assetName.text) + '.' + collectExt,
            'path': 'projects/' + self.engineConfig.currentProjectName + "/data/"+ str(self.assetName.text) + "/" + str(self.assetName.text) + "." + collectExt,
            'version': self.engineConfig.getVersion()
        }
        localElements.append(asset)
        self.assetsStore.put('assetsComponentArray', elements=localElements)

    def createImageAssets(self, instance):
        print("Creating first assets ... ")
        # resolvePathFolder
        self.resolvePathFolder()
        self.resolveAssetPathFolder()
        self.popup.dismiss()


    def load_from_filechooser(self, instance , selectedData):
        print("Selected data: ", selectedData)

        #self.load(self.fileBrowser.path, self.fileBrowser.selection)
        localHandler = self.fileBrowser.selection[0].replace(self.fileBrowser.path, '')

        self.selectedPathLabel.text = localHandler
        self.previewPicture.source=self.fileBrowser.selection[0]

    def setFileBrowserPath(self, instance):
        self.fileBrowser.path = instance.text
        print( '>>>>instance.text>>>' , instance.text)
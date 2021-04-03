import os
import io
import psutil
import threading
import string
from kivy.utils import platform
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
from engine.common.commons import PictureAPath, getMessageBoxYesNo
from engine.common.jsonN import JsonN

class AssetsEditorPopupAdd():

    def __init__(self, **kwargs):

        self.engineConfig = kwargs.get("engineConfig")
        self.engineRoot = kwargs.get("engineRoot")
        self.currentAsset = kwargs.get("currentAsset")

        self.operationStatus = True
        self.isFreeRigthBox = True

        self.box = BoxLayout(orientation="horizontal")
        self.leftBox = BoxLayout(orientation="vertical")
        self.imageResourceGUIBox = BoxLayout(orientation="vertical")

        print("DEBUG", platform)

        if platform == 'linux':
            drives = psutil.disk_partitions()

        if platform == 'win':
            drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]

        for item in drives:
            print(item)

        self.drivesChooseBox = BoxLayout(size_hint=(1, None),  height=40,)
        for item in drives:
            if platform == 'win':
                self.drivesChooseBox.add_widget(Button(
                    text=item + '/',
                    on_press=partial(self.setFileBrowserPath),
                            color=(self.engineConfig.getThemeTextColor()),
                        size_hint=(1, None),  height=65,
                        background_normal= '',
                        background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground'))
                ))
                print(" drive: ", item)
            elif platform == 'linux' or True:
                self.drivesChooseBox.add_widget(Button(
                    text=item.mountpoint ,
                    on_press=partial(self.setFileBrowserPath),
                            color=(self.engineConfig.getThemeTextColor()),
                        size_hint=(1, None),  height=65,
                        background_normal= '',
                        background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground'))
                ))
                print(" drive: ", item)


        self.imageResourceGUIBox.add_widget(self.drivesChooseBox)

        if platform == 'win':
            self.fileBrowser = FileChooserListView(# select_string='Select', dirselect: True
                # path='projects/' + self.engineConfig.currentProjectName + '/data/',
                filters=['*.png', '*.jpg'],
                path= drives[0] + '/',
                size_hint=(1,3),
                dirselect= True,
                on_submit=self.load_from_filechooser
            )
        elif platform == 'linux' or True:
            self.fileBrowser = FileChooserListView(# select_string='Select', dirselect: True
                # path='projects/' + self.engineConfig.currentProjectName + '/data/',
                filters=['*.png', '*.jpg'],
                path= drives[0].mountpoint + '/',
                size_hint=(1,3),
                dirselect= True,
                on_submit=self.load_from_filechooser
            )
            
        self.imageResourceGUIBox.add_widget(self.fileBrowser)
        self.fileBrowser.bind(selection=partial(self.load_from_filechooser))

        self.imageResourceGUIBox.add_widget(Label(text='Application assets pack path' , size_hint=(1, None),  height=40 ), )
        self.selectedPathLabel = Label(text='...')
        self.imageResourceGUIBox.add_widget(self.selectedPathLabel)

        self.assetName = TextInput( text='MyAssets1', foreground_color=(0,1,1, 1),
                                    size_hint=(1, None),  height=40)
        with self.assetName.canvas.before:
            Color(self.engineConfig.getThemeCustomColor('background')[0],
                     self.engineConfig.getThemeCustomColor('background')[1],
                     self.engineConfig.getThemeCustomColor('background')[2],
                     self.engineConfig.getThemeCustomColor('background')[3])
            self.assetName.rect = Rectangle(size=self.assetName.size,
                                            pos=self.assetName.pos)
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        self.imageResourceGUIBox.add_widget(self.assetName)

        # self.assetName.bind(pos=update_rect, size=update_rect)

        self.assetName.foreground_color = (1,1,1,1)

        self.commandBtn = Button(text='Add selected image',
                                 color=(self.engineConfig.getThemeTextColor()),
                                 size_hint=(1, None),  height=60,
                                 background_normal= '',
                                 background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')) )
                                 #on_press=partial(self.createImageAssets))
        self.commandBtn.bind(on_press=partial(self.createImageAssets))

        self.imageResourceGUIBox.add_widget(self.commandBtn)

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
                                size_hint=(1, None),  height=60,
                                background_normal= '',
                                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')))

        self.leftBox.add_widget(self.addImageRes)

        # Others  - Fonts
        self.addFontRes = Button(markup=True, text='[b]Add Font Resource[b]',
                                color=(self.engineConfig.getThemeTextColor()),
                                size_hint=(1, None),  height=60,
                                background_normal= '',
                                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')))

        # Add JSON Data  - JSONResource
        self.addJSONResBtn = Button(markup=True, text='[b]Add JSON DATA Resource[b]',
                                color=(self.engineConfig.getThemeTextColor()),
                                size_hint=(1, None),  height=60,
                                background_normal= '',
                                background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')))

        self.leftBox.add_widget(self.addJSONResBtn)
        self.leftBox.add_widget(self.addFontRes)
        self.leftBox.add_widget(self.cancelBtn)

        self.previewFont = Label(
                                  size_hint=(1, 1),
                                  markup=True,
                                  font_size=50,
                                  text="Font [b]Bold[/b]!")

        _local = 'CrossK ' + self.engineConfig.getVersion() + ' Assets Editor'
        self.popup = Popup(title=_local , content=self.box, auto_dismiss=False)

        self.cancelBtn.bind(on_press=self.popup.dismiss)
        self.addImageRes.bind(on_press=lambda a:self.showImageAssetGUI())
        self.addFontRes.bind(on_press=lambda a:self.showFontAssetGUI())
        self.addJSONResBtn.bind(on_press=lambda a:self.showJSONAssetGUI())

        self.popup.open()

    def showImageAssetGUI(self):
        # no prepare it si initial
        if self.isFreeRigthBox == True:
            self.box.add_widget(self.imageResourceGUIBox)
            self.isFreeRigthBox = False

            self.previewPicture.size_hint = (1,1)
            self.previewFont.size_hint = (0,0)

    def showFontAssetGUI(self):
        if self.isFreeRigthBox == True:
            # prepare
            self.fileBrowser.filters = ['*.ttf']
            self.commandBtn.text = 'Add Font Family'
            self.commandBtn.unbind(on_press=partial(self.createImageAssets)),
            self.commandBtn.bind(on_press=partial(self.createFontAssets))

            self.previewPicture.size_hint = (0,0)
            self.previewFont.size_hint = (1,1)

            self.box.add_widget(self.imageResourceGUIBox)
            self.isFreeRigthBox = False

    def showJSONAssetGUI(self):
        if self.isFreeRigthBox == True:
            # prepare
            self.fileBrowser.filters = ['*.json']
            self.commandBtn.text = 'Add JSON Object Data'

            self.commandBtn.unbind(on_press=partial(self.createImageAssets)),
            self.commandBtn.bind(on_press=partial(self.createJSONAssets))

            self.previewPicture.size_hint = (0,0)
            # self.previewFont.size_hint = (0,0)

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

    def resolveAssetPathFolder(self, typeOfAsset):

        CURRENT_ASSETPACK_PATH = os.path.abspath(
          os.path.join(os.path.dirname(__file__), '../../projects/' + self.engineConfig.currentProjectName + "/data/" + self.assetName.text)
        )

        collectExt = ''
        local = self.fileBrowser.selection[0][::-1]
        for item in local:
            if item == '.':
                print("Create Image Resource -> Break EXT = ", collectExt)
                break
            else:
                collectExt += item;
        collectExt = collectExt[::-1]
        # print(collectExt)

        if not os.path.exists(CURRENT_ASSETPACK_PATH):
            print("MAKE_ASSETS_PACK_DIR")
            os.mkdir(CURRENT_ASSETPACK_PATH)
        else:
            if self.currentAsset == None:
                print("SOMETHIND WRONG - ASSETS ALREADY EXIST")
                getMessageBoxYesNo(
                    message="Asset reference path with this name already exist. Please use some different name.",
                    msgType="OK")
                    #callback=wtf)
                return None

        self.operationStatus = False
        print("Assets pack write meta data...")
        copyfile(self.fileBrowser.selection[0], CURRENT_ASSETPACK_PATH + '/' + str(self.assetName.text) + '.' + collectExt)
        self.assetsStore = JsonStore(self.engineConfig.currentProjectAssetPath+ '/assets.json')
        localElements = self.assetsStore.get('assetsComponentArray')['elements']

        asset = {
            'name': self.assetName.text,
            'type': typeOfAsset,
            'ext': collectExt,
            'source': CURRENT_ASSETPACK_PATH + '/' + str(self.assetName.text) + '.' + collectExt,
            'path': 'projects/' + self.engineConfig.currentProjectName + "/data/"+ str(self.assetName.text) + "/" + str(self.assetName.text) + "." + collectExt,
            'version': self.engineConfig.getVersion()
        }

        # Check it if exist
        localCheckDouble = False
        for checkItem in localElements:
            if checkItem['name'] == asset['name']:
                localCheckDouble = True
                getMessageBoxYesNo(
                    message="Asset reference with this name already exist. Please use some different name.",
                    msgType="OK")
                    #callback=wtf)
        if localCheckDouble == False:
            localElements.append(asset)
            self.assetsStore.put('assetsComponentArray', elements=localElements)
            self.engineRoot.resourceGUIContainer.selfUpdate()

    def createImageAssets(self, instance):
        if self.operationStatus == True:
            self.resolvePathFolder()
            self.resolveAssetPathFolder('ImageResource')
            self.popup.dismiss()

    def createFontAssets(self, instance):
        if self.operationStatus == True:
            self.resolvePathFolder()
            self.resolveAssetPathFolder('FontResource')
            self.popup.dismiss()

    def createJSONAssets(self, instance):
        if self.operationStatus == True:
            self.resolvePathFolder()
            self.resolveAssetPathFolder('JSONResource')
            self.popup.dismiss()

    def load_from_filechooser(self, instance , selectedData):
        print("Selected data: ", selectedData)
        #self.load(self.fileBrowser.path, self.fileBrowser.selection)
        localHandler = self.fileBrowser.selection[0].replace(self.fileBrowser.path, '')

        self.selectedPathLabel.text = localHandler

        # check type assets
        print(">>", self.fileBrowser.filters)
        if self.fileBrowser.filters[0] ==  '*.png' or self.fileBrowser.filters[0] == '*.jpg':
            self.previewPicture.source=self.fileBrowser.selection[0]

        # JSON Nidza
        if '.json' in localHandler:
            self.imageResourceGUIBox.remove_widget(self.previewBox)

            testJSONNidzaLOader = JsonN(
                    assetsPath=self.fileBrowser.selection[0],
                    currentContainer=self.imageResourceGUIBox,
                    engineRoot=self.engineRoot
                )

    def setFileBrowserPath(self, instance):
        self.fileBrowser.path = instance.text
        print( 'setFileBrowserPath: ' , instance.text)

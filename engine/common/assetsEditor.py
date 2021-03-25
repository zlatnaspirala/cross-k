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
from engine.common.commons import getMessageBoxYesNo

class AssetsEditorPopup():

    def __init__(self, **kwargs):

        self.engineConfig = kwargs.get("engineConfig")
        self.currentAsset = kwargs.get("currentAsset")

        self.assetsStore = JsonStore('projects/' + self.engineConfig.currentProjectName + '/data/assets.json')

        # self.currentAsset is flag for editor Assets Details fomrs
        # if self.currentAsset == None:  -> it is strick add procedure
        if self.currentAsset == None:
            print('current asset need selected... any way for now', self.currentAsset) 

        print('current asset need selected... any way for now', self.currentAsset)

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

        self.imageResourceGUIBox.add_widget(Label(text='Application assets full source path:'))
        self.selectedPathLabel = Label(text='...')
        self.imageResourceGUIBox.add_widget(self.selectedPathLabel)

        self.imageResourceGUIBox.add_widget(Label(text='Application assets relative path:'))
        self.selectedRelativePathLabel = Label(text='...')
        self.imageResourceGUIBox.add_widget(self.selectedRelativePathLabel)

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

        self.imageResourceGUIBox.add_widget( Button(text='Update selected image asset',
                      color=(self.engineConfig.getThemeTextColor()),
                      size_hint=(1, None),  height=65,
                      background_normal= '',
                      background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                      on_press=partial(self.createImageAssets))
            )

        self.leftBox.add_widget(Label(text='CrossK assets editor', size_hint=(1, 0.1) ))
       
        titleText = Label(
                text='CrossK assets editor',
                color=(self.engineConfig.getThemeTextColor()),
                font_size=25, # add
                bold=True,    # add
                padding_x= 0, # test
                padding_y= 0, # test
                center=(1,1), # test
                font_blended= True,
                size_hint_x=1,
                size_hint_y=None,
                height=80)
        with titleText.canvas.before:
            Color(self.engineConfig.getThemeTextColorByComp('background')['r'],
                  self.engineConfig.getThemeTextColorByComp('background')['g'],
                  self.engineConfig.getThemeTextColorByComp('background')['b'])
            titleText.rect = Rectangle(size=titleText.size,
            pos=titleText.pos)
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        self.leftBox.add_widget(titleText)
        titleText.bind(pos=update_rect, size=update_rect)

        loadAssetElements = self.assetsStore.get('assetsComponentArray')['elements']


        for _index, item in enumerate(loadAssetElements):
            localBox = BoxLayout(size_hint=(1, None), height=30)
            test = Button(
                markup=True,
                halign="left", valign="middle",
                padding_x= 10,
                font_size=15,
                text='[b]' + item['name'] + '[/b][u][i] Image[/i][/u]',
                color=self.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=(self.engineConfig.getThemeBgSceneBtnColor()),
                on_press=partial(self.showAssetGUI, item),
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
                color=(self.engineConfig.getThemeCustomColor("alert")),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('background')),
                on_press=partial(self.showAssetGUI, item),
                size_hint=(0.2, None),
                height=30
            )
            localBox.add_widget(deleteAssetBtn)

        self.leftBox.add_widget(localBox)

        fillSpace = Label(text='', size_hint=(1,1))
        with fillSpace.canvas.before:
            Color(self.engineConfig.getThemeTextColorByComp('background')['r'],
                  self.engineConfig.getThemeTextColorByComp('background')['g'],
                  self.engineConfig.getThemeTextColorByComp('background')['b'])
            fillSpace.rect = Rectangle(size=fillSpace.size,
            pos=fillSpace.pos)
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        self.leftBox.add_widget(fillSpace)
        fillSpace.bind(pos=update_rect, size=update_rect)

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

        self.leftBox.add_widget(self.cancelBtn)
        # self.box.add_widget(self.infoBtn)

        _local = 'CrossK ' + self.engineConfig.getVersion() + ' Assets Editor'
        popup = Popup(title=_local , content=self.box, auto_dismiss=False)

        self.cancelBtn.bind(on_press=popup.dismiss)

        popup.open()

    def showAssetGUI(self, item, instance):

        
        test1 = os.path.join( '../../', 'projects/' + self.engineConfig.currentProjectName + "/")
        print("RRRRRRRRRRRRRRRRRR ", test1)

        print("ITEMinstanceIS ", os.path.dirname(__file__))

        transformPath = item['path'].replace('/', '\\')
        self.previewPicture.source=transformPath
        # det type of assets
        if item['type'] == 'ImageResource':
            if self.isFreeRigthBox == True:
                self.box.add_widget(self.imageResourceGUIBox)
                self.isFreeRigthBox = False
            self.assetName.text = item['name']
            self.selectedPathLabel.text = item['source']
            self.selectedRelativePathLabel.text = item['path']


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

        if len(self.fileBrowser.selection) == 0:
            def wtf():
                print('wtf')
            getMessageBoxYesNo( message="Nothing to update. Please select new source file.", msgType="OK", callback=wtf)
            return 0

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

        # localElements.append(asset)
        for _index, item in enumerate(localElements):
            if item['name'] == asset['name']:
                print("GOOOOD")
                localElements[_index] = asset

        self.assetsStore.put('assetsComponentArray', elements=localElements)

    def createImageAssets(self, instance):
        print("Creating first assets ... ")
        # resolvePathFolder
        self.resolvePathFolder()
        self.resolveAssetPathFolder()


    def load_from_filechooser(self, instance , selectedData):
        print("Selected data: ", selectedData)

        #self.load(self.fileBrowser.path, self.fileBrowser.selection)
        # localHandler = self.fileBrowser.selection[0].replace(self.fileBrowser.path, '')

        if str(self.fileBrowser.selection[0]).find('.png') != -1 and 
           str(self.fileBrowser.selection[0]).find('.jpg') != -1:
            print "Found!"
        else:
            print "Not found!"

        self.selectedPathLabel.text = localHandler
        self.previewPicture.source=self.fileBrowser.selection[0]

    def setFileBrowserPath(self, instance):
        self.fileBrowser.path = instance.text
        print( '>>>>instance.text>>>' , instance.text)
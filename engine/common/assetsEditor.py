import os
import io
import psutil
import threading
import string
from shutil import copyfile, rmtree
from functools import partial
from kivy.app import App
from kivy.utils import platform
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image, AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.storage.jsonstore import JsonStore
from kivy.core.clipboard import Clipboard
from engine.common.commons import PictureAPath
from engine.common.commons import getMessageBoxYesNo
from engine.common.fontFactory import FontFactory

class AssetsEditorPopup():

    def __init__(self, **kwargs):

        self.engineConfig = kwargs.get("engineConfig")
        self.currentAsset = kwargs.get("currentAsset")
        self.engineRoot = kwargs.get("engineRoot")
        self.assetsStore = JsonStore('projects/' + self.engineConfig.currentProjectName + '/data/assets.json')

        self.isFreeRigthBox = True
        self.box = BoxLayout(orientation="horizontal")

        self.leftBox = BoxLayout(orientation="vertical")
        self.imageResourceGUIBox = BoxLayout(orientation="vertical")

        if platform == 'linux':
            drives = psutil.disk_partitions()

        if platform == 'win':
            drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]

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
            self.fileBrowser = FileChooserListView(
                # Can be added default optimal engine config initial dir
                # select_string='Select', dirselect: True
                # path='projects/' + self.engineConfig.currentProjectName + '/data/',
                filters=['*.png', '*.jpg'],
                path= drives[1] + '/',
                size_hint=(1,3),
                dirselect= False,
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

        self.imageResourceGUIBox.add_widget(Label(text='Application assets full source path:',
                                                  size_hint=(1, None), height=40, font_size=15))
        self.selectedPathLabel = Label(text='...', size_hint=(1, None),  height=40, font_size=9, underline=True)
        self.imageResourceGUIBox.add_widget(self.selectedPathLabel)

        self.imageResourceGUIBox.add_widget(Label(text='Application assets relative path:', size_hint=(1, None), height=40))

        self.selectedRelativePathLabel = Button(text='...', size_hint=(1, None), height=40,
                                               font_size=12, underline=True,
                                               on_press=partial(self.copyToClipBoard),
                                               color=(self.engineConfig.getThemeTextColor()),
                                               background_normal= '',
                                               background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                                                )

        self.imageResourceGUIBox.add_widget(self.selectedRelativePathLabel)

        self.assetNameGUINAme = Label(text='Name of assets reference (READ ONLY)',
                                      color=(self.engineConfig.getThemeTextColor()),
                                      font_size=15,
                                      size_hint=(1, None),
                                      height=40)

        self.imageResourceGUIBox.add_widget(self.assetNameGUINAme)

        self.assetName = Label( text='MyAssets1',
                                color=(self.engineConfig.getThemeTextColor()),
                                font_size=12,
                                underline=True,
                                size_hint=(1, None),  height=40)

        with self.assetName.canvas.before:
            Color(self.engineConfig.getThemeCustomColor('warn')[0],
                  self.engineConfig.getThemeCustomColor('warn')[1],
                  self.engineConfig.getThemeCustomColor('warn')[2],
                  self.engineConfig.getThemeCustomColor('warn')[3])
            self.assetName.rect = Rectangle(size=self.assetName.size,
            pos=self.assetName.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        self.imageResourceGUIBox.add_widget(self.assetName)

        self.imageResourceGUIBox.add_widget(
            Button(text='Update selected image asset',
                   color=(self.engineConfig.getThemeTextColor()),
                   size_hint=(1, None),  height=65,
                   font_size=15,
                   bold=True,
                   background_normal= '',
                   background_color=(self.engineConfig.getThemeCustomColor('engineBtnsBackground')),
                   on_press=partial(self.createImageAssets)))

        self.leftBox.add_widget(Label(text='CrossK assets editor', size_hint=(1, None),
                        height=220,
                        font_size=25,
                        bold=True ))

        assetListHeder = BoxLayout(size_hint=(1, None), height=80)

        titleText = Label(
                text='Assets List.',
                color=(self.engineConfig.getThemeTextColor()),
                font_size=25,
                bold=True,
                padding_x= 0,
                padding_y= 0,
                center=(1,1),
                size_hint_x=1,
                size_hint_y=1,
                height=60)
        with titleText.canvas.before:
            Color(self.engineConfig.getThemeBgSceneBtnColor())
            titleText.rect = Rectangle(size=titleText.size,
                                       pos=titleText.pos)
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        self.leftBox.add_widget(titleText)
        titleText.bind(pos=update_rect, size=update_rect)

        headerSelector = Label(
                text='Selector',
                color=(self.engineConfig.getThemeTextColor()),
                font_size=15, # add
                bold=True,    # add
                padding_x= 0, # test
                padding_y= 0, # test
                center=(1,1), # test
                font_blended= True,
                size_hint_x=1,
                size_hint_y=None,
                height=40)
        with headerSelector.canvas.before:
            Color(self.engineConfig.getThemeTextColorByComp('background')['r'],
                  self.engineConfig.getThemeTextColorByComp('background')['g'],
                  self.engineConfig.getThemeTextColorByComp('background')['b'])
            headerSelector.rect = Rectangle(size=headerSelector.size,
            pos=headerSelector.pos)
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
 
        headerSelector.bind(pos=update_rect, size=update_rect)
        assetListHeder.add_widget(headerSelector)

        headerPreview = Label(
                text='Preview',
                color=(self.engineConfig.getThemeTextColor()),
                font_size=15, # add
                bold=True,    # add
                padding_x= 0, # test
                padding_y= 0, # test
                center=(1,1), # test
                font_blended= True,
                size_hint_x=0.3,
                size_hint_y=None,
                height=40)
        with headerPreview.canvas.before:
            Color(self.engineConfig.getThemeTextColorByComp('background')['r'],
                  self.engineConfig.getThemeTextColorByComp('background')['g'],
                  self.engineConfig.getThemeTextColorByComp('background')['b'])
            headerPreview.rect = Rectangle(size=headerPreview.size,
            pos=headerPreview.pos)
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        headerPreview.bind(pos=update_rect, size=update_rect)

        assetListHeder.add_widget(headerPreview)

        headerDelete = Label(
                text='Note: No undo operation',
                color=(self.engineConfig.getThemeTextColor()),
                font_size=15, # add
                bold=True,    # add
                padding_x= 0, # test
                padding_y= 0, # test
                center=(1,1), # test
                font_blended= True,
                size_hint_x=1,
                size_hint_y=None,
                height=40)
        with headerDelete.canvas.before:
            Color(self.engineConfig.getThemeTextColorByComp('background')['r'],
                  self.engineConfig.getThemeTextColorByComp('background')['g'],
                  self.engineConfig.getThemeTextColorByComp('background')['b'])
            headerDelete.rect = Rectangle(size=headerDelete.size,
            pos=headerDelete.pos)
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        headerDelete.bind(pos=update_rect, size=update_rect)
        assetListHeder.add_widget(headerDelete)

        self.leftBox.add_widget(assetListHeder)

        loadAssetElements = self.assetsStore.get('assetsComponentArray')['elements']

        self.sceneScroller = ScrollView(
                                    size_hint=(1, None),
                                    size=(500,650),
                                    pos_hint= {'center_x':0.5,'top': 0})
        self.selfUpdate(loadAssetElements)

        self.leftBox.add_widget(self.sceneScroller)

        fillSpace = Label(text='---', size_hint=(1,0.3))
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
        self.previewFont = Label(
                                  size_hint=(1, 1),
                                  markup=True,
                                  font_size=50,
                                  text="Font [b]Bold[/b]!")
        self.previewBox.add_widget(Label(text='Preview Box', bold= True, font_size=15 ))
        self.previewBox.add_widget(self.previewPicture)
        self.previewBox.add_widget(self.previewFont)

        self.imageResourceGUIBox.add_widget(self.previewBox)

        self.box.add_widget(self.leftBox)

        self.leftBox.add_widget(self.cancelBtn)

        _local = 'CrossK ' + self.engineConfig.getVersion() + ' Assets Editor'
        self.popup = Popup(title=_local , content=self.box, auto_dismiss=False)
        self.cancelBtn.bind(on_press=self.popup.dismiss)
        self.popup.open()

    def showAssetGUI(self, item, instance):

        if (platform == 'win'):
            transformPath = item['path'].replace('/', '\\')
        else:
            transformPath = item['path']

        if item['type'] == 'ImageResource':
            if self.isFreeRigthBox == True:
                self.box.add_widget(self.imageResourceGUIBox)
                self.isFreeRigthBox = False
            self.assetName.text = item['name']
            self.selectedPathLabel.text = item['source']
            self.selectedRelativePathLabel.text = item['path']
            self.previewPicture.source=transformPath
            self.previewFont.size_hint = (0,0)
            self.previewPicture.size_hint = (1,1)
        elif item['type'] == 'FontResource':
            if self.isFreeRigthBox == True:
                self.box.add_widget(self.imageResourceGUIBox)
                self.isFreeRigthBox = False
            self.assetName.text = item['name']
            self.selectedPathLabel.text = item['source']
            self.selectedRelativePathLabel.text = item['path']
            self.previewPicture.size_hint = (0,0)
            self.previewPicture.size = (5,5)
            self.previewFont.text="Font [b]Bold[/b]!"
            self.previewFont.size_hint = (1,1)
            self.previewFont.font_name=item['path']
        elif item['type'] == 'JSONResource':
            self.fileBrowser.filters = ["*.json"]
            if self.isFreeRigthBox == True:
                self.box.add_widget(self.imageResourceGUIBox)
                self.isFreeRigthBox = False
            self.assetName.text = item['name']
            self.selectedPathLabel.text = item['source']
            self.selectedRelativePathLabel.text = item['path']
            self.previewPicture.size_hint = (0,0)
            self.previewPicture.size = (5,5)
            self.previewFont.size_hint = (1,1)
            # nikola 0.5.0
            localStore = JsonStore(item['path'])
            print(">>>>>>>>>>>>>>>" + localStore.get('name'))
            self.previewFont.font_size = "10";
            self.previewFont.text = "JSON root keys: \n "
            for key in localStore._data.keys():
                self.previewFont.text += " " + key + "\n";
                #  localStore.get('name') 
                print(key)

    def copyToClipBoard(self, instance):
        Clipboard.copy(self.selectedRelativePathLabel.text)
        print('Copied to clipboard.')

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

        localCheckIsExist = False
        for _index, item in enumerate(localElements):
            if item['name'] == asset['name']:
                localCheckIsExist = True
                localElements[_index] = asset
        def catchErr1():
            print("catchErr1")

        if localCheckIsExist == True:
            self.assetsStore.put('assetsComponentArray', elements=localElements)
            # resourceGUIContainer 
            self.popup.dismiss()
        else:
            getMessageBoxYesNo(message='Something wrong with updating asset name => ' + asset['name'], msgType='OK', callback=catchErr1)

    def createImageAssets(self, instance):
        print("Creating first assets ... ")
        # resolvePathFolder
        self.resolvePathFolder()
        self.resolveAssetPathFolder()

    def deleteAsset(self, item, instance):

        self.assetsStore = JsonStore('projects/'+self.engineConfig.currentProjectName +'/data/assets.json')
        currElements = self.assetsStore.get('assetsComponentArray')['elements']

        isDeleted = False
        for index, itemA in enumerate(currElements):
            if itemA['name'] == item['name']:
                currElements.pop(index)
                isDeleted = True
                self.assetsStore.put('assetsComponentArray', elements=currElements)
                break

        if isDeleted == True:
            self.engineRoot.resourceGUIContainer.selfUpdate()
            self.selfUpdate(currElements)
            rmtree('projects/' + self.engineConfig.currentProjectName +'/data/' + item['name'])
        else:
            getMessageBoxYesNo( message="Something wrong with delete operation.", msgType="OK", callback=wtf)

    def load_from_filechooser(self, instance , selectedData):
        # Selector
        if str(self.fileBrowser.selection[0]).find('.png') != -1 or str(self.fileBrowser.selection[0]).find('.jpg') != -1:
            print("Found!")
        else:
            print("Not found!")
            return None
        self.selectedPathLabel.text = self.fileBrowser.selection[0]
        self.previewPicture.source=self.fileBrowser.selection[0]

    def setFileBrowserPath(self, instance):
        self.fileBrowser.path = instance.text
        print('Selected:', instance.text)

    def selfUpdate(self, loadAssetElements):

        alllocalBox = BoxLayout(size_hint=(1, None), height=len(loadAssetElements) * 90, orientation='vertical')
        for _index, item in enumerate(loadAssetElements):

            localBox = BoxLayout(size_hint=(1, None),height=90,  orientation='horizontal')
            currentColor = (self.engineConfig.getThemeBgSceneBtnColor())
            if item['type'] == 'ImageResource':
                currentColor = (self.engineConfig.getThemeBgSceneBoxColor())

            localBox.add_widget(Button(
                markup=True,
                halign="left", valign="middle",
                padding_x= 10,
                font_size=15,
                text='[b]' + item['name'] + '[/b] [u][i]' + item['type'] + '[/i][/u]',
                color=self.engineConfig.getThemeTextColor(),
                background_normal= '',
                background_color=currentColor,
                on_press=partial(self.showAssetGUI, item),
                size_hint=(1, None),
                height=90
            ))
            if item['type'] == 'ImageResource':
                localPrevListBox = AsyncImage(
                                      source=item['path'], size_hint=(0.4, None) , height=90 )
                with localPrevListBox.canvas.before:
                    Color(self.engineConfig.getThemeCustomColor('background')[0],
                                 self.engineConfig.getThemeCustomColor('background')[1],
                                 self.engineConfig.getThemeCustomColor('background')[2],
                                 self.engineConfig.getThemeCustomColor('background')[3])
                    localPrevListBox.rect = Rectangle(size=localPrevListBox.size,
                                                      pos=localPrevListBox.pos)
                def update_rect(instance, value):
                    instance.rect.pos = instance.pos
                    instance.rect.size = instance.size
                localPrevListBox.bind(pos=update_rect, size=update_rect)

                localBox.add_widget(localPrevListBox)
            elif item['type'] == 'FontResource':
                localBox.add_widget( Label(font_name=item['path'], size_hint=(0.4, None) , height=90, text = 'Font' ))
            elif item['type'] == 'JSONResource':
                localBox.add_widget( Label(size_hint=(0.4, None) , height=90, text = 'JSON DATA' ))

            localBox.add_widget(Button(
                markup=True,
                halign="left", valign="middle",
                padding_x= 10,
                font_size=15,
                text='[b]Delete[/b]',
                color=(self.engineConfig.getThemeCustomColor("alert")),
                background_normal= '',
                background_color=(self.engineConfig.getThemeCustomColor('background')),
                on_press=partial(self.deleteAsset, item),
                size_hint=(1, None),
                height=90
            ))
            print('ADDED ', item)
            alllocalBox.add_widget(localBox)

        self.sceneScroller.clear_widgets()

        self.sceneScroller.add_widget(alllocalBox)

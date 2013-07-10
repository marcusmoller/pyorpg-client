import pygame
from pygame.locals import *
from pgu import gui
import pygUI as pygUI

from objects import Item
from constants import *
import global_vars as g


UI_FONT_COLOR = (251, 230, 204)


class OpenItemDialog(gui.Dialog):
    def __init__(self, engine, **params):
        self.engine = engine

        self._count = 0

        title = gui.Label("Open Item")

        t = gui.Table()

        t.tr()
        t.td(gui.Label('Select an item:'), colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        self.itemList = gui.List(width=200, height=140)
        t.td(self.itemList, colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        e = gui.Button('Open item')
        e.connect(gui.CLICK, self.openItem, None)
        t.td(e)

        e = gui.Button('Cancel')
        e.connect(gui.CLICK, self.close, None)
        t.td(e)

        t.tr()
        t.td(gui.Spacer(10, 10))

        gui.Dialog.__init__(self, title, t)

    def openItem(self, value):
        listValue = self.itemList.value

        if listValue != None:
            self.engine.openItem(itemNum=listValue)
            self.close()

    def openDialog(self, value):
        self.loadItems()
        self.open()

    def loadItems(self):
        self.clearList()
        for i in range(MAX_ITEMS):
            if Item[i].name != '':
                self.addItem(str(i) + ' - "' + Item[i].name + '"')

        self.itemList.resize()
        self.itemList.repaint()

    def addItem(self, item):
        self.itemList.add(gui.Label(item), value=self._count)
        self._count += 1

    def clearList(self):
        self.itemList.clear()
        self.itemList.resize()
        self.itemList.repaint()
        self._count = 0


class ItemEditorContainer(gui.Container):
    def __init__(self, engine, **params):
        gui.Container.__init__(self, **params)

        self.engine = engine
        self.value = gui.Form()

        # dialogs
        openItemDialog = OpenItemDialog(self)

        # menu title
        self.tTitle = gui.Table(width=272, height=32)

        self.tTitle.tr()
        self.tTitle.td(gui.Label("Item Editor", name='itemTitle', color=UI_FONT_COLOR))

        # content
        self.tContent = gui.Table(width=272, height=200)

        self.tContent.tr()
        e = gui.Button("Open item...", width=100)
        e.connect(gui.CLICK, openItemDialog.openDialog, None)
        self.tContent.td(e, colspan=2)

        self.tContent.tr()
        self.tContent.td(gui.Label('Item Name:', color=UI_FONT_COLOR))
        self.tContent.td(gui.Input('', size=16, name='inpItemName'))

        self.tContent.tr()
        self.tContent.td(gui.Label('Item Type:', color=UI_FONT_COLOR))
        e = gui.Select(name='selItemType')
        e.add('None', 0)
        e.add('Weapon', 1)
        e.add('Armor', 2)
        e.add('Helmet', 3)
        e.add('Shield', 4)
        e.add('Potion (+HP)', 5)
        e.add('Potion (+MP)', 6)
        e.add('Potion (+SP)', 7)
        e.add('Potion (-HP)', 8)
        e.add('Potion (-MP)', 9)
        e.add('Potion (-SP)', 10)
        e.add('Key', 11)
        e.add('Currency', 12)
        e.add('Spell', 13)
        e.value = 0
        e.connect(gui.CHANGE, self.updateType, None)
        self.tContent.td(e)
        '''
        self.tContent.tr()
        self.tContent.td(gui.Label('Item Data1:', color=UI_FONT_COLOR, name='lblItemData1'))
        self.tContent.td(gui.Input('', size=16, name='inpItemData1'))

        self.tContent.tr()
        self.tContent.td(gui.Label('Item Data2:', color=UI_FONT_COLOR, name='lblItemData2'))
        self.tContent.td(gui.Input('', size=16, name='inpItemData2'))

        self.tContent.tr()
        self.tContent.td(gui.Label('Item Data3:', color=UI_FONT_COLOR, name='lblItemData3'))
        self.tContent.td(gui.Input('', size=16, name='inpItemData3'))'''

        # bottom buttons
        self.tBottom = gui.Table(width=272, height=200)

        self.tBottom.tr()
        e = gui.Button("Save", width=100, height=40)
        e.connect(gui.CLICK, self.saveItem, None)
        self.tBottom.td(e)

        e = gui.Button("Cancel", width=100, height=40)
        e.connect(gui.CLICK, self.cancel, None)
        self.tBottom.td(e)

        self.add(self.tTitle, 0, 0)
        self.add(self.tContent, 0, 100)
        self.add(self.tBottom, 0, 368)

    def openItem(self, itemNum):
        # redraw selected sprite
        g.gameEngine.graphicsEngine.gameGUI.itemEditorGUI.selectedSpriteNum = Item[itemNum].pic
        g.gameEngine.graphicsEngine.gameGUI.itemEditorGUI.draw()

        if self.tContent.find('inpItemName'):
            self.value['inpItemName'].value = Item[itemNum].name

    def updateType(self, value):
        typeValue = self.value['selItemType'].value

        # create new rows if they don't exist
        # todo: this is stupid - it would be better with show/hide
        if not self.tContent.find('lblItemData1'):
            self.tContent.tr()
            self.tContent.td(gui.Label('Item Data1:', color=UI_FONT_COLOR, name='lblItemData1'))
            self.tContent.td(gui.Input('', size=16, name='inpItemData1'))

        if not self.tContent.find('lblItemData2'):
            self.tContent.tr()
            self.tContent.td(gui.Label('Item Data2:', color=UI_FONT_COLOR, name='lblItemData2'))
            self.tContent.td(gui.Input('', size=16, name='inpItemData2'))

        if not self.tContent.find('lblItemData3'):
            self.tContent.tr()
            self.tContent.td(gui.Label('Item Data3:', color=UI_FONT_COLOR, name='lblItemData3'))
            self.tContent.td(gui.Input('', size=16, name='inpItemData3'))

        # update labels
        if typeValue >= ITEM_TYPE_WEAPON and typeValue <= ITEM_TYPE_SHIELD:
            self.value['lblItemData1'].set_text('Durability:')
            self.value['lblItemData2'].set_text('Strength:')

            # remove data3
            self.tContent.remove(self.tContent.find('lblItemData3'))
            self.tContent.remove(self.tContent.find('inpItemData3'))

        elif typeValue >= ITEM_TYPE_POTIONADDHP and typeValue <= ITEM_TYPE_POTIONSUBSP:
            self.value['lblItemData1'].set_text('Vital Impact:')

            # remove data2 and data3
            self.tContent.remove(self.tContent.find('lblItemData2'))
            self.tContent.remove(self.tContent.find('inpItemData2'))
            self.tContent.remove(self.tContent.find('lblItemData3'))
            self.tContent.remove(self.tContent.find('inpItemData3'))

        elif typeValue == ITEM_TYPE_SPELL:
            self.value['lblItemData1'].set_text('Spell:')

            # remove data2 and data3
            self.tContent.remove(self.tContent.find('lblItemData2'))
            self.tContent.remove(self.tContent.find('inpItemData2'))
            self.tContent.remove(self.tContent.find('lblItemData3'))
            self.tContent.remove(self.tContent.find('inpItemData3'))
        else:
            # remove all data
            self.tContent.remove(self.tContent.find('lblItemData1'))
            self.tContent.remove(self.tContent.find('inpItemData1'))
            self.tContent.remove(self.tContent.find('lblItemData2'))
            self.tContent.remove(self.tContent.find('inpItemData2'))
            self.tContent.remove(self.tContent.find('lblItemData3'))
            self.tContent.remove(self.tContent.find('inpItemData3'))


    def saveItem(self, value):
        # save properties
        Map.name  = self.propertiesCtrl.value["inpMapName"].value
        Map.up    = int(self.propertiesCtrl.value["inpMapUp"].value)
        Map.down  = int(self.propertiesCtrl.value["inpMapDown"].value)
        Map.left  = int(self.propertiesCtrl.value["inpMapLeft"].value)
        Map.right = int(self.propertiesCtrl.value["inpMapRight"].value)

        # send the map
        g.tcpConn.sendMap()

        # quit editor
        self.quitEditor()

    def cancel(self, value):
        self.quitEditor()

    def quitEditor(self):
        g.gameEngine.graphicsEngine.gameGUI.setState(0)
        g.gameEngine.graphicsEngine.gameGUI.guiContainer.closeItemEditor()
        g.editor = EDITOR_NONE
        g.canMoveNow = True


class ItemEditorGUI():
    def __init__(self, surface):
        self.surface = surface

        # selected item sprite
        self.selectedSpriteNum = 0
        self.selectedSpriteSurface = pygame.Surface((PIC_X, PIC_Y))
        self.selectedSpriteRect = pygame.Rect((632, 80, 32, 32))

        # scroll buttons
        # - scroll buttons (place them near self.selectedSpriteRect)
        btnScrollLeft = pygUI.pygButton((600, 88, 32, 32), normal=g.dataPath + '/themes/default/hslider.left.tga')
        btnScrollRight = pygUI.pygButton((680, 88, 32, 32), normal=g.dataPath + '/themes/default/hslider.right.tga')

        self.scrollButtons = (btnScrollLeft, btnScrollRight)

    def init(self):
        self.draw()

    def draw(self):
        # update selected sprite surface
        tempImage = pygame.image.load(g.dataPath + '/items/' + str(self.selectedSpriteNum) + '.bmp').convert()
        self.selectedSpriteSurface.blit(tempImage, (0, 0))

        # render it onto the ui
        self.surface.blit(self.selectedSpriteSurface, self.selectedSpriteRect)

        # render all buttons
        for button in self.scrollButtons:
            button.draw(self.surface)

    def drawElements(self):
        for button in self.scrollButtons:
            button.draw(self.surface)

    def update(self, event):
        if 'click' in self.scrollButtons[0].handleEvents(event):
            # previous
            if self.selectedSpriteNum > 0:
                self.selectedSpriteNum -= 1

            self.draw()

        if 'click' in self.scrollButtons[1].handleEvents(event):
            # next
            if self.selectedSpriteNum < 18:
                self.selectedSpriteNum += 1

            self.draw()

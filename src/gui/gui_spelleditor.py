import pygame
from pygame.locals import *
from pgu import gui
import pygUI as pygUI

from objects import Spell, Item
from constants import *
import global_vars as g


UI_FONT_COLOR = (251, 230, 204)


class OpenSpellDialog(gui.Dialog):
    def __init__(self, engine, **params):
        self.engine = engine

        self._count = 0

        title = gui.Label("Open Spell")

        t = gui.Table()

        t.tr()
        t.td(gui.Label('Select a spell:'), colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        self.spellList = gui.List(width=200, height=140)
        t.td(self.spellList, colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        e = gui.Button('Open spell')
        e.connect(gui.CLICK, self.openSpell, None)
        t.td(e)

        e = gui.Button('Cancel')
        e.connect(gui.CLICK, self.close, None)
        t.td(e)

        t.tr()
        t.td(gui.Spacer(10, 10))

        gui.Dialog.__init__(self, title, t)

    def openSpell(self, value):
        listValue = self.spellList.value

        if listValue != None:
            self.engine.openSpell(spellNum=listValue)
            self.close()

    def openDialog(self, value):
        self.loadSpells()
        self.open()

    def loadSpells(self):
        self.clearList()
        for i in range(MAX_SPELLS):
            if Spell[i].name != '':
                self.addItem(str(i) + ' - "' + Spell[i].name + '"')

        self.spellList.resize()
        self.spellList.repaint()

    def addItem(self, item):
        self.spellList.add(gui.Label(item), value=self._count)
        self._count += 1

    def clearList(self):
        self.spellList.clear()
        self.spellList.resize()
        self.spellList.repaint()
        self._count = 0


class DataGiveItem(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)

        self.tr()
        self.lblItemNum = gui.Label('Item: 0', color=UI_FONT_COLOR)
        self.td(self.lblItemNum)

        self.tr()
        e = gui.HSlider(value=0, min=0, max=99, size=10, width=120, name='selDataDur')
        e.connect(gui.CHANGE, self.updateLabelItemNum, e)
        self.td(e)

        self.tr()
        self.td(gui.Spacer(10, 20))

        self.tr()
        self.lblStr = gui.Label('Strength: 0', color=UI_FONT_COLOR)
        self.td(self.lblStr)

        self.tr()
        e = gui.HSlider(value=0, min=0, max=99, size=10, width=120, name='selDataStr')
        e.connect(gui.CHANGE, self.updateLabelStr, e)
        self.td(e)

    def updateLabelStr(self, value):
        self.lblStr.set_text('Strength: ' + str(value.value))

    def updateLabelItemNum(self, value):
        self.lblItemNum.set_text('Item: ' + Item[value.value].name)


class DataVitalMod(gui.Table):
    def __init__(self, **params):
        # todo, set slider maximum = vital mod amount
        gui.Table.__init__(self, **params)

        self.tr()
        self.lblVital = gui.Label('Vital Mod: Use the slider', color=UI_FONT_COLOR)
        self.td(self.lblVital)

        self.tr()
        e = gui.HSlider(value=0, min=0, max=10, size=10, width=120, name='selDataVit')
        e.connect(gui.CHANGE, self.updateVitalName, e)
        self.td(e)

    def updateVitalName(self, value):
        self.lblVital.set_text('Vital Mod: ' + str(value.value))



class SpellEditorContainer(gui.Container):
    def __init__(self, engine, **params):
        gui.Container.__init__(self, **params)

        self.engine = engine
        self.value = gui.Form()

        # item editor state
        self.itemNum = None

        # dialogs
        openSpellDialog = OpenSpellDialog(self)

        # data types
        self.dataGiveItem = DataGiveItem(name="dataGiveItem")
        self.dataVitalMod = DataVitalMod(name="dataVitalMod")

        # menu title
        self.tTitle = gui.Table(width=272, height=32)

        self.tTitle.tr()
        self.tTitle.td(gui.Label("Spell Editor", name='spellTitle', color=UI_FONT_COLOR))

        # content
        self.tContent = gui.Table(width=272, height=123)

        self.tContent.tr()
        e = gui.Button("Open spell...", width=100)
        e.connect(gui.CLICK, openSpellDialog.openDialog, None)
        self.tContent.td(e, colspan=2)

        self.tContent.tr()
        self.tContent.td(gui.Label('Spell Name:', color=UI_FONT_COLOR), colspan=2)
        self.tContent.tr()
        self.tContent.td(gui.Input('', size=26, name='inpSpellName'), colspan=2, valign=-1)

        self.tContent.tr()
        self.tContent.td(gui.Label('Spell Type:', color=UI_FONT_COLOR))
        e = gui.Select(name='selSpellType')
        e.add('Add HP', 0)
        e.add('Add MP', 1)
        e.add('Add SP', 2)
        e.add('Remove HP', 3)
        e.add('Remove MP', 4)
        e.add('Remove SP', 5)
        e.add('Give item', 6)
        e.value = 0
        e.connect(gui.CHANGE, self.updateType, None)
        self.tContent.td(e)

        # data input
        self.tData = gui.Table(width=272, height=75)

        # bottom buttons
        self.tBottom = gui.Table(width=272, height=200)

        self.tBottom.tr()
        self.saveButton = gui.Button("Add Spell", width=100, height=40)
        self.saveButton .connect(gui.CLICK, self.saveItem, None)
        self.tBottom.td(self.saveButton)

        e = gui.Button("Cancel", width=100, height=40)
        e.connect(gui.CLICK, self.cancel, None)
        self.tBottom.td(e)

        self.add(self.tTitle, 0, 0)
        self.add(self.tContent, 0, 100)
        self.add(self.tData, 0, 255)
        self.add(self.tBottom, 0, 368)

    def openItem(self, itemNum):
        # redraw selected sprite
        g.gameEngine.graphicsEngine.gameGUI.itemEditorGUI.selectedSpriteNum = Item[itemNum].pic
        g.gameEngine.graphicsEngine.gameGUI.itemEditorGUI.draw()

        if self.tContent.find('inpItemName'):
            self.value['inpItemName'].value = Item[itemNum].name

        # set type and data
        typeValue = Item[itemNum].type
        self.value['selItemType'].value = typeValue

        if typeValue >= ITEM_TYPE_WEAPON and typeValue <= ITEM_TYPE_SHIELD:
            self.value['selDataDur'].value = int(0 if Item[itemNum].data1 is None else Item[itemNum].data1)
            self.value['selDataStr'].value = int(0 if Item[itemNum].data2 is None else Item[itemNum].data2)

        elif typeValue >= ITEM_TYPE_POTIONADDHP and typeValue <= ITEM_TYPE_POTIONSUBSP:
            self.value['selDataVit'].value = int(0 if Item[itemNum].data1 is None else Item[itemNum].data1)

        elif typeValue == ITEM_TYPE_SPELL:
            self.value['selDataSpell'].value = int(0 if Item[itemNum].data1 is None else Item[itemNum].data1)

        # rename save button
        self.saveButton.value = 'Save Item'

        # update item num
        self.itemNum = itemNum

    def hideAll(self):
        if self.tData.find("dataVitalMod"):
            self.tData.remove(self.tData.find("dataVitalMod"))

        if self.tData.find("dataGiveItem"):
            self.tData.remove(self.tData.find("dataGiveItem"))

    def updateType(self, value):
        typeValue = self.value['selSpellType'].value

        # update labels
        if typeValue != SPELL_TYPE_GIVEITEM:
            self.hideAll()
            self.tData.tr()
            self.tData.td(self.dataVitalMod, valign=-1)

        else:
            self.hideAll()
            self.tData.tr()
            self.tData.td(self.dataGiveItem, valign=-1)

    def saveItem(self, value):
        typeValue = self.value['selItemType'].value

        if self.itemNum == None:
            # if it's a new item then find a new item id to use
            for i in range(len(Item)):
                if Item[i].name == '':
                    self.itemNum = i
                    break

        # save item properties
        Item[self.itemNum].name = self.value['inpItemName'].value
        Item[self.itemNum].pic = g.gameEngine.graphicsEngine.gameGUI.itemEditorGUI.selectedSpriteNum
        Item[self.itemNum].type = typeValue

        # save item data
        if typeValue >= ITEM_TYPE_WEAPON and typeValue <= ITEM_TYPE_SHIELD:
            Item[self.itemNum].data1 = self.value['selDataDur'].value
            Item[self.itemNum].data2 = self.value['selDataStr'].value

        elif typeValue >= ITEM_TYPE_POTIONADDHP and typeValue <= ITEM_TYPE_POTIONSUBSP:
            Item[self.itemNum].data1 = self.value['selDataVit'].value

        elif typeValue == ITEM_TYPE_SPELL:
            Item[self.itemNum].data1 = self.value['selDataSpell'].value

        g.tcpConn.sendSaveItem(self.itemNum)

        # quit editor
        self.quitEditor()

    def cancel(self, value):
        self.quitEditor()

    def quitEditor(self):
        # reset everything
        #self.resetEditor()

        # quit
        g.gameEngine.graphicsEngine.gameGUI.setState(0)
        g.gameEngine.graphicsEngine.gameGUI.guiContainer.closeSpellEditor()
        g.editor = EDITOR_NONE
        g.canMoveNow = True

    def resetEditor(self):
        self.itemNum = None

        # selected sprite
        g.gameEngine.graphicsEngine.gameGUI.itemEditorGUI.selectedSpriteNum = 0

        # reset everything on quit
        self.value['inpItemName'].value = ''
        self.value['selItemType'].value = 0
        self.saveButton.value = 'Add item'

        # equipment
        self.value['selDataDur'].value = 0
        self.value['selDataStr'].value = 0

        # vit
        self.value['selDataVit'].value = 0

        # spell
        self.value['selDataSpell'].value = 0


class SpellEditorGUI():
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
        tempImage = pygame.image.load(g.dataPath + '/spells/' + str(self.selectedSpriteNum) + '.bmp').convert()
        pygame.draw.rect(self.selectedSpriteSurface, (0, 0, 0), (0, 0, 32, 32))
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

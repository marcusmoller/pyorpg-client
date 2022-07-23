import pygame
from pygame.locals import *
from pgu import gui
from .python_gui import *

from objects import Spell, Item
from resourcemanager import ResourceManager
from constants import *
import global_vars as g


UI_FONT_COLOR = (251, 230, 204)


class OpenSpellDialog(gui.Dialog):
    def __init__(self, engine, **params):
        self.engine = engine

        self._count = 0

        title = gui.Label(_("Open Spell"))

        t = gui.Table()

        t.tr()
        t.td(gui.Label(_('Select a spell:')), colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        self.spellList = gui.List(width=200, height=140)
        t.td(self.spellList, colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        e = gui.Button(_('Open spell'))
        e.connect(gui.CLICK, self.openSpell, None)
        t.td(e)

        e = gui.Button(_('Cancel'))
        e.connect(gui.CLICK, self.close, None)
        t.td(e)

        t.tr()
        t.td(gui.Spacer(10, 10))

        gui.Dialog.__init__(self, title, t)

    def openSpell(self, value):
        listValue = self.spellList.value

        if listValue != None:
            self.engine.requestOpenSpell(spellNum=listValue)
            self.close()

    def openDialog(self, value):
        self.loadSpells()
        self.open()

    def loadSpells(self):
        self.clearList()
        for i in range(MAX_SPELLS):
            if Spell[i].name != '':
                self.addItem(str(i) + ' - "' + str(Spell[i].name) + '"')

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
        self.lblItemNum = gui.Label(_('Item: 0'), color=UI_FONT_COLOR)
        self.td(self.lblItemNum)

        self.tr()
        self.sliItemNum = gui.HSlider(value=0, min=0, max=99, size=10, width=120, name='selDataItemNum')
        self.sliItemNum.connect(gui.CHANGE, self.updateLabelItemNum, self.sliItemNum)
        self.td(self.sliItemNum)

        self.tr()
        self.td(gui.Spacer(10, 20))

        self.tr()
        self.lblStr = gui.Label(_('Item Value: 0'), color=UI_FONT_COLOR)
        self.td(self.lblStr)

        self.tr()
        e = gui.HSlider(value=0, min=0, max=99, size=10, width=120, name='selDataItemVal')
        e.connect(gui.CHANGE, self.updateLabelStr, e)
        self.td(e)

    def updateMaxValues(self, maxItemNum):
        self.sliItemNum.max = maxItemNum

    def updateLabelStr(self, value):
        self.lblStr.set_text(_('Item Value: ') + str(value.value))

    def updateLabelItemNum(self, value):
        if Item[value.value].name != '':
            self.lblItemNum.set_text(_('Item: ') + Item[value.value].name)

        else:
            self.lblItemNum.set_text(_('Not a valid item num!'))


class DataVitalMod(gui.Table):
    def __init__(self, **params):
        # todo, set slider maximum = vital mod amount
        gui.Table.__init__(self, **params)

        self.tr()
        self.lblVital = gui.Label(_('Vital Mod: 0'), color=UI_FONT_COLOR)
        self.td(self.lblVital)

        self.tr()
        e = gui.HSlider(value=0, min=0, max=10, size=10, width=120, name='selDataVit')
        e.connect(gui.CHANGE, self.updateVitalName, e)
        self.td(e)

    def updateVitalName(self, value):
        self.lblVital.set_text(_('Vital Mod: ') + str(value.value))


class SpellEditorContainer(gui.Container):
    def __init__(self, engine, **params):
        gui.Container.__init__(self, **params)

        self.engine = engine
        self.value = gui.Form()

        # spell editor state
        self.spellNum = None

        # dialogs
        openSpellDialog = OpenSpellDialog(self)

        # data types
        self.dataGiveItem = DataGiveItem(name="dataGiveItem")
        self.dataVitalMod = DataVitalMod(name="dataVitalMod")

        # menu title
        self.tTitle = gui.Table(width=272, height=32)

        self.tTitle.tr()
        self.tTitle.td(gui.Label(_("Spell Editor"), name='spellTitle', color=UI_FONT_COLOR))

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

        # - make vital mod default
        self.tData.tr()
        self.tData.td(self.dataVitalMod, valign=-1)

        # bottom buttons
        self.tBottom = gui.Table(width=272, height=200)

        self.tBottom.tr()
        self.saveButton = gui.Button("Add Spell", width=100, height=40)
        self.saveButton .connect(gui.CLICK, self.saveSpell, None)
        self.tBottom.td(self.saveButton)

        e = gui.Button("Cancel", width=100, height=40)
        e.connect(gui.CLICK, self.cancel, None)
        self.tBottom.td(e)

        self.add(self.tTitle, 0, 0)
        self.add(self.tContent, 0, 100)
        self.add(self.tData, 0, 255)
        self.add(self.tBottom, 0, 368)

    def initialize(self):
        self.dataGiveItem.updateMaxValues(3)

    def requestOpenSpell(self, spellNum):
        # request edit spell
        g.tcpConn.sendEditSpell(spellNum)

    def openSpell(self, spellNum):
        # redraw selected sprite
        g.gameEngine.graphicsEngine.gameGUI.spellEditorGUI.selectedSpriteNum = Spell[spellNum].pic
        g.gameEngine.graphicsEngine.gameGUI.spellEditorGUI.draw()

        self.value['inpSpellName'].value = Spell[spellNum].name

        # set type and data
        typeValue = Spell[spellNum].type
        self.value['selSpellType'].value = typeValue

        if typeValue != SPELL_TYPE_GIVEITEM:
            self.value['selDataVit'].value = int(0 if Spell[spellNum].data1 is None else Spell[spellNum].data1)

        else:
            self.value['selDataItemNum'].value = int(0 if Spell[spellNum].data1 is None else Spell[spellNum].data1)
            self.value['selDataItemVal'].value = int(0 if Spell[spellNum].data2 is None else Spell[spellNum].data2)

        # rename save button
        self.saveButton.value = 'Save Spell'

        # update item num
        self.spellNum = spellNum

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

    def saveSpell(self, value):
        typeValue = self.value['selSpellType'].value

        if self.spellNum is None:
            # if it's a new spell then find a new spell id to use
            for i in range(len(Spell)):
                if Spell[i].name == '':
                    self.spellNum = i
                    break

        # save spell properties
        Spell[self.spellNum].name = self.value['inpSpellName'].value
        Spell[self.spellNum].pic = g.gameEngine.graphicsEngine.gameGUI.spellEditorGUI.selectedSpriteNum
        Spell[self.spellNum].type = typeValue

        # save spell data
        if typeValue != SPELL_TYPE_GIVEITEM:
            Spell[self.spellNum].data1 = self.value['selDataVit'].value
        else:
            Spell[self.spellNum].data1 = self.value['selDataItemNum'].value
            Spell[self.spellNum].data2 = self.value['selDataItemVal'].value

        Spell[self.spellNum].data3 = 0

        g.tcpConn.sendSaveSpell(self.spellNum)

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
        g.gameEngine.graphicsEngine.gameGUI.spellEditorGUI.selectedSpriteNum = 0

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
        btnScrollLeft = pygButton((600, 88, 32, 32), normal=g.dataPath + '/themes/default/hslider.left.tga')
        btnScrollRight = pygButton((680, 88, 32, 32), normal=g.dataPath + '/themes/default/hslider.right.tga')

        self.scrollButtons = (btnScrollLeft, btnScrollRight)

    def init(self):
        self.draw()

    def draw(self):
        # update selected sprite surface
        tempImage = ResourceManager.spellSprites[self.selectedSpriteNum]
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
            if self.selectedSpriteNum < len(ResourceManager.spellSprites)-1:
                self.selectedSpriteNum += 1

            self.draw()

import pygame
from pygame.locals import *
from pgu import gui
from .python_gui import *

from objects import Item, NPC, Stats
from resourcemanager import ResourceManager
from constants import *
import global_vars as g

class OpenNPCDialog(gui.Dialog):
    def __init__(self, engine, **params):
        self.engine = engine

        self._count = 0

        title = gui.Label("Open NPC")

        t = gui.Table()

        t.tr()
        t.td(gui.Label('Select a NPC:'), colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        self.npcList = gui.List(width=200, height=140)
        t.td(self.npcList, colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        e = gui.Button('Open NPC')
        e.connect(gui.CLICK, self.openNPC, None)
        t.td(e)

        e = gui.Button('Cancel')
        e.connect(gui.CLICK, self.close, None)
        t.td(e)

        t.tr()
        t.td(gui.Spacer(10, 10))

        gui.Dialog.__init__(self, title, t)

    def openNPC(self, value):
        listValue = self.npcList.value

        if listValue != None:
            self.engine.openNPC(npcNum=listValue)
            self.close()

    def openDialog(self, value):
        self.loadNPCs()
        self.open()

    def loadNPCs(self):
        self.clearList()
        for i in range(MAX_NPCS):
            if NPC[i].name != '':
                self.addItem(str(i) + ' - "' + NPC[i].name + '"')

        self.npcList.resize()
        self.npcList.repaint()

    def addItem(self, item):
        self.npcList.add(gui.Label(item), value=self._count)
        self._count += 1

    def clearList(self):
        self.npcList.clear()
        self.npcList.resize()
        self.npcList.repaint()
        self._count = 0

class OpenItemDialog(gui.Dialog):
    def __init__(self, engine, **params):
        self.engine = engine

        self._count = 0

        title = gui.Label("Choose Item")

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
        e = gui.Button('Choose item')
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
            self.engine.itemNum = listValue
            self.engine.selectDropItem(Item[listValue].name)
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


class NPCGeneralControl(gui.Table):
    def __init__(self, parent=None, **params):
        gui.Table.__init__(self, **params)

        self.parent = parent

        self.value = gui.Form()

        # dialogs
        openNpcDialog = OpenNPCDialog(self)

        self.tr()
        self.td(gui.Spacer(10, 70))

        self.tr()
        e = gui.Button("Open NPC...", width=100)
        e.connect(gui.CLICK, openNpcDialog.openDialog, None)
        self.td(e, colspan=2)

        self.tr()
        self.td(gui.Spacer(10, 10))

        self.tr()
        self.td(gui.Label('Name:', color=UI_FONT_COLOR), colspan=2)
        self.tr()
        self.td(gui.Input('', size=26, name='inpNpcName'), colspan=2, valign=-1)

        self.tr()
        self.td(gui.Spacer(10, 10))

        self.tr()
        self.td(gui.Label('Behaviour:', color=UI_FONT_COLOR), colspan=2)
        self.tr()
        e = gui.Select(name='selBehaviour')
        e.add('Attack on sight', 0)
        e.add('Attack when attacked', 1)
        e.add('Friendly', 2)
        e.add('Shopkeeper', 3)
        e.add('Guard', 4)
        e.value = 0
        #e.connect(gui.CHANGE, self.updateType, None)
        self.td(e, colspan=2)

        self.tr()
        self.td(gui.Spacer(10, 10))

        self.tr()
        self.lblSpawnSecs = gui.Label('Respawn rate: 0 secs', color=UI_FONT_COLOR)
        self.td(self.lblSpawnSecs, colspan=2)

        self.tr()
        e = gui.HSlider(value=5, min=5, max=120, size=10, width=120, name='selDataSpawnSecs')
        e.connect(gui.CHANGE, self.updateLabelSpawnSecs, e)
        self.td(e, colspan=2)

    def openNPC(self, npcNum):
        # pass it on to NPCEditorContainer
        self.parent.requestOpenNpc(npcNum)

    def updateLabelSpawnSecs(self, value):
        self.lblSpawnSecs.set_text('Respawn rate: ' + str(value.value) + ' secs')



class NPCCombatControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)

        self.value = gui.Form()

        # dialogs
        openItemDialog = OpenItemDialog(self)

        # item information
        self.itemNum = None
        self.itemVal = 0

        self.tr()
        self.td(gui.Label('Attack message:', color=UI_FONT_COLOR))
        self.tr()
        self.td(gui.Input('', size=26, name='inpNpcAttackSay'), valign=-1)

        self.tr()
        self.td(gui.Spacer(10, 20))

        self.tr()
        self.lblRan = gui.Label('Range: 0', color=UI_FONT_COLOR)
        self.td(self.lblRan)

        self.tr()
        e = gui.HSlider(value=0, min=0, max=20, size=10, width=120, name='selDataRan')
        e.connect(gui.CHANGE, self.updateLabelRan, e)
        self.td(e)

        self.tr()
        self.td(gui.Spacer(10, 20))

        self.tr()
        self.lblDropChance = gui.Label('Drop Chance: 0 (0%)', color=UI_FONT_COLOR)
        self.td(self.lblDropChance)

        self.tr()
        e = gui.HSlider(value=0, min=0, max=50, size=10, width=120, name='selDataDropChance')
        e.connect(gui.CHANGE, self.updateLabelDropChance, e)
        self.td(e)

        self.tr()
        self.td(gui.Spacer(10, 10))

        self.tr()
        self.lblDropItem = gui.Label('Drop Item: None', color=UI_FONT_COLOR)
        self.td(self.lblDropItem)

        self.tr()
        e = gui.Button("Choose item...", width=100)
        e.connect(gui.CLICK, openItemDialog.openDialog, None)
        self.td(e, colspan=2)

        self.tr()
        self.td(gui.Spacer(10, 10))

        self.tr()
        self.lblDropItemVal = gui.Label('Drop Item Value: 1', color=UI_FONT_COLOR)
        self.td(self.lblDropItemVal)

        self.tr()
        e = gui.HSlider(value=1, min=1, max=99, size=10, width=120, name='selDataDropItemVal')
        e.connect(gui.CHANGE, self.updateLabelDropItemVal, e)
        self.td(e)

    def updateLabelRan(self, value):
        self.lblRan.set_text('Range: ' + str(value.value))

    def updateLabelDropChance(self, value):
        if value.value != 0:
            self.lblDropChance.set_text('Drop Item Chance: ' + str(value.value) + ' (' + str(round(1./value.value*100, 1)) +'%)')

        else:
            self.lblDropChance.set_text('Drop Item Chance: 0 (0%)')

    def selectDropItem(self, value):
        self.lblDropItem.set_text('Drop Item: ' + str(value))

    def updateLabelDropItemVal(self, value):
        self.lblDropItemVal.set_text('Drop Item Value: ' + str(value.value))

class NPCStatsControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)

        self.value = gui.Form()

        self.tr()
        self.td(gui.Spacer(10, 20))

        self.tr()
        self.lblStr = gui.Label('Strength: 0', color=UI_FONT_COLOR)
        self.td(self.lblStr)

        self.tr()
        e = gui.HSlider(value=0, min=0, max=99, size=10, width=120, name='selDataStr')
        e.connect(gui.CHANGE, self.updateLabelStr, e)
        self.td(e)

        self.tr()
        self.td(gui.Spacer(10, 20))

        self.tr()
        self.lblDef = gui.Label('Defense: 0', color=UI_FONT_COLOR)
        self.td(self.lblDef)

        self.tr()
        e = gui.HSlider(value=0, min=0, max=99, size=10, width=120, name='selDataDef')
        e.connect(gui.CHANGE, self.updateLabelDef, e)
        self.td(e)

        self.tr()
        self.td(gui.Spacer(10, 20))

        self.tr()
        self.lblMag = gui.Label('Magic: 0', color=UI_FONT_COLOR)
        self.td(self.lblMag)

        self.tr()
        e = gui.HSlider(value=0, min=0, max=99, size=10, width=120, name='selDataMag')
        e.connect(gui.CHANGE, self.updateLabelMag, e)
        self.td(e)

        self.tr()
        self.td(gui.Spacer(10, 20))

        self.tr()
        self.lblSpd = gui.Label('Speed: 0', color=UI_FONT_COLOR)
        self.td(self.lblSpd)

        self.tr()
        e = gui.HSlider(value=0, min=0, max=99, size=10, width=120, name='selDataSpd')
        e.connect(gui.CHANGE, self.updateLabelSpd, e)
        self.td(e)

    def updateLabelStr(self, value):
        self.lblStr.set_text('Strength: ' + str(value.value))

    def updateLabelDef(self, value):
        self.lblDef.set_text('Defense: ' + str(value.value))

    def updateLabelMag(self, value):
        self.lblMag.set_text('Magic: ' + str(value.value))

    def updateLabelSpd(self, value):
        self.lblSpd.set_text('Speed: ' + str(value.value))


class NPCEditorContainer(gui.Container):
    def __init__(self, engine, **params):
        gui.Container.__init__(self, **params)

        self.engine = engine

        # item editor state
        self.npcNum = None

        # menus
        self.npcGeneralCtrl = NPCGeneralControl(parent=self, name='generalCtrl')
        self.npcCombatCtrl = NPCCombatControl(name='combatCtrl')
        self.npcStatsCtrl = NPCStatsControl(name='statsCtrl')

        # menu title
        self.tTitle = gui.Table(width=272, height=32)

        self.tTitle.tr()
        self.tTitle.td(gui.Label("NPC Editor", name='npcTitle', color=UI_FONT_COLOR))

        # buttons
        self.t = gui.Table(width=272, height=50)

        e = gui.Button("General", width=70)
        e.connect(gui.CLICK, self.toggleGeneral, None)
        self.t.td(e)

        e = gui.Button("Combat", width=70)
        e.connect(gui.CLICK, self.toggleCombat, None)
        self.t.td(e)

        e = gui.Button("Stats", width=70)
        e.connect(gui.CLICK, self.toggleStats, None)
        self.t.td(e)

        # content
        self.tContent = gui.Table(width=272, height=123)

        self.tContent.tr()
        self.tContent.td(self.npcGeneralCtrl, valign=-1)

        # bottom buttons
        self.tBottom = gui.Table(width=272, height=200)

        self.tBottom.tr()
        self.saveButton = gui.Button("Add NPC", width=100, height=40)
        self.saveButton .connect(gui.CLICK, self.saveNPC, None)
        self.tBottom.td(self.saveButton)

        e = gui.Button("Cancel", width=100, height=40)
        e.connect(gui.CLICK, self.cancel, None)
        self.tBottom.td(e)

        self.add(self.tTitle, 0, 0)
        self.add(self.t, 0, 48)
        self.add(self.tContent, 0, 100)
        self.add(self.tBottom, 0, 368)

    def requestOpenNpc(self, npcNum):
        # request edit npc
        g.tcpConn.sendEditNpc(npcNum)

    def openNPC(self, npcNum):
        # set general as default first menu
        self.toggleGeneral(None)

        # redraw selected npc sprite
        g.gameEngine.graphicsEngine.gameGUI.npcEditorGUI.selectedSpriteNum = NPC[npcNum].sprite
        g.gameEngine.graphicsEngine.gameGUI.npcEditorGUI.draw()

        # load npc variables
        self.npcGeneralCtrl.value['inpNpcName'].value = NPC[npcNum].name
        self.npcCombatCtrl.value['inpNpcAttackSay'].value = NPC[npcNum].attackSay 
        self.npcGeneralCtrl.value['selDataSpawnSecs'].value = NPC[npcNum].spawnSecs

        self.npcCombatCtrl.value['selDataDropChance'].value = NPC[npcNum].dropChance
        self.npcCombatCtrl.itemNum = NPC[npcNum].dropItem
        self.npcCombatCtrl.value['selDataDropItemVal'].value = NPC[npcNum].dropItemValue

        self.npcGeneralCtrl.value['selBehaviour'].value = NPC[npcNum].behaviour
        self.npcCombatCtrl.value['selDataRan'].value = NPC[npcNum].range
        self.npcStatsCtrl.value['selDataStr'].value = NPC[npcNum].stat[Stats.strength]
        self.npcStatsCtrl.value['selDataDef'].value = NPC[npcNum].stat[Stats.defense]
        self.npcStatsCtrl.value['selDataMag'].value = NPC[npcNum].stat[Stats.magic]
        self.npcStatsCtrl.value['selDataSpd'].value = NPC[npcNum].stat[Stats.speed]

        # change save button
        self.saveButton.value = 'Save NPC'

        # update npcNum
        self.npcNum = npcNum

    def updateType(self, value):
        print('todo')

    def saveNPC(self, value):
         # if it's a new NPC then find a new NPC id to use
        if self.npcNum is None:
            for i in range(len(NPC)):
                if NPC[i].name == '':
                    self.npcNum = i
                    break

        NPC[self.npcNum].name = self.npcGeneralCtrl.value['inpNpcName'].value
        NPC[self.npcNum].attackSay = self.npcCombatCtrl.value['inpNpcAttackSay'].value
        NPC[self.npcNum].sprite = g.gameEngine.graphicsEngine.gameGUI.npcEditorGUI.selectedSpriteNum
        NPC[self.npcNum].spawnSecs = self.npcGeneralCtrl.value['selDataSpawnSecs'].value

        NPC[self.npcNum].dropChance = self.npcCombatCtrl.value['selDataDropChance'].value
        NPC[self.npcNum].dropItem = self.npcCombatCtrl.itemNum
        NPC[self.npcNum].dropItemValue = self.npcCombatCtrl.value['selDataDropItemVal'].value

        NPC[self.npcNum].behaviour = self.npcGeneralCtrl.value['selBehaviour'].value
        NPC[self.npcNum].range = self.npcCombatCtrl.value['selDataRan'].value
        NPC[self.npcNum].stat[Stats.strength] = self.npcStatsCtrl.value['selDataStr'].value
        NPC[self.npcNum].stat[Stats.defense] = self.npcStatsCtrl.value['selDataDef'].value
        NPC[self.npcNum].stat[Stats.magic] = self.npcStatsCtrl.value['selDataMag'].value
        NPC[self.npcNum].stat[Stats.speed] = self.npcStatsCtrl.value['selDataSpd'].value

        # send the npc
        g.tcpConn.sendSaveNpc(self.npcNum)

        # quit editor
        self.quitEditor()

    def cancel(self, value):
        self.quitEditor()

    def quitEditor(self):
        # reset everything
        self.resetEditor()

        # quit
        g.gameEngine.graphicsEngine.gameGUI.setState(0)
        g.gameEngine.graphicsEngine.gameGUI.guiContainer.closeNpcEditor()
        g.editor = EDITOR_NONE
        g.canMoveNow = True

    def resetEditor(self):
        # set general as default first menu
        self.toggleGeneral(None)

        # redraw selected npc sprite
        g.gameEngine.graphicsEngine.gameGUI.npcEditorGUI.selectedSpriteNum = 0
        g.gameEngine.graphicsEngine.gameGUI.npcEditorGUI.draw()

        # load npc variables
        self.npcGeneralCtrl.value['inpNpcName'].value = ''
        self.npcCombatCtrl.value['inpNpcAttackSay'].value = ''
        self.npcGeneralCtrl.value['selDataSpawnSecs'].value = 5

        self.npcCombatCtrl.value['selDataDropChance'].value = 0
        self.npcCombatCtrl.itemNum = None
        self.npcCombatCtrl.value['selDataDropItemVal'].value = 0

        self.npcGeneralCtrl.value['selBehaviour'].value = 0
        self.npcCombatCtrl.value['selDataRan'].value = 0
        self.npcStatsCtrl.value['selDataStr'].value = 0
        self.npcStatsCtrl.value['selDataDef'].value = 0
        self.npcStatsCtrl.value['selDataMag'].value = 0
        self.npcStatsCtrl.value['selDataSpd'].value = 0

        # change save button
        self.saveButton.value = 'Add NPC'

        # update npcNum
        self.npcNum = None

    def hideAll(self):
        if self.tContent.find("generalCtrl"):
            self.tContent.remove(self.tContent.find("generalCtrl"))

        if self.tContent.find("combatCtrl"):
            self.tContent.remove(self.tContent.find("combatCtrl"))

        if self.tContent.find("statsCtrl"):
            self.tContent.remove(self.tContent.find("statsCtrl"))

    def toggleGeneral(self, value):
        self.engine.state = 0
        self.engine.draw()

        self.hideAll()
        self.tContent.tr()
        self.tContent.td(self.npcGeneralCtrl, valign=-1)

    def toggleCombat(self, value):
        self.engine.state = 1
        self.engine.draw()

        self.hideAll()
        self.tContent.tr()
        self.tContent.td(self.npcCombatCtrl, valign=-1)

    def toggleStats(self, value):
        self.engine.state = 2
        self.engine.draw()

        self.hideAll()
        self.tContent.tr()
        self.tContent.td(self.npcStatsCtrl, valign=-1)

class NPCEditorGUI():
    def __init__(self, surface):
        self.surface = surface

        self.state = 0

        # selected item sprite
        self.selectedSpriteNum = 0
        self.selectedSpriteSurface = pygame.Surface((2*PIC_X, 2*PIC_Y))
        self.selectedSpriteRect = pygame.Rect((616, 122, 64, 64))

        # scroll buttons
        # - scroll buttons (place them near self.selectedSpriteRect)
        btnScrollLeft = pygButton((600, 146, 32, 32), normal=g.dataPath + '/themes/default/hslider.left.tga')
        btnScrollRight = pygButton((680, 146, 32, 32), normal=g.dataPath + '/themes/default/hslider.right.tga')

        self.scrollButtons = (btnScrollLeft, btnScrollRight)

    def init(self):
        self.state = 0
        self.draw()

    def draw(self):
        g.gameEngine.graphicsEngine.gameGUI.reset()

        if self.state == 0:
            # update selected sprite surface
            tempImage = ResourceManager.plrSprites[self.selectedSpriteNum]
            pygame.draw.rect(self.selectedSpriteSurface, (0, 0, 0), (0, 0, 65, 75))
            self.selectedSpriteSurface.blit(tempImage, (0, 0), (0, 128, 64, 64))

            # render it onto the ui
            self.surface.blit(self.selectedSpriteSurface, self.selectedSpriteRect)

            # render all buttons
            self.drawElements()

    def drawElements(self):
        if self.state == 0:
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
            if self.selectedSpriteNum < len(ResourceManager.plrSprites)-1:
                self.selectedSpriteNum += 1

            self.draw()

import pygame
from pygame.locals import *
from pgu import gui

import pygUI as pygUI
from gamelogic import *
from network.database import *
from objects import *
from constants import *
import global_vars as g

from gui_mapeditor import MapEditorContainer, MapEditorGUI

# gui states
GUI_STATS = 0
GUI_INVENTORY = 1
GUI_EQUIPMENT = 2

GUI_MAPEDITOR = 3
GUI_ITEMEDITOR = 4
GUI_NPCEDITOR = 5
GUI_SPELLEDITOR = 6
GUI_SHOPEDITOR = 7

#TODO: get rid of g.canMoveNow...

class QuitDialog(gui.Dialog):
    def __init__(self, **params):
        title = gui.Label("Exit Game")

        t = gui.Table()

        t.tr()
        t.td(gui.Label("Are you sure you want to quit?"), colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        def btnQuit(value):
            g.gameEngine.quitGame()

        t.tr()
        e = gui.Button("Quit")
        e.connect(gui.CLICK, btnQuit, None)
        t.td(e)

        e = gui.Button("Cancel")
        e.connect(gui.CLICK, self.close, None)
        t.td(e)

        t.tr()
        t.td(gui.Spacer(10, 10))

        gui.Dialog.__init__(self, title, t)

class ChatControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)
        self.value = gui.Form()
        self.engine = None

        self._data = ''

        self._count = 1
        self.focused = False

        self.tr()
        self.chatMsg = gui.Input(maxlength=44, width=468, focusable=False)
        self.chatMsg.connect(gui.KEYDOWN, self.lkey)
        self.td(self.chatMsg)

        self.tr()
        self.chatList = gui.Table()
        self.box = gui.ScrollArea(self.chatList, width=480, height=172, hscrollbar=False)
        self.td(self.box)

        self.tr()
        class Hack(gui.Spacer):
            def __init__(self, box):
                super(gui.Spacer, self).__init__()
                self.box = box

            def resize(self, width=None, height=None):
                self.box.set_vertical_scroll(65535)
                return 1, 1

        dirtyHack = Hack(self.box)
        self.td(dirtyHack)

    def lkey(self, _event):
        e = _event

        if e.key == K_RETURN:
            if self.chatMsg.value != '':
                handleMsg(self.chatMsg.value)
                self.chatMsg.value = ''

                g.canMoveNow = True

    def addText(self, text, color=(0, 0, 0)):
        self.chatList.tr()
        self.chatList.td(gui.Label(str(text), color=color), align=-1)
        self.box.resize()

    def clearChat(self):
        print "todo"


class uiContainer(gui.Container):
    def __init__(self, engine, **params):
        gui.Container.__init__(self, **params)

        self.engine = engine


        # menu title
        self.tTitle = gui.Table(width=272, height=32)

        # navigation
        self.tBottom = gui.Table(width=272, height=200)

        self.tBottom.tr()
        e = gui.Button("Stats", width=100, height=40)
        e.connect(gui.CLICK, self.toggleStats, None)
        self.tBottom.td(e)
        e = gui.Button("Inventory", width=100, height=40)
        e.connect(gui.CLICK, self.toggleInventory, None)
        self.tBottom.td(e)

        self.tBottom.tr()
        e = gui.Button('Equipment', width=100, height=40)
        e.connect(gui.CLICK, self.toggleEquipment, None)
        self.tBottom.td(e)
        e = gui.Button('Spellbook', width=100, height=40)
        e.connect(gui.CLICK, self.toggleSpellbook, None)
        self.tBottom.td(e)

        self.tBottom.tr()
        e = gui.Button('Settings', width=100, height=40)
        e.connect(gui.CLICK, self.toggleSettings, None)
        self.tBottom.td(e, colspan=2)

        self.add(self.tTitle, 0, 0)
        self.add(self.tBottom, 0, 368)

        # default UI view, todo
        #self.toggleStats()

    def toggleStats(self, value=0):
        self.engine.setState(GUI_STATS)

        plrName = getPlayerName(g.myIndex)
        plrLevel = getPlayerLevel(g.myIndex)

        if plrLevel == None:
            plrLevel = 1

        self.updateTitle(plrName + ', level ' + str(plrLevel))

    def toggleInventory(self, value):
        self.engine.setState(GUI_EQUIPMENT)
        self.updateTitle('Inventory')

    def toggleEquipment(self, value):
        self.engine.setState(GUI_STATS)
        self.updateTitle('Equipment')

    def toggleSpellbook(self, value):
        self.engine.setState(GUI_STATS)
        self.updateTitle('Spellbook')

    def toggleSettings(self, value):
        self.engine.setState(GUI_STATS)
        self.updateTitle('Settings')

    def updateTitle(self, title, titleColor=(251, 230, 204)):
        if self.tTitle.find('uiTitle'):
            self.tTitle.remove(self.tTitle.find('uiTitle'))

        self.tTitle.tr()
        self.tTitle.td(gui.Label(title, name='uiTitle', color=titleColor))


class GUIContainer(gui.Container):
    def __init__(self, engine, **params):
        gui.Container.__init__(self, **params)

        self.engine = engine

        self.chatCtrl = ChatControl(name="chatCtrl")
        self.uiCtrl = uiContainer(self.engine, name="uiCtrl")
        self.mapEditorControl = MapEditorContainer(self.engine.mapEditorGUI, name="mapEditorCtrl")

        # default controls
        self.add(self.chatCtrl, 16, 384)
        self.add(self.uiCtrl, 512, 16)

    def openEditor(self, value=0):
        self.add(self.mapEditorControl, 512, 16)
        g.canMoveNow = False

        # close ui
        self.remove(self.find("uiCtrl"))

    def closeEditor(self, value=0):
        self.remove(self.find("mapEditorCtrl"))

        # add ui
        self.add(self.uiCtrl, 512, 16)

    def updateEngines(self):
        # dirty hack
        self.uiCtrl.engine = self.engine


class GameGUI():
    def __init__(self, graphicsEngine):
        self.graphicsEngine = graphicsEngine
        self.state = GUI_STATS

        self.background = pygame.image.load(g.dataPath + '/gui/game_background.png')
        g.guiSurface.blit(self.background, (0, 0))

        # events
        self.pressedKeys = []

        # game GUIs
        self.mapEditorGUI = MapEditorGUI(g.guiSurface)

        # input fields (TODO: dont hardcode placement)
        self.inpChat = pygUI.pygInputField((16, 384, 480, 20), "", 40, (255, 255, 255))
        self.inpChat.restricted = '\'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\\\'()*+,-./:;<=>?@[\]^_`{|}~\''
        self.listLog = pygUI.pygList((16, 420, 480, 164), (255, 255, 255))

        # TEMPORARY: MAP EDITOR
        self.label1 = pygUI.pygLabel((544, 150, 20, 20), "Selected tile:")

        # GUI
        self.app = gui.App()

        self.guiContainer = GUIContainer(self, align=-1, valign=-1)
        self.guiContainer.updateEngines()

        self.app.init(self.guiContainer)

        # dialogs
        self.quitDialog = QuitDialog()

        # dirty
        self.isDirty = True

    def setState(self, state):
        self.state = state
        self.reset()

    def draw(self, surface, surfaceRect):
        # surface and surfaceRect is a part of a stupid hack. See graphics.py

        # render ui
        if self.isDirty:
            self.drawUI()
            # todo: check for isDirty, currently set to True at all times
            self.isDirty = True

        # part of the hack. game map is blitted so that the gui (app.paint) is ABOVE the game screen
        g.screenSurface.blit(surface, surfaceRect)

        # render gui
        self.app.paint()

    def update(self, event):
        self.app.event(event)

        if event.type == KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.guiContainer.chatCtrl.focused == False:
                    self.guiContainer.chatCtrl.chatMsg.focus()
                    self.guiContainer.chatCtrl.focused = True
                    g.canMoveNow = False
                elif self.guiContainer.chatCtrl.focused == True:
                    self.guiContainer.chatCtrl.chatMsg.blur()
                    self.guiContainer.chatCtrl.focused = False
                    g.canMoveNow = True

            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                if not self.quitDialog.is_open():
                    self.quitDialog.open()

        if self.state == GUI_MAPEDITOR:
            self.mapEditorGUI.update(event)

    ##############
    # INTERFACES #
    ##############

    def reset(self):
        ''' resets the whole surface '''
        g.guiSurface.blit(self.background, (0, 0))
        self.drawUI()

    def drawUI(self):
        if self.state == GUI_STATS:
            self.drawStats()

        elif self.state == GUI_EQUIPMENT:
            self.drawHealthBar()
            self.drawManaBar()

        elif self.state == GUI_MAPEDITOR:
            self.mapEditorGUI.drawElements()

        g.screenSurface.blit(g.guiSurface, (0, 0))

    def drawStats(self):
        ''' the stats interface '''
        self.drawHealthBar()
        self.drawManaBar()
        self.drawStatText()

    def drawInventory(self):
        ''' the inventory interface '''
        self.drawManaBar()

    #############
    # FUNCTIONS #
    #############

    def drawStatText(self):
        font = pygame.font.SysFont('monospace', 15)
        fontColor = (251, 230, 204)

        label = font.render('STR - ' + str(getPlayerStat(g.myIndex, Stats.strength)), 0, fontColor)
        labelRect = label.get_rect()
        labelRect.centerx = 590
        labelRect.centery = 150
        g.guiSurface.blit(label, labelRect)

        label = font.render('DEF - ' + str(getPlayerStat(g.myIndex, Stats.defense)), 0, fontColor)
        labelRect = label.get_rect()
        labelRect.centerx = 590
        labelRect.centery = 170
        g.guiSurface.blit(label, labelRect)

        label = font.render('SPD - ' + str(getPlayerStat(g.myIndex, Stats.speed)), 0, fontColor)
        labelRect = label.get_rect()
        labelRect.centerx = 705
        labelRect.centery = 150
        g.guiSurface.blit(label, labelRect)

        label = font.render('MAG - ' + str(getPlayerStat(g.myIndex, Stats.magic)), 0, fontColor)
        labelRect = label.get_rect()
        labelRect.centerx = 705
        labelRect.centery = 170
        g.guiSurface.blit(label, labelRect)

    def drawHealthBar(self):
        emptyBarSurface = pygame.image.load(g.dataPath + '/gui/bar_empty.png').convert_alpha()
        redBarSurface = pygame.image.load(g.dataPath + '/gui/bar_red.png').convert_alpha()

        pos = (544, 75)
        healthBarWidth = 208*Player[g.myIndex].vitals[Vitals.hp]/Player[g.myIndex].maxHP
        g.guiSurface.blit(emptyBarSurface, pos)
        g.guiSurface.blit(redBarSurface, pos, (0, 0, healthBarWidth, 28))

    def drawManaBar(self):
        emptyBarSurface = pygame.image.load(g.dataPath + '/gui/bar_empty.png').convert_alpha()
        blueBarSurface = pygame.image.load(g.dataPath + '/gui/bar_blue.png').convert_alpha()

        pos = (544, 100)
        manaBarWidth = 208*Player[g.myIndex].vitals[Vitals.mp]/Player[g.myIndex].maxMP
        g.guiSurface.blit(emptyBarSurface, pos)
        g.guiSurface.blit(blueBarSurface, pos, (0, 0, manaBarWidth, 28))

    def drawEquipment(self):
        emptyBarSurface = pygame.image.load(g.dataPath + '/gui/bar_empty.png').convert_alpha()
        blueBarSurface = pygame.image.load(g.dataPath + '/gui/bar_blue.png').convert_alpha()

        pos = (544, 150)
        manaBarWidth = 208*Player[g.myIndex].vitals[Vitals.mp]/Player[g.myIndex].maxMP
        g.guiSurface.blit(emptyBarSurface, pos)
        g.guiSurface.blit(blueBarSurface, pos, (0, 0, manaBarWidth, 28))

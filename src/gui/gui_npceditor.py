import pygame
from pygame.locals import *
from pgu import gui
import pygUI as pygUI

from objects import NPC
from constants import *
import global_vars as g

class NPCEditorContainer(gui.Container):
    def __init__(self, engine, **params):
        gui.Container.__init__(self, **params)

        self.engine = engine
        self.value = gui.Form()

        # item editor state
        self.itemNum = None

        # dialogs

        # menu title
        self.tTitle = gui.Table(width=272, height=32)

        self.tTitle.tr()
        self.tTitle.td(gui.Label("NPC Editor", name='npcTitle', color=UI_FONT_COLOR))

        # content
        self.tContent = gui.Table(width=272, height=123)

        self.tContent.tr()


        self.tContent.tr()
        self.tContent.td(gui.Label('Name:', color=UI_FONT_COLOR), colspan=2)
        self.tContent.tr()
        self.tContent.td(gui.Input('', size=26, name='inpNpcName'), colspan=2, valign=-1)

        self.tContent.tr()
        self.tContent.td(gui.Label('Behaviour:', color=UI_FONT_COLOR), colspan=2)
        self.tContent.tr()
        e = gui.Select(name='selBehaviour')
        e.add('Attack on sight', 0)
        e.add('Attack when attacked', 1)
        e.add('Friendly', 2)
        e.add('Shopkeeper', 3)
        e.add('Guard', 4)
        e.value = 0
        e.connect(gui.CHANGE, self.updateType, None)
        self.tContent.td(e, colspan=2)

        # data input
        self.tData = gui.Table(width=272, height=75)

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
        self.add(self.tContent, 0, 100)
        self.add(self.tData, 0, 255)
        self.add(self.tBottom, 0, 368)

    def openNPC(self, itemNum):
        print 'todo'

    def hideAll(self):
        if self.tData.find("dataEquipment"):
            self.tData.remove(self.tData.find("dataEquipment"))

        if self.tData.find("dataPotion"):
            self.tData.remove(self.tData.find("dataPotion"))

        if self.tData.find("dataSpell"):
            self.tData.remove(self.tData.find("dataSpell"))

    def updateType(self, value):
        print 'todo'

    def saveNPC(self, value):
        print 'todo'

        # quit editor
        self.quitEditor()

    def cancel(self, value):
        self.quitEditor()

    def quitEditor(self):
        # reset everything
        self.resetEditor()

        # quit
        g.gameEngine.graphicsEngine.gameGUI.setState(0)
        g.gameEngine.graphicsEngine.gameGUI.guiContainer.closeItemEditor()
        g.editor = EDITOR_NONE
        g.canMoveNow = True

    def resetEditor(self):
        print 'todo'

class NPCEditorGUI():
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
        tempImage = pygame.image.load(g.dataPath + '/sprites/' + str(self.selectedSpriteNum) + '.bmp').convert()
        self.selectedSpriteSurface.blit(tempImage, (0, 0), (96, 0, 32, 32))

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
            if self.selectedSpriteNum < 16:
                self.selectedSpriteNum += 1

            self.draw()

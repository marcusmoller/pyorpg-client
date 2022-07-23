import sys
import pygame
from pygame.locals import *
from pgu import gui
from twisted.internet import reactor

import global_vars as g
from objects import *
from constants import *

import gui.python_gui as pygUI
from gui.dialogs import alertMessageDialog

class newCharControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)
        self.value = gui.Form()
        self.engine = None

        def btnNextClass(btn):
            self.engine.classIndex += 1
            self.engine.updateClassSelection()

        def btnPrevClass(btn):
            self.engine.classIndex -= 1
            self.engine.updateClassSelection()

        def btnCreateChar(btn):
            self.engine.createCharacter()

        def btnCancel(btn):
            g.gameState = MENU_CHAR

        self.tr()
        self.lblCharName = gui.Label(_('Character Name'), color=(255, 255, 255))
        self.td(self.lblCharName, colspan=3, valign=1)

        self.tr()
        self.inpCharName = gui.Input(name='inpCharName', value='')
        self.td(self.inpCharName, colspan=3)

        self.tr()
        self.lblClassName = gui.Label(_('CLASS NAME'), color=(255, 255, 255))
        self.td(self.lblClassName, colspan=3, valign=1)

        self.tr()
        btn = gui.Button(_("Previous"), width=160, height=40)
        btn.connect(gui.CLICK, btnPrevClass, None)
        self.td(btn)
        self.td(gui.Spacer(300, 160))
        btn = gui.Button(_("Next"), width=160, height=40)
        btn.connect(gui.CLICK, btnNextClass, None)
        self.td(btn)

        self.tr()
        self.td(gui.Spacer(0, 0))
        self.btnSelChar = gui.Button(_("Create Character"), width=160, height=30)
        self.btnSelChar.connect(gui.CLICK, btnCreateChar, None)
        self.td(self.btnSelChar)
        self.td(gui.Spacer(0, 0))

        self.tr()
        self.td(gui.Spacer(0, 20))

        self.tr()
        self.td(gui.Spacer(0, 0))
        btn = gui.Button("Cancel", width=160, height=30)
        btn.connect(gui.CLICK, btnCancel, None)
        self.td(btn)
        self.td(gui.Spacer(0, 0))

class menuNewCharacter():
    def __init__(self, surface):
        self.surface = surface
        self.x = 10
        self.y = 10

        self.backgroundImage = pygame.image.load(g.dataPath + '/gui/bg_menu.png')

        # class selection
        self.classIndex = 0

        # - statistics
        self.labelInfoStats = pygUI.pygLabel((544, 50, 256, 20), _("Class Statistics"), align=pygUI.ALIGN_CENTER)

        self.labelHP = pygUI.pygLabel((544, 70, 10, 10), "HP: ")
        self.labelMP = pygUI.pygLabel((544, 90, 10, 10), "MP: ")
        self.labelSP = pygUI.pygLabel((544, 110, 10, 10), "SP: ")

        self.labelStr = pygUI.pygLabel((544, 150, 10, 10), "Strength: ")
        self.labelDef = pygUI.pygLabel((544, 170, 10, 10), "Defense:")
        self.labelSpd = pygUI.pygLabel((544, 190, 10, 10), "Speed:")
        self.labelMag = pygUI.pygLabel((544, 210, 10, 10), "Magic:")

        self.labels = (self.labelInfoStats, self.labelHP, self.labelMP, self.labelSP, self.labelStr, self.labelDef, self.labelSpd, self.labelMag)

        # sprite image
        self.spriteScale = 2
        self.spriteImage = pygame.Surface((2*PIC_X * self.spriteScale, 2*PIC_Y * self.spriteScale))
        self.spriteImageRect = self.spriteImage.get_rect()
        self.spriteImageRect.centerx = 800/2
        self.spriteImageRect.centery = 600/2 - 20

        # GUI
        self.app = gui.App()

        self.charControl = newCharControl()
        self.charControl.engine = self

        self.c = gui.Container(align=0, valign=0)
        self.c.add(self.charControl, 0, 0)

        self.app.init(self.c)

    def draw(self):
        # background
        self.surface.blit(self.backgroundImage, (0, 0))
        self.surface.blit(self.spriteImage, self.spriteImageRect)

        self.app.paint()

        for label in self.labels:
            label.draw(self.surface)

        pygame.display.update()

    def _handleEvents(self, event):
        # keyboard shortcuts
        self.app.event(event)

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            g.gameState = MENU_CHAR

    def isStringLegal(self, string):
        restricted = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

        for i in range(len(string)):
            if string[i] not in restricted:
                alertMessageDialog(msg=_('The name is not valid! The name may only contain a-z and 0-9.'), title=_('An error occured'))
                return False

        return True

    def createCharacter(self):
        name = self.charControl.inpCharName.value

        if len(name) >= 3:
            if self.isStringLegal(name):
                g.tcpConn.sendAddChar(name, "male", self.classIndex, (g.gameEngine.menuChar.charIndex-1))
                g.gameEngine.setState(MENU_CHAR)

    def updateClassSelection(self):
        if self.classIndex > (g.maxClasses-1):
            self.classIndex = 0
        elif self.classIndex < 0:
            self.classIndex = (g.maxClasses-1)

        self.charControl.lblClassName.set_text(Class[self.classIndex].name)

        self.labelHP.setText("HP: " + str(Class[self.classIndex].vital[Vitals.hp]))
        self.labelMP.setText("MP: " + str(Class[self.classIndex].vital[Vitals.mp]))
        self.labelSP.setText("SP: " + str(Class[self.classIndex].vital[Vitals.sp]))

        self.labelStr.setText("Strength: " + str(Class[self.classIndex].stat[Stats.strength]))
        self.labelDef.setText("Defense: " + str(Class[self.classIndex].stat[Stats.defense]))
        self.labelSpd.setText("Speed: " + str(Class[self.classIndex].stat[Stats.speed]))
        self.labelMag.setText("Magic: " + str(Class[self.classIndex].stat[Stats.magic]))

        self.updateCharSprite(Class[self.classIndex].sprite)

    def updateCharSprite(self, sprite):
        tempImage = pygame.image.load(g.dataPath + "/sprites/" + str(sprite) + ".png").convert_alpha()
        tempSprite = pygame.Surface((64, 64))

        tempSprite.blit(tempImage, (0, 0), (0, 128, 64, 64))

        self.spriteImage = pygame.transform.scale(tempSprite, (2*PIC_X * self.spriteScale, 2*PIC_Y * self.spriteScale))
        self.spriteImage.set_colorkey((0, 0, 0))


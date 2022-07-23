#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import pygame
from pygame.locals import *
import configparser

from twisted.internet import reactor

import global_vars as g
from resourcemanager import ResourceManager

from gamelogic import *
from graphics import *
from sound import SoundEngine
from gui.gui import *
from menu.menulogin import menuLogin
from menu.menuregister import menuRegister
from menu.menuchar import menuCharacters
from menu.menunewchar import menuNewCharacter
from objects import *
from network.client import *
from network.database import *


class Engine:
    def __init__(self):
        self.FRAMES_PER_SECOND = 20

        # menus
        self.menuLogin = menuLogin(g.screenSurface)
        self.menuRegister = menuRegister(g.screenSurface)
        self.menuChar = menuCharacters(g.screenSurface)
        self.menuNewChar = menuNewCharacter(g.screenSurface)

        self.graphicsEngine = GraphicsEngine()

        self.tmr25 = 0
        self.tmr1000 = 0
        self.walkTimer = 0
        self.clockTick = 0

    def init(self):
        ResourceManager.loadEverything()
        g.soundEngine = SoundEngine()
        g.soundEngine.loadSounds()

        self.initConfig(g.dataPath + '/config.cfg')

        self.setState(MENU_LOGIN)

        pygame.display.flip()
        self.gameLoop()
        reactor.run()

    def initConnection(self):
        ''' starts the connection to the server '''
        connectionProtocol = startConnection()
        g.tcpConn = TCPConnection(connectionProtocol)

    def initConfig(self, configFile):
        ''' reads the configuration file '''

        if not os.path.isfile(configFile):
            print('No configuration file was found')
            return

        config = configparser.RawConfigParser()
        config.read(configFile)

        try:
            if config.getboolean('sound', 'sfx') is False:
                g.soundEngine.sfxMuted = True

            if config.getboolean('sound', 'music') is False:
                g.soundEngine.musicMuted = True
        except:
            print('An error occured while reading the configuration file')

    def disconnect(self):
        g.connector.disconnect()

    def setState(self, state):
        ''' sets the game state '''
        if state == MENU_LOGIN:
            g.gameState = MENU_LOGIN
            g.soundEngine.play(SOUND_OPENING, True, True)

        elif state == MENU_REGISTER:
            g.gameState = MENU_REGISTER

        elif state == MENU_CHAR:
            g.gameState = MENU_CHAR

        elif state == MENU_NEWCHAR:
            g.gameState = MENU_NEWCHAR

        elif state == MENU_INGAME:
            g.gameState = MENU_INGAME
            g.soundEngine.play(SOUND_TOWN, True, True)

    def gameLoop(self, FPS=25):
        ''' the main loop of the game '''
        # TODO: DIRTY AREAS
        if g.gameState == MENU_LOGIN:
            self.menuLogin.draw()

        elif g.gameState == MENU_REGISTER:
            self.menuRegister.draw()

        elif g.gameState == MENU_CHAR:
            self.menuChar.draw()

        elif g.gameState == MENU_NEWCHAR:
            self.menuNewChar.draw()

        elif g.gameState == MENU_INGAME:
            # todo: dirty areas

            if g.inGame:
                self.clockTick = time.time() * 1000 # convert to ms

                if self.tmr25 < self.clockTick:
                    self.checkInputKeys()

                    if g.canMoveNow:
                        # check if player is trying to move
                        checkMovement()
                        # check if player is trying to attack
                        checkAttack()

                    self.tmr25 = self.clockTick + 25

                # process movements
                if self.walkTimer < self.clockTick:
                    for i in range(0, len(g.playersOnMap)):
                        if Player[g.playersOnMap[i]].moving > 0:
                            processMovement(g.playersOnMap[i])

                    #for i in range(g.npcHighIndex):
                    for i in range(0, MAX_MAP_NPCS):
                        if Map.npc[i] != None:
                            if mapNPC[i].moving > 0:
                                processNPCMovement(i)

                    self.walkTimer = self.clockTick + 30

                self.graphicsEngine.renderGraphics()

            # flip graphics
            pygame.display.update()
            #pygame.display.update(self.graphicsEngine.dirtyRects)

        pygame.event.pump()
        for event in pygame.event.get():
            # todo: organize this better...
            if g.gameState == MENU_LOGIN:
                self.menuLogin._handleEvents(event)

            elif g.gameState == MENU_REGISTER:
                self.menuRegister._handleEvents(event)

            elif g.gameState == MENU_CHAR:
                self.menuChar._handleEvents(event)

            elif g.gameState == MENU_NEWCHAR:
                self.menuNewChar._handleEvents(event)

            elif g.gameState == MENU_INGAME:
                self.graphicsEngine.gameGUI.update(event)

            if event.type == pygame.QUIT:
                reactor.stop()
                pygame.quit()

            elif event.type == pygame.MOUSEMOTION:
                self.handleMouse(event)

        # make it loop
        reactor.callLater(1./FPS, self.gameLoop)

    def quitGame(self):
        ''' called when quitting the game '''
        if g.tcpConn != None:
            # if connected to server, send quit msg
            g.tcpConn.sendQuit()

        reactor.stop()
        pygame.quit()


    ##################
    # INPUT SPECIFIC #
    #################

    def checkInputKeys(self):
        ''' checks for input events '''
        def pressed(key):
            keys = pygame.key.get_pressed()

            if keys[key]:
                return True
            else:
                return False

        if pressed(pygame.K_UP) or pressed(pygame.K_w):
            g.inpDIR_UP = True
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = False

        elif pressed(pygame.K_DOWN) or pressed(pygame.K_s):
            g.inpDIR_UP = False
            g.inpDIR_DOWN = True
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = False

        elif pressed(pygame.K_LEFT) or pressed(pygame.K_a):
            g.inpDIR_UP = False
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = True
            g.inpDIR_RIGHT = False

        elif pressed(pygame.K_RIGHT) or pressed(pygame.K_d):
            g.inpDIR_UP = False
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = True

        elif pressed(pygame.K_LSHIFT) or pressed(pygame.K_RSHIFT):
            g.inpDIR_UP = False
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = False
            g.inpSHIFT = True
            g.inpCTRL = False

        elif pressed(pygame.K_LCTRL) or pressed(pygame.K_RCTRL):
            g.inpDIR_UP = False
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = False
            g.inpSHIFT = False
            g.inpCTRL = True

        elif pressed(pygame.K_RETURN):
            checkMapGetItem()

        else:
            g.inpDIR_UP = False
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = False
            g.inpSHIFT = False
            g.inpCTRL = False

        # check hotkeys
        for key in g.SPELLBOOK_HOTKEYS.keys():
            if pressed(key):
                spellNum = getSpellbookHotkey(key)

                if spellNum is not None:
                    castSpell(spellNum)

    def handleMouse(self, event):
        g.cursorX = event.pos[0]
        g.cursorY = event.pos[1]

        # only set mouse tile position within game screen boundaries
        if g.cursorX > 16 and g.cursorX < (16 + 15*PIC_X):
            g.cursorXTile = (g.cursorX - 16) // PIC_X

        if g.cursorY > 16 and g.cursorY < (16 + 11*PIC_Y):
            g.cursorYTile = (g.cursorY - 16) // PIC_Y

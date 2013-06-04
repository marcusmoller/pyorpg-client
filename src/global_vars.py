#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import pygame
from pygame.locals import *

pygame.init()

# TCPconnection (CClientTCP)
gameEngine = None
tcpConn = None

# player variables
myIndex = None

# main gameloop
inGame = False
isLogging = True
gameState = 0
connectionStatus = ""

canMoveNow = True

editor = None

# Input (modInput.bas)
inpDIR_UP = False
inpDIR_DOWN = False
inpDIR_LEFT = False
inpDIR_RIGHT = False

# used for improved looping
highIndex = 0
playersOnMapHighIndex = 0
playersOnMap = []

# used for draggin picture boxes
sOffsetX = 0
sOffestY = 0

# freeze controls when getting map
gettingMap = False

# mouse tile location
cursorX = 0
cursorY = 0

# maximum classes
maxClasses = 0

dataPath = os.path.join('..', 'data')

# --------------------

# GENERAL
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# SDL
screenSurface = None

gameSurface = pygame.Surface((480, 352))
bgSurface = None

guiSurface = pygame.Surface((800, 600))

# SURFACE SPECIFIC
gameSurfaceXOffset = 0    # 800 - (32*15) MAEMO
gameSurfaceYOffset = 0

guiSurfaceXOffset = 0
guiSurfaceYOffset = 0

clock = pygame.time.Clock()

# FONT
nameFont = pygame.font.SysFont("Fixedsys", 14)

# TILES
tileDimension = 32

# TEMPORARY (!!!)
argUsername = None
argPassword = None

# map
mapNames = []

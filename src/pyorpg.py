#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import getopt
import pygame
from pygame.locals import *

import global_vars as g
from constants import *

pygame.display.set_caption(GAME_NAME)
g.screenSurface = pygame.display.set_mode((g.SCREEN_WIDTH, g.SCREEN_HEIGHT))

import engine

if __name__ == "__main__":
    g.gameEngine = engine.Engine()
    g.gameEngine.init()
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import getopt
import argparse
import pygame
from pygame.locals import *

import engine
import global_vars as g
from constants import *

parser = argparse.ArgumentParser(prog='PyORPG')
parser.add_argument('-ip', help='connect to server on ip')
parser.add_argument('-p', help='connect to server on port')
parser.add_argument('--no-sound', help='disables sound', action='store_false')
args = vars(parser.parse_args())

if args['ip'] != None:
    print "ip todo"

pygame.display.set_caption(GAME_NAME)
g.screenSurface = pygame.display.set_mode((g.SCREEN_WIDTH, g.SCREEN_HEIGHT))

if __name__ == "__main__":
    g.gameEngine = engine.Engine()
    g.gameEngine.init()
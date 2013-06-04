#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    File: CSprites.py
    
    MSPython is a RPG written in Python using PyGame.
    Copyright (C) 2011  Marcus Møller

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    This file holds the game sprites.
"""

import pygame
from pygame.locals import *

import global_vars as g

from data import *

# LOOK AT BOTTOM FOR CONSTANTS

class CharSprite(pygame.sprite.Sprite):
    """Sprite for animated NPCs and class for Player"""
    #            N  S  W   E
    DX = [None,  0, 0, -1, 1]
    DY = [None, -1, 1,  0, 0]
    
    isPlayer = False
    
    def __init__(self, pos=(0, 0), spriteID=1):
        super(CharSprite, self).__init__()
        
        self.frames = self.loadSpriteFrames(spriteID)
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.animation = self.standAnim()
        self.pos = pos

        self.dx = 0
        self.dy = 0
        
        # CONSTANTS
        self.DIR_UP = 1
        self.DIR_DOWN = 2
        self.DIR_LEFT = 3
        self.DIR_RIGHT = 4
        
        self._direction = self.DIR_DOWN

    def _getX(self):
        return self.rect.x/32

    def _getY(self):
        return self.rect.y/32

    def _setX(self, x):
        self.rect.x = x*32

    def _setY(self, y):
        self.rect.y = y*32
        
    def _getPos(self):
        """Check the current position of the sprite on the map."""

        return ((self.rect.x)/32), ((self.rect.y)/32)

    def _setPos(self, pos):
        """Set the position and depth of the sprite on the map."""

        self.rect.x = pos[0]*32
        self.rect.y = pos[1]*32
        
    pos = property(_getPos, _setPos)

        
    def draw(self):
        g.gameSurface.blit(self.image, (self.rect[0], self.rect[1]))
        
    def update(self, *args):
        self.image = self.frames[self._direction]
        #self.animation.next()
        
    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]
        
    def standAnim(self):
        while True:
            """Change to next frame every two ticks"""
            for frame in self.frames:
                self.image = frame
                yield None
                yield None
        
    def loadSpriteFrames(self, row):
        images = loadSlicedSprites(32, 32, row, "Sprites.png")
        return images
    
    #############
    # FUNCTIONS #
    #############
    
    def doTeleport(self, x, y):
        self.pos = (int(x), int(y))
        print "Teleported player to destination: (" + x + ", " + y + ")"
                  
class PlayerSprite(CharSprite):
    isPlayer = True
    
    def __init__(self, pos=(5, 5)):   
        CharSprite.__init__(self, pos, 10)
        
        self.animation = None
        self.image = self.frames[self._direction]
        
    def walkAnim(self):
        for frame in range(4):
            if frame == 3:
                frame = 0
            
            self.image = self.frames[frame + ((self._direction * 3) - 3)]
            
            yield None
            self.move(4*self.DX[self._direction], 4*self.DY[self._direction])
            yield None
            self.move(4*self.DX[self._direction], 4*self.DY[self._direction])
            
            
    def update(self, *args):
        if self.animation is None:
            self.image = self.frames[(self._direction * 3) - 2]
        else:
            try:
                self.animation.next()
            except StopIteration:
                self.animation = None
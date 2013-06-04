#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, pygame
from pygame.locals import *

def loadImage(filename):
    try:
        image = pygame.image.load(filename).convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
    except pygame.error:
        raise SystemExit, "Unable to load: " + filename
    return image.convert_alpha()
    
def loadSlicedSprites(w, h, row, filename):
    images = []
    masterImage = pygame.image.load(filename).convert_alpha()
    
    masterWidth, masterHeight = masterImage.get_size()
    
    '''for i in xrange(int(masterHeight/h)):
        for j in xrange(int(masterWidth/w)):
            images.append(masterImage.subsurface((j*w, i*h, w, h)))'''
    
    for i in xrange(int(masterWidth/w)):
        images.append(masterImage.subsurface((i*w, row*h , w, h)))
    
    return images

def loadTileTable(filename, w, h):
    image = pygame.image.load(filename).convert_alpha()
    imageWidth, imageHeight = image.get_size()
    tileTable = []
    
    for tile_x in range(0, imageWidth/w):
        line = []
        tileTable.append(line)
        for tile_y in range(0, imageHeight/h):
            rect = (tile_x*w, tile_y*h, w, h)
            line.append(image.subsurface(rect))
    return tileTable

def loadSlicedSprites2(w, h, filename):
    images = []
    masterImage = pygame.image.load(filename).convert_alpha()
    
    masterWidth, masterHeight = masterImage.get_size()
    
    for i in xrange(int(masterHeight/h)):
        for j in xrange(int(masterWidth/w)):
            images.append(masterImage.subsurface((j*w, i*h, w, h)))
    
    return images
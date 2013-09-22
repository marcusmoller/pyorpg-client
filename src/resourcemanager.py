import pygame
import os

import global_vars as g

class ResourceManagerClass():
    def __init__(self):
        self.backgrounds = []
        self.plrSprites = []
        self.tileSprites = []
        self.itemSprites = []
        self.spellSprites = []

    def getAmountOfFiles(self, folder, fileExtension):
        amount = 0
        for file in os.listdir(g.dataPath + '/' + folder):
            if file.endswith(fileExtension):
                amount += 1

        return amount

    def loadImage(self, image):
        if image.endswith('.bmp'):
            tempImage = pygame.image.load(image).convert()
            tempImage.set_colorkey((0, 0, 0)) # set black color to transparent
            return tempImage

        elif image.endswith('.png'):
            return pygame.image.load(image).convert_alpha()

    def loadEverything(self):
        self.loadPlrSprites()
        self.loadItems()
        self.loadSpells()

    def loadPlrSprites(self):
        amount = self.getAmountOfFiles('sprites', '.png')

        for i in range(amount):
            try:
                self.plrSprites.append(self.loadImage(g.dataPath + '/sprites/' + str(i) + '.png'))
            except:
                break

    def loadItems(self):
        amount = self.getAmountOfFiles('items', '.png')
        
        for i in range(amount):
            try:
                self.itemSprites.append(self.loadImage(g.dataPath + '/items/' + str(i) + '.png'))
            except:
                break

    def loadSpells(self):
        amount = self.getAmountOfFiles('spells', '.bmp')
        
        for i in range(amount):
            try:
                self.spellSprites.append(self.loadImage(g.dataPath + '/spells/' + str(i) + '.bmp'))

            except:
                break


ResourceManager = ResourceManagerClass()
import pygame
from constants import *
from resourcemanager import ResourceManager


class CharacterSprite(pygame.sprite.DirtySprite):
    def __init__(self, sprite):
        super(CharacterSprite, self).__init__()

        self.image = ResourceManager.plrSprites[sprite]

        self.rect.x = 0
        self.rect.y = 0

class MapLayerSprite(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.Surface((MAX_MAPX*PIC_X, MAX_MAPY*PIC_Y), pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
from constants import *
import pygame

# Public data structures
# - Initializations are at the bottom of the source code

class Stats():
    strength,  \
    defense,   \
    speed,     \
    magic,     \
    stat_count \
    = range(5)


class Vitals():
    hp,         \
    mp,         \
    sp,         \
    vital_count \
    = range(4)


class Equipment():
    weapon,         \
    armor,          \
    helmet,         \
    shield,         \
    equipment_count \
    = range(5)


class PlayerClass():
    def __init__(self):
        # General
        self.Name = ""
        self.Class = None
        self.Sprite = 4
        self.level = None
        self.exp = None
        self.access = None
        self.pk = None

        # stats
        self.stats = [None for i in range(Stats.stat_count)]
        self.statsPoints = None

        # vitals (hp, mp etc.)
        self.vitals = [None for i in range(Vitals.vital_count)]

        # equipment
        self.equipment = [None for i in range(Equipment.equipment_count)]

        # Position
        self.Map = None     # None
        self.x = 5      # None
        self.y = 5          # None
        self.Dir = 1        # None

        # Client
        self.maxHP = None
        self.maxMP = None
        self.maxSP = None
        self.xOffset = 0
        self.yOffset = 0
        self.moving = 0
        self.attacking = 0
        self.attackTimer = 0
        self.mapGetTimer = 0
        self.castedSpell = 0


class ClassClass():
    def __init__(self):
        self.name = ""
        self.sprite = 1
        self.stat = [None for i in range(Stats.stat_count)]

        # for client use
        self.vital = [None for i in range(Vitals.vital_count)]


class TileClass():
    def __init__(self):
        self.ground = 0
        self.mask = 0
        self.anim = 0
        self.fringe = 0
        self.type = 0
        self.data1 = 0
        self.data2 = 0
        self.data3 = 0


class TilePosClass():
    def __init__(self):
        self.x = 0
        self.y = 0

        self.ground = pygame.Rect(0, 0, 0, 0)
        self.mask = pygame.Rect(0, 0, 0, 0)
        self.anim = pygame.Rect(0, 0, 0, 0)
        self.fringe = pygame.Rect(0, 0, 0, 0)


class TempTileClass():
    def __init__(self):
        self.doorOpen = 0


class MapClass():
    def __init__(self):
        self.name = ""
        self.revision = 0
        self.moral = None
        self.tileSet = 1

        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0

        self.bootMap = 0
        self.bootX = 0
        self.bootY = 0

        self.tile = [[TileClass() for i in range(MAX_MAPY)] for i in range(MAX_MAPX)]


# Data initializations
Map = MapClass()
MapTilePosition = [[TilePosClass() for i in range(MAX_MAPY)] for i in range(MAX_MAPX)]
TempTile = [[TempTileClass() for i in range(MAX_MAPY)] for i in range(MAX_MAPX)]

Player = [PlayerClass() for i in range(MAX_PLAYERS)]

#todo: dont use a fixed size, please
Class = [ClassClass() for i in range(99)]

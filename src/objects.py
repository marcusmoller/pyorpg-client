from constants import MAX_PLAYERS, MAX_MAPX, MAX_MAPY, MAX_INV, MAX_ITEMS, MAX_MAP_ITEMS, MAX_NPCS, MAX_MAP_NPCS, MAX_SPELLS, MAX_PLAYER_SPELLS, MAX_TRADES, MAX_SHOPS
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

class PlayerInvClass():
    def __init__(self):
        self.num = None
        self.value = 0
        self.dur = 0

class PlayerClass():
    def __init__(self):
        # General
        self.Name = ""
        self.Class = None
        self.Sprite = 0
        self.level = 0
        self.exp = 0
        self.access = 0
        self.pk = 0

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

        # Client only
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
        self.ground = None
        self.mask = 0
        self.anim = 0
        self.fringe = None
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
        self.npc = [None for i in range(MAX_MAP_NPCS)]

class MapItemClass():
    def __init__(self):
        self.num = None
        self.value = None
        self.dur = None

        self.x = None
        self.y = None

class ItemClass():
    def __init__(self):
        self.name = ""
        self.pic = 0
        self.type = 0
        self.data1 = 0
        self.data2 = 0
        self.data3 = 0

class SpellClass():
    def __init__(self):
        self.name = ''
        self.pic = None

        self.reqMp = None
        self.reqClass = None
        self.reqLevel = None

        self.type = None
        self.data1 = 0
        self.data2 = 0
        self.data3 = 0

class NPCClass():
    def __init__(self):
        self.name = ''
        self.attackSay = ''

        self.sprite = None
        self.spawnSecs = 20
        self.behaviour = 0
        self.range = 0

        self.dropChance = 0
        self.dropItem = 0
        self.dropItemValue = 0

        self.stat = [None for i in range(Stats.stat_count)]

class MapNPCClass():
    def __init__(self):
        self.num = None
        self.target = None

        self.vital = [None for i in range(Vitals.vital_count)]

        self.map = None
        self.x = None
        self.y = None
        self.dir = None

        # client use only
        self.xOffset = 0
        self.yOffset = 0
        self.moving = 0
        self.attacking = False
        self.attackTimer = 0

class TradeItemClass():
    def __init__(self):
        self.giveItem = None
        self.giveValue = None

        self.getItem = None
        self.getValue = None

class ShopClass():
    def __init__(self):
        self.name = ''
        self.joinSay = ''
        self.leaveSay = ''
        self.fixesItems = False
        self.tradeItem = [TradeItemClass() for i in range(MAX_TRADES)]



# Data initializations
Map = MapClass()
MapTilePosition = [[TilePosClass() for i in range(MAX_MAPY)] for i in range(MAX_MAPX)]
TempTile = [[TempTileClass() for i in range(MAX_MAPY)] for i in range(MAX_MAPX)]

Player = [PlayerClass() for i in range(MAX_PLAYERS)]
PlayerInv = [PlayerInvClass() for i in range(MAX_INV)]
PlayerSpells = [None for i in range(MAX_PLAYER_SPELLS)]

#todo: dont use a fixed size, please
Class = [ClassClass() for i in range(99)]
Item = [ItemClass() for i in range(MAX_ITEMS)]
Spell = [SpellClass() for i in range(MAX_SPELLS)]
NPC = [NPCClass() for i in range(MAX_NPCS)]
MapItem = [MapItemClass() for i in range(MAX_MAP_ITEMS)]
mapNPC = [MapNPCClass() for i in range(MAX_MAP_NPCS)]
Shop = [ShopClass() for i in range(MAX_SHOPS)]

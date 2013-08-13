# Server information
GAME_IP = "127.0.0.1"

# Tilesheet width
# - Number of tiles in width in tileset
TILESHEET_WIDTH = 7

# movement speed variables
WALK_SPEED = 4
RUN_SPEED  = 8

# Tile size
PIC_X = 32
PIC_Y = 32

# Sprite, item, spell size constants
SIZE_X = PIC_X
SIZE_Y = PIC_Y

# game states
MENU_LOGIN    = 0
MENU_REGISTER = 1
MENU_CHAR     = 2
MENU_NEWCHAR  = 3
MENU_INGAME   = 4

# sound states
SOUND_OPENING = 0
SOUND_TOWN = 1
SOUND_OTHER = 2

# debugging
DEBUGGING = False


###############################################
# VALUES BELOW MUST MATCH THE SERVER'S VALUES #
###############################################

# general constants
GAME_NAME = "PyORPG"  # the game name
GAME_PORT = 2727      # the game port
MAX_PLAYERS = 70      # the maximum amount of (online) players allowed in the game
MAX_ITEMS = 255       # the total maximum amount of items allowed in the game
MAX_NPCS = 255        # the total maximum amount of npcs allowed in the game
MAX_MAP_NPCS = 5      # the maximum amount of npcs allowed on a map
MAX_INV = 9  # 50     # the amount of inventory slots
MAX_LEVELS = 100      # the maximum player and npc level

# website
GAME_WEBSITE = "https://powrtoch.org/pyorpg/"

# account constants
NAME_LENGTH = 20
MAX_CHARS = 3

# map constants
MAX_MAPS = 100
MAX_MAPX = 15
MAX_MAPY = 11

# text colors
class textColor():
    BLACK      = (  0,   0,   0)
    WHITE      = (255, 255, 255)
    BLUE       = (  0,   0, 255)
    GREEN      = (  0, 255,   0)
    RED        = (255,   0,   0)
    CYAN       = (  0, 255, 255)
    YELLOW     = (255, 255,   0)
    GREY       = (128, 128, 128)
    PINK       = (255,   0, 255)
    BROWN      = (153,  76,   0)

    BRIGHT_RED   = (255,  51,  51)
    BRIGHT_GREEN = (128, 255,   0)
    BRIGHT_BLUE  = (  0, 128, 255)
    BRIGHT_CYAN  = (  0, 255, 128)

    DARK_GREY    = ( 96,  96,  96)
    DARK_CYAN    = (  0, 204, 204)


sayColor       = textColor.GREY
globalColor    = textColor.BRIGHT_BLUE
broadcastColor = textColor.PINK
tellColor      = textColor.BRIGHT_GREEN
emoteColor     = textColor.BRIGHT_CYAN
adminColor     = textColor.BRIGHT_CYAN
helpColor      = textColor.PINK
whoColor       = textColor.PINK
joinLeftColor  = textColor.DARK_GREY
npcColor       = textColor.BROWN
alertColor     = textColor.RED
newMapColor    = textColor.PINK

UI_FONT_COLOR = (251, 230, 204)

# tile constants
TILE_TYPE_WALKABLE = 0
TILE_TYPE_BLOCKED  = 1
TILE_TYPE_WARP     = 2
TILE_TYPE_ITEM     = 3
TILE_TYPE_NPCAVOID = 4
TILE_TYPE_KEY      = 5
TILE_TYPE_KEYOPEN  = 6

# item constants
ITEM_TYPE_NONE        = 0
ITEM_TYPE_WEAPON      = 1
ITEM_TYPE_ARMOR       = 2
ITEM_TYPE_HELMET      = 3
ITEM_TYPE_SHIELD      = 4
ITEM_TYPE_POTIONADDHP = 5
ITEM_TYPE_POTIONADDMP = 6
ITEM_TYPE_POTIONADDSP = 7
ITEM_TYPE_POTIONSUBHP = 8
ITEM_TYPE_POTIONSUBMP = 9
ITEM_TYPE_POTIONSUBSP = 10
ITEM_TYPE_KEY         = 11
ITEM_TYPE_CURRENCY    = 12
ITEM_TYPE_SPELL       = 13

# direction constants
DIR_UP = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_RIGHT = 3

# player movement
MOVING_WALKING = 1
MOVING_RUNNING = 2

# admin constants
ADMIN_MONITOR   = 1
ADMIN_MAPPER    = 2
ADMIN_DEVELOPER = 3
ADMIN_CREATOR   = 4

# npc constants
NPC_BEHAVIOUR_ATTACKONSIGHT = 0
NPC_BEHAVIOUR_ATTACKWHENATTACKED = 1
NPC_BEHAVIOUR_FRIENDLY = 2
NPC_BEHAVIOUR_SHOPKEEPER = 3
NPC_BEHAVIOUR_GUARD = 4

# game editor constants
EDITOR_NONE  = 0
EDITOR_ITEM  = 1
EDITOR_NPC   = 2
EDITOR_SPELL = 3
EDITOR_SHOP  = 4
EDITOR_MAP   = 5
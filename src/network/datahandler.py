import time
import os.path

from pgu import gui
from gui.dialogs import alertMessageDialog
from .database import *
from gamelogic import *
import global_vars as g
from objects import *
from constants import *
from .packettypes import *
from utils.utils import *


class DataHandler():
    ''' class for handling data sent from the server '''

    def __init__(self, protocol=2):
        self.protocol = protocol

    def handleData(self, data):
        jsonData = decodeJSON(data)
        packetType = jsonData[0]["packet"]

        if packetType == ServerPackets.SAlertMsg:
            self.handleAlertMsg(jsonData)

        elif packetType == ServerPackets.SAllChars:
            self.handleAllChars(jsonData)

        elif packetType == ServerPackets.SLoginOK:
            self.handleLoginOK(jsonData)

        elif packetType == ServerPackets.SNewCharClasses:
            self.handleNewCharClasses(jsonData)

        elif packetType == ServerPackets.SClassesData:
            self.handleClassesData(jsonData)

        elif packetType == ServerPackets.SInGame:
            self.handleInGame()

        elif packetType == ServerPackets.SSpells:
            self.handlePlayerSpells(jsonData)

        elif packetType == ServerPackets.SPlayerInv:
            self.handlePlayerInv(jsonData)

        elif packetType == ServerPackets.SPlayerInvUpdate:
            self.handlePlayerInvUpdate(jsonData)

        elif packetType == ServerPackets.SPlayerWornEq:
            self.handlePlayerWornEq(jsonData)

        elif packetType == ServerPackets.SPlayerHP:
            self.handlePlayerHP(jsonData)

        elif packetType == ServerPackets.SPlayerMP:
            self.handlePlayerMP(jsonData)

        elif packetType == ServerPackets.SPlayerSP:
            self.handlePlayerSP(jsonData)

        elif packetType == ServerPackets.SPlayerStats:
            self.handlePlayerStats(jsonData)

        elif packetType == ServerPackets.SPlayerData:
            self.handlePlayerData(jsonData)

        elif packetType == ServerPackets.SPlayerLevel:
            self.handlePlayerLevel(jsonData)

        elif packetType == ServerPackets.SPlayerMove:
            self.handlePlayerMove(jsonData)

        elif packetType == ServerPackets.SPlayerDir:
            self.handlePlayerDir(jsonData)

        elif packetType == ServerPackets.SPlayerXY:
            self.handlePlayerXY(jsonData)

        elif packetType == ServerPackets.SAttack:
            self.handleAttack(jsonData)

        elif packetType == ServerPackets.SCastSpell:
            self.handleSpellCast(jsonData)

        elif packetType == ServerPackets.SCheckForMap:
            self.handleCheckForMap(jsonData)

        elif packetType == ServerPackets.SMapData:
            self.handleMapData(jsonData)

        elif packetType == ServerPackets.SMapItemData:
            self.handleMapItemData(jsonData)

        elif packetType == ServerPackets.SMapNpcData:
            self.handleMapNpcData(jsonData)

        elif packetType == ServerPackets.SMapDone:
            self.handleMapDone()

        elif packetType == ServerPackets.SSayMsg:
            self.handleSayMsg(jsonData)

        elif packetType == ServerPackets.SGlobalMsg:
            self.handleGlobalMsg(jsonData)

        elif packetType == ServerPackets.SAdminMsg:
            self.handleAdminMsg(jsonData)

        elif packetType == ServerPackets.SPlayerMsg:
            self.handlePlayerMsg(jsonData)

        elif packetType == ServerPackets.SMapMsg:
            self.handleMapMsg(jsonData)

        elif packetType == ServerPackets.SSpawnItem:
            self.handleSpawnItem(jsonData)

        elif packetType == ServerPackets.SItemEditor:
            self.handleItemEditor()

        elif packetType == ServerPackets.SUpdateItem:
            self.handleUpdateItem(jsonData)

        elif packetType == ServerPackets.SSpellEditor:
            self.handleSpellEditor()

        elif packetType == ServerPackets.SEditSpell:
            self.handleEditSpell(jsonData)

        elif packetType == ServerPackets.SUpdateSpell:
            self.handleUpdateSpell(jsonData)

        elif packetType == ServerPackets.SEditMap:
            self.handleEditMap()

        elif packetType == ServerPackets.SNpcEditor:
            self.handleNpcEditor()

        elif packetType == ServerPackets.SEditNpc:
            self.handleEditNpc(jsonData)

        elif packetType == ServerPackets.SSpawnNpc:
            self.handleSpawnNpc(jsonData)

        elif packetType == ServerPackets.SNpcMove:
            self.handleNpcMove(jsonData)

        elif packetType == ServerPackets.SNpcDir:
            self.handleNpcDir(jsonData)

        elif packetType == ServerPackets.SNpcDead:
            self.handleNpcDead(jsonData)

        elif packetType == ServerPackets.SUpdateNpc:
            self.handleUpdateNpc(jsonData)

        elif packetType == ServerPackets.SMapList:
            self.handleMapList(jsonData)

        elif packetType == ServerPackets.SLeft:
            self.handleLeft(jsonData)

        elif packetType == ServerPackets.SHighIndex:
            self.handleHighIndex(jsonData)

        else:
            # Packet is unknown - hacking attempt
            print("hacking attempt")

    def handleAlertMsg(self, jsonData):
        msg = jsonData[0]['msg']

        alertMessageDialog(msg=msg)

    def handleAllChars(self, jsonData):
        # pass it on to the character selection

        # this is a rather dirty hack
        # this is to tell the client, that the server has actually allowed the log in - should probably be done elsewhere
        g.gameEngine.setState(MENU_CHAR)
        g.gameEngine.menuChar.updateCharacters(jsonData)

    def handleLoginOK(self, jsonData):
        g.myIndex = jsonData[0]["index"]
        log("Login was successful! Index ID is: " + str(g.myIndex))

    def handleNewCharClasses(self, jsonData):
        g.maxClasses = jsonData[0]["maxclasses"]

        for i in range(0, g.maxClasses):
            Class[i].name = jsonData[i+1]["classname"]
            Class[i].sprite = jsonData[i+1]["sprite"]

            Class[i].vital[Vitals.hp] = jsonData[i+1]["classmaxhp"]
            Class[i].vital[Vitals.mp] = jsonData[i+1]["classmaxmp"]
            Class[i].vital[Vitals.sp] = jsonData[i+1]["classmaxsp"]

            Class[i].stat[Stats.strength] = jsonData[i+1]["classstatstr"]
            Class[i].stat[Stats.defense] = jsonData[i+1]["classstatdef"]
            Class[i].stat[Stats.speed] = jsonData[i+1]["classstatspd"]
            Class[i].stat[Stats.magic] = jsonData[i+1]["classstatmag"]

        # for creating a new character
        g.gameEngine.menuNewChar.updateClassSelection()

    def handleClassesData(self, jsonData):
        g.maxClasses = jsonData[0]["maxclasses"]

        for i in range(0, g.maxClasses):
            Class[i].name = jsonData[i+1]["classname"]
            Class[i].sprite = jsonData[i+1]["sprite"]

            Class[i].vital[Vitals.hp] = jsonData[i+1]["classmaxhp"]
            Class[i].vital[Vitals.mp] = jsonData[i+1]["classmaxmp"]
            Class[i].vital[Vitals.sp] = jsonData[i+1]["classmaxsp"]

            Class[i].stat[Stats.strength] = jsonData[i+1]["classstatstr"]
            Class[i].stat[Stats.defense] = jsonData[i+1]["classstatdef"]
            Class[i].stat[Stats.speed] = jsonData[i+1]["classstatspd"]
            Class[i].stat[Stats.magic] = jsonData[i+1]["classstatmag"]

    def handleInGame(self):
        g.inGame = True
        # gameInit (START SPIL)
        # gameLoop
        log("Player is ingame")

        # TODO: fix this
        initMapData()

    def handlePlayerSpells(self, jsonData):
        for i in range(len(jsonData)-1):
            slot = jsonData[i+1]['slot']
            PlayerSpells[slot] = jsonData[i+1]['spellnum']

    def handlePlayerInv(self, jsonData):
        for i in range(len(jsonData)-1):
            if jsonData[i+1]['itemnum'] is not None:
                setPlayerInvItemNum(g.myIndex, i, jsonData[i+1]['itemnum'])
                setPlayerInvItemValue(g.myIndex, i, jsonData[i+1]['itemvalue'])
                setPlayerInvItemDur(g.myIndex, i, jsonData[i+1]['itemdur'])

    def handlePlayerInvUpdate(self, jsonData):
        invSlot = jsonData[0]['invslot']
        itemNum = jsonData[0]['itemnum']
        itemValue = jsonData[0]['itemvalue']
        itemDur = jsonData[0]['itemdur']

        setPlayerInvItemNum(g.myIndex, invSlot, itemNum)
        setPlayerInvItemValue(g.myIndex, invSlot, itemValue)
        setPlayerInvItemDur(g.myIndex, invSlot, itemDur)

    def handlePlayerWornEq(self, jsonData):
        setPlayerEquipmentSlot(g.myIndex, jsonData[0]['helmet'], Equipment.helmet)
        setPlayerEquipmentSlot(g.myIndex, jsonData[0]['armor'], Equipment.armor)
        setPlayerEquipmentSlot(g.myIndex, jsonData[0]['weapon'], Equipment.weapon)
        setPlayerEquipmentSlot(g.myIndex, jsonData[0]['shield'], Equipment.shield)

    def handlePlayerHP(self, jsonData):
        Player[g.myIndex].maxHP = jsonData[0]["hp_max"]
        setPlayerVital(g.myIndex, Vitals.hp, jsonData[0]["hp"])

    def handlePlayerMP(self, jsonData):
        Player[g.myIndex].maxMP = jsonData[0]["mp_max"]
        setPlayerVital(g.myIndex, Vitals.mp, jsonData[0]["mp"])

    def handlePlayerSP(self, jsonData):
        Player[g.myIndex].maxSP = jsonData[0]["sp_max"]
        setPlayerVital(g.myIndex, Vitals.sp, jsonData[0]["sp"])

    def handlePlayerStats(self, jsonData):
        setPlayerStat(g.myIndex, Stats.strength, jsonData[0]["strength"])
        setPlayerStat(g.myIndex, Stats.defense, jsonData[0]["defense"])
        setPlayerStat(g.myIndex, Stats.speed, jsonData[0]["speed"])
        setPlayerStat(g.myIndex, Stats.magic, jsonData[0]["magic"])

    def handlePlayerLevel(self, jsonData):
        setPlayerLevel(g.myIndex, jsonData[0]['level'])
        setPlayerExp(g.myIndex, jsonData[0]['exp'])
        g.expToNextLvl = jsonData[0]['exptolevel']

        # refresh main ui
        g.gameEngine.graphicsEngine.gameGUI.reset()

    def handlePlayerData(self, jsonData):
        index = jsonData[0]["index"]

        setPlayerName(index, jsonData[0]["name"])
        setPlayerSprite(index, jsonData[0]["sprite"])
        setPlayerMap(index, jsonData[0]["map"])
        setPlayerX(index, jsonData[0]["x"])
        setPlayerY(index, jsonData[0]["y"])
        setPlayerDir(index, jsonData[0]["direction"])
        setPlayerAccess(index, jsonData[0]["access"])

        if index == g.myIndex:
            g.inpDIR_UP = False
            g.inpDIR_DOWN = False
            g.inpDIR_LEFT = False
            g.inpDIR_RIGHT = False

        Player[index].moving = 0
        Player[index].xOffset = 0
        Player[index].yOffset = 0

        getPlayersOnMap()

    def handlePlayerMove(self, jsonData):
        index = jsonData[0]["index"]
        x = jsonData[0]["x"]
        y = jsonData[0]["y"]
        direction = jsonData[0]["direction"]
        movement = jsonData[0]["moving"]

        setPlayerX(index, x)
        setPlayerY(index, y)
        setPlayerDir(index, direction)

        Player[index].xOffset = 0
        Player[index].yOffset = 0
        Player[index].moving = movement

        if direction == DIR_UP:
            Player[index].yOffset = PIC_Y

        elif direction == DIR_DOWN:
            Player[index].yOffset = -PIC_Y

        elif direction == DIR_LEFT:
            Player[index].xOffset = PIC_X

        elif direction == DIR_RIGHT:
            Player[index].xOffset = -PIC_X

    def handlePlayerDir(self, jsonData):
        index = jsonData[0]["index"]
        direction = jsonData[0]["direction"]

        setPlayerDir(index, direction)

    def handlePlayerXY(self, jsonData):
        x = jsonData[0]['x']
        y = jsonData[0]['y']

        setPlayerX(g.myIndex, x)
        setPlayerY(g.myIndex, y)

        # make sure they arent walking
        Player[g.myIndex].moving = 0
        Player[g.myIndex].xOffset = 0
        Player[g.myIndex].yOffset = 0

    def handleAttack(self, jsonData):
        i = jsonData[0]['attacker']

        Player[i].attacking = 1
        Player[i].attackTimer = time.time()

        # play attack sound
        g.soundEngine.playAttack()
        print("attacksound!")

    def handleSpellCast(self, jsonData):
        targetType = jsonData[0]['targettype']
        target = jsonData[0]['target']
        spellNum = jsonData[0]['spellnum']

        if target is None or spellNum is None:
            return

        tickCount = time.time() * 1000
        if targetType == TARGET_TYPE_PLAYER:
            for i in range(MAX_SPELLANIM):
                if Player[target].spellAnimations[i].spellNum is None:
                    Player[target].spellAnimations[i].spellNum = spellNum
                    Player[target].spellAnimations[i].timer = tickCount + 120
                    Player[target].spellAnimations[i].framePointer = 0
                    break  

        elif targetType == TARGET_TYPE_NPC:
            for i in range(MAX_SPELLANIM):
                if mapNPC[target].spellAnimations[i].spellNum is None:
                    mapNPC[target].spellAnimations[i].spellNum = spellNum
                    mapNPC[target].spellAnimations[i].timer = tickCount + 120
                    mapNPC[target].spellAnimations[i].framePointer = 0
                    break

        g.soundEngine.playSpellHit(Spell[spellNum].type)

    def handleCheckForMap(self, jsonData):
        # erase other players
        for i in range(len(Player)):
            if i != g.myIndex:
                setPlayerMap(i, 0)

        # erase temporary tiles
        clearTempTile()

        clearMapNpcs()
        clearMapItems()
        clearMap()

        mapNum = jsonData[0]["mapnum"]
        revision = jsonData[0]["revision"]

        # check if a revision is even needed
        if os.path.isfile("data/maps/" + str(mapNum) + ".pom"):
            loadMap(mapNum)
            if Map.revision == revision:
                # we dont need new mapo
                g.tcpConn.sendNeedMap()
                return

        # we need the new map
        g.tcpConn.sendNeedMap(1)

    def handleMapData(self, jsonData):
        # todo: fix the darn -1 thingy
        Map.name     = jsonData[0]["mapname"]
        Map.revision = jsonData[0]["revision"]
        Map.moral    = jsonData[0]["moral"]
        Map.tileset  = jsonData[0]["tileset"]
        Map.up       = jsonData[0]["up"]
        Map.down     = jsonData[0]["down"]
        Map.left     = jsonData[0]["left"]
        Map.right    = jsonData[0]["right"]
        Map.bootMap  = jsonData[0]["bootmap"]
        Map.bootX    = jsonData[0]["bootx"]
        Map.bootY    = jsonData[0]["booty"]

        i = 1
        for x in range(MAX_MAPX):
            for y in range(MAX_MAPY):
                Map.tile[x][y].layer1 = jsonData[i][0]["layer1"]
                Map.tile[x][y].layer2 = jsonData[i][0]["layer2"]
                Map.tile[x][y].layer3 = jsonData[i][0]["layer3"]
                Map.tile[x][y].mask   = jsonData[i][0]["mask"]
                Map.tile[x][y].anim   = jsonData[i][0]["animation"]
                Map.tile[x][y].fringe = jsonData[i][0]["fringe"]
                Map.tile[x][y].type   = jsonData[i][0]["type"]
                Map.tile[x][y].data1  = jsonData[i][0]["data1"]
                Map.tile[x][y].data2  = jsonData[i][0]["data2"]
                Map.tile[x][y].data3  = jsonData[i][0]["data3"]

                i += 1

        for j in range(MAX_MAP_NPCS):
            Map.npc[j] = jsonData[i][0]["npc"]

            i += 1

        # save map
        saveMap(jsonData[0]["mapnum"])

    def handleMapItemData(self, jsonData):
        for i in range(MAX_MAP_ITEMS):
            MapItem[i].num = jsonData[i+1]['itemnum']
            MapItem[i].value = jsonData[i+1]['itemval']
            MapItem[i].dur = jsonData[i+1]['itemdur']
            MapItem[i].x = jsonData[i+1]['x']
            MapItem[i].y = jsonData[i+1]['y']

    def handleMapNpcData(self, jsonData):
        for i in range(MAX_MAP_NPCS):
            mapNPC[i].num = jsonData[i+1]['num']
            mapNPC[i].x = jsonData[i+1]['x']
            mapNPC[i].y = jsonData[i+1]['y']
            mapNPC[i].dir = jsonData[i+1]['dir']


    def handleMapDone(self):
        # calculate amount of npcs on map
        g.npcHighIndex = 0
        for i in range(MAX_MAP_NPCS):
            if Map.npc[i] != None:
                g.npcHighIndex += 1
        
        calcTilePositions()
        g.gameEngine.graphicsEngine.redrawMap()

        g.gettingMap = False
        g.canMoveNow = True

    def handleSayMsg(self, jsonData):
        ''' called when a player sends a message in the map '''
        msg = jsonData[0]["msg"]
        color = jsonData[0]["color"]
        addText(msg, color)

    def handleGlobalMsg(self, jsonData):
        msg = jsonData[0]["msg"]
        color = jsonData[0]["color"]
        addText(msg, color)

    def handleAdminMsg(self, jsonData):
        msg = jsonData[0]["msg"]
        color = jsonData[0]["color"]
        addText(msg, color)

    def handlePlayerMsg(self, jsonData):
        msg = jsonData[0]["msg"]
        color = jsonData[0]["color"]
        addText(msg, color)

    def handleMapMsg(self, jsonData):
        msg = jsonData[0]["msg"]
        color = jsonData[0]["color"]
        addText(msg, color)

    def handleSpawnItem(self, jsonData):
        itemSlot = jsonData[0]['slot']

        MapItem[itemSlot].num = jsonData[0]['itemnum']
        MapItem[itemSlot].value = jsonData[0]['itemval']
        MapItem[itemSlot].dur = jsonData[0]['itemdur']
        MapItem[itemSlot].x = jsonData[0]['x']
        MapItem[itemSlot].y = jsonData[0]['y']

    def handleItemEditor(self):
        ''' called when server allows player to edit items '''
        g.editor = EDITOR_ITEM

        g.gameEngine.graphicsEngine.gameGUI.guiContainer.openItemEditor()
        g.gameEngine.graphicsEngine.gameGUI.setState(4)
        g.gameEngine.graphicsEngine.gameGUI.itemEditorGUI.init()

    def handleUpdateItem(self, jsonData):
        itemNum = jsonData[0]['itemnum']

        # update item
        Item[itemNum].name = jsonData[0]['itemname']
        Item[itemNum].pic = int(jsonData[0]['itempic'])
        Item[itemNum].type = (jsonData[0]['itemtype'])
        Item[itemNum].data1 = jsonData[0]['itemdata1']
        Item[itemNum].data2 = jsonData[0]['itemdata2']
        Item[itemNum].data3 = jsonData[0]['itemdata3']

    def handleSpellEditor(self):
        g.editor = EDITOR_SPELL

        g.gameEngine.graphicsEngine.gameGUI.guiContainer.openSpellEditor()
        g.gameEngine.graphicsEngine.gameGUI.setState(6)
        g.gameEngine.graphicsEngine.gameGUI.spellEditorGUI.init()

    def handleEditSpell(self, jsonData):
        spellNum = jsonData[0]['spellnum']

        # update spell
        Spell[spellNum].name = jsonData[0]['spellname']
        Spell[spellNum].pic = jsonData[0]['pic']
        Spell[spellNum].type = jsonData[0]['type']

        Spell[spellNum].reqMp = jsonData[0]['reqmp']
        Spell[spellNum].reqClass = jsonData[0]['reqclass']
        Spell[spellNum].reqLevel = jsonData[0]['reqlevel']

        Spell[spellNum].data1 = jsonData[0]['data1']
        Spell[spellNum].data2 = jsonData[0]['data2']
        Spell[spellNum].data3 = jsonData[0]['data3']

        # update the spell editor
        g.gameEngine.graphicsEngine.gameGUI.guiContainer.spellEditorControl.openSpell(spellNum)

    def handleUpdateSpell(self, jsonData):
        spellNum = jsonData[0]['spellnum']

        # update everything
        Spell[spellNum].name = jsonData[0]['spellname']
        Spell[spellNum].pic = jsonData[0]['pic']
        Spell[spellNum].type = jsonData[0]['type']

        Spell[spellNum].reqMp = jsonData[0]['reqmp']

        Spell[spellNum].data1 = jsonData[0]['data1']

    def handleEditMap(self):
        ''' called when server allows player to edit the map '''
        g.editor = EDITOR_MAP

        g.gameEngine.graphicsEngine.gameGUI.guiContainer.openEditor()
        g.gameEngine.graphicsEngine.gameGUI.setState(3)
        g.gameEngine.graphicsEngine.gameGUI.mapEditorGUI.init()

    def handleNpcEditor(self):
        g.editor = EDITOR_NPC

        g.gameEngine.graphicsEngine.gameGUI.guiContainer.openNpcEditor()
        g.gameEngine.graphicsEngine.gameGUI.setState(5)
        g.gameEngine.graphicsEngine.gameGUI.npcEditorGUI.init()

    def handleEditNpc(self, jsonData):
        npcNum = jsonData[0]['npcnum']

        # update npc
        NPC[npcNum].name = jsonData[0]['name']
        NPC[npcNum].attackSay = jsonData[0]['attacksay']
        NPC[npcNum].sprite = jsonData[0]['sprite']
        NPC[npcNum].spawnSecs = jsonData[0]['spawnsec']
        NPC[npcNum].behaviour = jsonData[0]['behavior']
        NPC[npcNum].range = jsonData[0]['range']

        NPC[npcNum].dropChance = jsonData[0]['dropchance']
        NPC[npcNum].dropItem = jsonData[0]['dropitem']
        NPC[npcNum].dropItemValue = jsonData[0]['dropitemval']

        NPC[npcNum].stat[Stats.strength] = jsonData[0]['strength']
        NPC[npcNum].stat[Stats.defense] = jsonData[0]['defense']
        NPC[npcNum].stat[Stats.magic] = jsonData[0]['magic']
        NPC[npcNum].stat[Stats.speed] = jsonData[0]['speed']

        # update the npc editor
        g.gameEngine.graphicsEngine.gameGUI.guiContainer.npcEditorControl.openNPC(npcNum)

    def handleSpawnNpc(self, jsonData):
        mapNpcNum = jsonData[0]['mapnpcnum']

        mapNPC[mapNpcNum].num = jsonData[0]['num']
        mapNPC[mapNpcNum].x = jsonData[0]['x']
        mapNPC[mapNpcNum].y = jsonData[0]['y']
        mapNPC[mapNpcNum].dir = jsonData[0]['dir']

        # client use only
        mapNPC[mapNpcNum].xOffset = 0
        mapNPC[mapNpcNum].yOffset = 0
        mapNPC[mapNpcNum].moving = 0

    def handleNpcMove(self, jsonData):
        mapNpcNum = jsonData[0]['mapnpcnum']

        mapNPC[mapNpcNum].x = jsonData[0]['x']
        mapNPC[mapNpcNum].y = jsonData[0]['y']
        mapNPC[mapNpcNum].dir = jsonData[0]['dir']
        direction = jsonData[0]['dir']

        mapNPC[mapNpcNum].xOffset = 0
        mapNPC[mapNpcNum].yOffset = 0
        mapNPC[mapNpcNum].moving = jsonData[0]['movement']

        if direction == DIR_UP:
            mapNPC[mapNpcNum].yOffset = PIC_Y

        elif direction == DIR_DOWN:
            mapNPC[mapNpcNum].yOffset = PIC_Y * -1

        elif direction == DIR_LEFT:
            mapNPC[mapNpcNum].xOffset = PIC_X

        elif direction == DIR_RIGHT:
            mapNPC[mapNpcNum].xOffset = PIC_X * -1

    def handleNpcDir(self, jsonData):
        mapNpcNum = jsonData[0]['mapnpcnum']
        direction = jsonData[0]['direction']

        mapNPC[mapNpcNum].dir = direction
        mapNPC[mapNpcNum].xOffset = 0
        mapNPC[mapNpcNum].yOffset = 0
        mapNPC[mapNpcNum].moving = 0

    def handleNpcDead(self, jsonData):
        mapNpcNum = jsonData[0]['mapnpcnum']
        clearMapNpc(mapNpcNum)

        # remove target if current target
        if g.targetType == TARGET_TYPE_NPC and mapNpcNum == g.target:
            g.target = None
            g.targetType = TARGET_TYPE_NONE


    def handleUpdateNpc(self, jsonData):
        npcNum = jsonData[0]['npcnum']

        # update npc
        NPC[npcNum].name = jsonData[0]['name']
        NPC[npcNum].attackSay = ''
        NPC[npcNum].sprite = jsonData[0]['sprite']
        NPC[npcNum].spawnSecs = 0
        NPC[npcNum].behaviour = 0
        NPC[npcNum].range = 0
        NPC[npcNum].stat[Stats.strength] = 0
        NPC[npcNum].stat[Stats.defense] = 0
        NPC[npcNum].stat[Stats.magic] = 0
        NPC[npcNum].stat[Stats.speed] = 0

    def handleMapList(self, jsonData):
        ''' called when receiving list of map names from server which is used for map editing '''
        g.mapNames = jsonData[1]['mapnames']

    def handleLeft(self, jsonData):
        ''' called when a player has left the game '''
        index = jsonData[0]["index"]
        clearPlayer(index)
        getPlayersOnMap()

    def handleHighIndex(self, jsonData):
        g.highIndex = jsonData[0]["highindex"]
        log("highIndex updated")

from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, error

import json
import base64

from .database import *
from .packettypes import *
from .datahandler import *
from utils.utils import *
from gui.dialogs import alertMessageDialog
from constants import *
import global_vars as g
from objects import *

dataHandler = None

def startConnection():
    global dataHandler
    factory = gameClientFactory()
    g.connector = reactor.connectTCP(GAME_IP, GAME_PORT, factory)
    dataHandler = DataHandler()

    return factory.protocol

class gameClientProtocol(LineReceiver):
    MAX_LENGTH = 999999 #todo: find a suitable size (see client: sendMap (in clienttcp.py))

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        ''' called when connection has been made '''
        ''' used for logging in and new account '''

        if g.gameState == MENU_LOGIN:
            # logging in, so send login after connection has been established
            username = g.gameEngine.menuLogin.username
            password = g.gameEngine.menuLogin.password

            g.tcpConn.sendLogin(username, password)

        log("Connection established to server")

    def lineReceived(self, data):
        global dataHandler

        # handle base64 data
        decodedData = base64.b64decode(data).decode('utf-8')

        log("Received data from server")
        log(f'-> {decodedData}')

        dataHandler.handleData(decodedData)

    def sendData(self, data):
        # encode data using base64
        data_bytes = data.encode("utf-8")
        encodedData = base64.b64encode(data_bytes)
        self.sendLine(encodedData)


class gameClientFactory(ClientFactory):
    def __init__(self):
        self.protocol = p = gameClientProtocol(self)

    def startedConnecting(self, connector):
        log("Connecting to server...")

    def buildProtocol(self, addr):
        return self.protocol

    def clientConnectionFailed(self, connector, reason):
        errorMsg = reason.getErrorMessage().split(':')
        alertMessageDialog('Unable to connect to server: ' + errorMsg[1] + errorMsg[2], 'An error occured')
        print(reason.getErrorMessage())

    def clientConnectionLost(self, connector, reason):
        print(reason.getErrorMessage())
        try:
            #reactor.stop()
            log("Disconnection from server")
        except error.ReactorNotRunning:
            pass


class TCPConnection():
    def __init__(self, protocol):
        self.protocol = protocol

    def sendData(self, data):
        self.protocol.sendData(data)

    def sendNewAccount(self, username, password):
        packet = json.dumps([{"packet": ClientPackets.CNewAccount, "name": username, "password": password}])
        self.sendData(packet)

    def sendDelAccount(self, username, password):
        packet = json.dumps([{"packet": ClientPackets.CDelAccount, "name": username, "password": password}])
        self.sendData(packet)

    def sendLogin(self, username, password):
        packet = json.dumps([{"packet": ClientPackets.CLogin, "name": username, "password": password}], ensure_ascii=False)
        self.sendData(packet)

    def sendAddChar(self, name, sex, classNum, slot):
        packet = json.dumps([{"packet": ClientPackets.CAddChar, "name": name, "sex": sex, "class": classNum, "slot": slot}])
        self.sendData(packet)

    def sendDelChar(self, slot):
        packet = json.dumps([{"packet": ClientPackets.CDelChar}])
        self.sendData(packet)

    def sendGetClasses(self):
        packet = json.dumps([{"packet": ClientPackets.CGetClasses}])
        self.sendData(packet)

    def sendUseChar(self, charslot):
        packet = json.dumps([{"packet": ClientPackets.CUseChar, "charslot": charslot}])
        self.sendData(packet)

    def sayMsg(self, msg):
        packet = json.dumps([{"packet": ClientPackets.CSayMsg, "msg": msg}])
        self.sendData(packet)

    def globalMsg(self, msg):
        packet = json.dumps([{"packet": ClientPackets.CGlobalMsg, "msg": msg}])
        self.sendData(packet)

    def broadcastMsg(self, msg):
        packet = json.dumps([{"packet": ClientPackets.CBroadcastMsg, "msg": msg}])
        self.sendData(packet)

    def emoteMsg(self, msg):
        packet = json.dumps([{"packet": ClientPackets.CEmoteMsg, "msg": msg}])
        self.sendData(packet)

    def playerMsg(self, msg, msgTo):
        packet = json.dumps([{"packet": ClientPackets.CPlayerMsg, "msg": msg, "msgto": msgTo}])
        self.sendData(packet)

    def adminMsg(self, msg):
        packet = json.dumps([{"packet": ClientPackets.CAdminMsg, "msg": msg}])
        self.sendData(packet)

    def sendPlayerMove(self):
        packet = json.dumps([{"packet": ClientPackets.CPlayerMove, "direction": getPlayerDir(g.myIndex), "moving": Player[g.myIndex].moving}])
        self.sendData(packet)

    def sendPlayerAttack(self):
        packet = json.dumps([{"packet": ClientPackets.CAttack}])
        self.sendData(packet)

    def sendPlayerDir(self):
        packet = json.dumps([{"packet": ClientPackets.CPlayerDir, "direction": getPlayerDir(g.myIndex)}])
        self.sendData(packet)

    def sendPlayerRequestNewMap(self):
        packet = json.dumps([{"packet": ClientPackets.CRequestNewMap, "direction": getPlayerDir(g.myIndex)}])
        self.sendData(packet)

    def sendMapGetItem(self):
        packet = json.dumps([{"packet": ClientPackets.CMapGetItem}])
        self.sendData(packet)

    def sendMap(self):
        #todo: npc

        #canMoveNow = false

        packet = []
        packet.append({"packet": ClientPackets.CMapData, \
                       "mapname": Map.name, \
                       "moral": Map.moral, \
                       "tileset": Map.tileSet, \
                       "up": Map.up, \
                       "down": Map.down, \
                       "left": Map.left, \
                       "right": Map.right, \
                       "bootmap": Map.bootMap, \
                       "bootx": Map.bootX, \
                       "booty": Map.bootY})

        for x in range(MAX_MAPX):
            for y in range(MAX_MAPY):
                tempTile = Map.tile[x][y]
                packet.append([{"layer1":    tempTile.layer1, \
                                "layer2":    tempTile.layer2, \
                                "layer3":    tempTile.layer3, \
                                "mask":      tempTile.mask, \
                                "animation": tempTile.anim, \
                                "fringe":    tempTile.fringe, \
                                "type":      tempTile.type, \
                                "data1":     tempTile.data1, \
                                "data2":     tempTile.data2, \
                                "data3":     tempTile.data3}])


        for i in range(MAX_MAP_NPCS):
            packet.append([{'npcnum': Map.npc[i]}])


        packet = json.dumps(packet)
        self.sendData(packet)

    def sendNeedMap(self, answer=0):
        packet = json.dumps([{"packet": ClientPackets.CNeedMap, "answer": answer}])
        self.sendData(packet)

    def warpMeTo(self, name):
        packet = json.dumps([{'packet': ClientPackets.CWarpMeTo, 'name': name}])
        self.sendData(packet)

    def warpToMe(self, name):
        packet = json.dumps([{'packet': ClientPackets.CWarpToMe, 'name': name}])
        self.sendData(packet)

    def warpTo(self, mapNum):
        packet = json.dumps([{'packet': ClientPackets.CWarpTo, 'map': mapNum}])
        self.sendData(packet)

    def sendSetAccess(self, name, access):
        packet = json.dumps([{'packet': ClientPackets.CSetAccess, 'name': name, 'access': access}])
        self.sendData(packet)

    def sendGiveItem(self, name, itemnum):
        packet = json.dumps([{'packet': ClientPackets.CGiveItem, 'name': name, 'itemnum': itemnum}])
        self.sendData(packet)

    def sendSetSprite(self, spriteNum):
        packet = json.dumps([{"packet": ClientPackets.CSetSprite, "sprite": spriteNum}])
        self.sendData(packet)

    def sendMapReport(self):
        packet = json.dumps([{"packet": ClientPackets.CMapReport}])
        self.sendData(packet)

    def sendMapRespawn(self):
        packet = json.dumps([{"packet": ClientPackets.CMapRespawn}])
        self.sendData(packet)

    def sendUseItem(self, invNum):
        packet = json.dumps([{"packet": ClientPackets.CUseItem, "invnum": invNum}])
        self.sendData(packet)

    def sendCastSpell(self, spellslot):
        packet = json.dumps([{"packet": ClientPackets.CCast, "spellslot": spellslot}])
        self.sendData(packet)

    def sendTarget(self, x, y):
        packet = json.dumps([{"packet": ClientPackets.CTarget, 'x': x, 'y': y}])
        self.sendData(packet)

    def sendInfoRequest(self, plrName):
        packet = json.dumps([{"packet": ClientPackets.CPlayerInfoRequest, "name": plrName}])
        self.sendData(packet)

    def sendWhosOnline(self):
        packet = json.dumps([{'packet': ClientPackets.CWhosOnline}])
        self.sendData(packet)

    def sendRequestEditMap(self):
        packet = json.dumps([{"packet": ClientPackets.CRequestEditMap}])
        self.sendData(packet)

    def sendRequestEditItem(self):
        packet = json.dumps([{"packet": ClientPackets.CRequestEditItem}])
        self.sendData(packet)

    def sendSaveItem(self, itemNum):
        packet = json.dumps([{"packet": ClientPackets.CSaveItem, 'itemnum': itemNum, 'itemname': Item[itemNum].name, 'itempic': Item[itemNum].pic, 'itemtype': Item[itemNum].type, 'itemdata1': Item[itemNum].data1, 'itemdata2': Item[itemNum].data2, 'itemdata3': Item[itemNum].data3}])
        self.sendData(packet)

    def sendRequestSpells(self):
        packet = json.dumps([{"packet": ClientPackets.CSpells}])
        self.sendData(packet)

    def sendRequestEditSpell(self):
        packet = json.dumps([{"packet": ClientPackets.CRequestEditSpell}])
        self.sendData(packet)

    def sendEditSpell(self, spellNum):
        packet = json.dumps([{"packet": ClientPackets.CEditSpell, 'spellnum': spellNum}])
        self.sendData(packet)

    def sendSaveSpell(self, spellNum):
        packet = json.dumps([{"packet": ClientPackets.CSaveSpell, 'spellnum': spellNum, 'spellname': Spell[spellNum].name, 'spellpic': Spell[spellNum].pic, 'spelltype': Spell[spellNum].type, 'mpreq': Spell[spellNum].reqMp, 'classreq': Spell[spellNum].reqClass, 'levelreq': Spell[spellNum].reqLevel, 'data1': Spell[spellNum].data1, 'data2': Spell[spellNum].data2, 'data3': Spell[spellNum].data3}])
        self.sendData(packet)

    def sendRequestEditNpc(self):
        packet = json.dumps([{"packet": ClientPackets.CRequestEditNpc}])
        self.sendData(packet)

    def sendEditNpc(self, npcNum):
        packet = json.dumps([{"packet": ClientPackets.CEditNpc, 'npcnum': npcNum}])
        self.sendData(packet)

    def sendSaveNpc(self, npcNum):
        packet = json.dumps([{"packet": ClientPackets.CSaveNpc, 'npcnum': npcNum, 'name': NPC[npcNum].name, 'attacksay': NPC[npcNum].attackSay, 'sprite': NPC[npcNum].sprite, 'spawnsec': NPC[npcNum].spawnSecs, 'behavior': NPC[npcNum].behaviour, 'range': NPC[npcNum].range, \
                                                                'dropchance': NPC[npcNum].dropChance, 'dropitem': NPC[npcNum].dropItem, 'dropitemval': NPC[npcNum].dropItemValue, \
                                                                'strength': NPC[npcNum].stat[Stats.strength], 'defense': NPC[npcNum].stat[Stats.defense], 'magic': NPC[npcNum].stat[Stats.magic], 'speed': NPC[npcNum].stat[Stats.speed]}])
        self.sendData(packet)

    def sendQuit(self):
        packet = json.dumps([{"packet": ClientPackets.CQuit}])
        self.sendData(packet)

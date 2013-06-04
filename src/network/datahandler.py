import os.path

from database import *
from gamelogic import *
import global_vars as g
from objects import *
from constants import *
from packettypes import *
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

		elif packetType == ServerPackets.SPlayerHP:
			self.handlePlayerHP(jsonData)

		elif packetType == ServerPackets.SPlayerMP:
			self.handlePlayerMP(jsonData)

		elif packetType == ServerPackets.SPlayerSP:
			self.handlePlayerSP(jsonData)

		elif packetType == ServerPackets.SPlayerData:
			self.handlePlayerData(jsonData)

		elif packetType == ServerPackets.SPlayerMove:
			self.handlePlayerMove(jsonData)

		elif packetType == ServerPackets.SPlayerDir:
			self.handlePlayerDir(jsonData)

		elif packetType == ServerPackets.SCheckForMap:
			self.handleCheckForMap(jsonData)

		elif packetType == ServerPackets.SMapData:
			self.handleMapData(jsonData)

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

		elif packetType == ServerPackets.SEditMap:
			self.handleEditMap()

		elif packetType == ServerPackets.SMapList:
			self.handleMapList(jsonData)

		elif packetType == ServerPackets.SLeft:
			self.handleLeft(jsonData)

		elif packetType == ServerPackets.SHighIndex:
			self.handleHighIndex(jsonData)

		else:
			# Packet is unknown - hacking attempt
			print "hacking attempt"


	def handleAlertMsg(self, jsonData):
		msg = jsonData[0]['msg']

		# todo: show dialog

	def handleAllChars(self, jsonData):
		# pass it on to the character selection
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

		# TODO: FIX THIS FOR GOD SAKE
		initMapData()

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

	def handleCheckForMap(self, jsonData):
		# erase other players
		for i in range(len(Player)):
			if i != g.myIndex:
				setPlayerMap(i, 0)

		# erase temporary tiles
		clearTempTile()
		# clearMapNPCS
		# clearMapitems
		# clearMap

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
				Map.tile[x][y].ground = jsonData[i][0]["ground"]
				Map.tile[x][y].mask   = jsonData[i][0]["mask"]
				Map.tile[x][y].anim   = jsonData[i][0]["animation"]
				Map.tile[x][y].fringe = jsonData[i][0]["fringe"]
				Map.tile[x][y].type   = jsonData[i][0]["type"]
				Map.tile[x][y].data1  = jsonData[i][0]["data1"]
				Map.tile[x][y].data2  = jsonData[i][0]["data2"]
				Map.tile[x][y].data3  = jsonData[i][0]["data3"]

				i += 1

		# save map
		saveMap(jsonData[0]["mapnum"])

	def handleMapDone(self):
		calcTilePositions()

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

	def handleEditMap(self):
		''' called when server allows player to edit the map '''
		g.editor = EDITOR_MAP

		g.gameEngine.graphicsEngine.gameGUI.guiContainer.openEditor()
		g.gameEngine.graphicsEngine.gameGUI.setState(3)
		g.gameEngine.graphicsEngine.gameGUI.mapEditorGUI.init()


	def handleMapList(self, jsonData):
		''' called when receiving list of map names from server '''
		g.mapNames = jsonData[1]['mapnames']

	def handleLeft(self, jsonData):
		index = jsonData[0]["index"]
		clearPlayer(index)
		getPlayersOnMap()

	def handleHighIndex(self, jsonData):
		g.highIndex = jsonData[0]["highindex"]
		log("highIndex updated")
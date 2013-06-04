from gamelogic import *
from objects import *
import global_vars as g
from constants import *

editor = 0
editorIndex = 0

# selecting tiles
editorTileX = 0
editorTileY = 0

# map attribute data
editorData1 = 0
editorData2 = 0
editorData3 = 0

class GameEditor():
	def __init__(self, graphicsEngine):
		self.editor = 0
		self.editorIndex = 0

		# selecting tiles
		self.editorTileX = 0
		self.editorTileY = 0

		# map attribute data
		self.editorData1 = 0
		self.editorData2 = 0
		self.editorData3 = 0

		self.graphicsEngine = graphicsEngine

	def _handleEvents(self, event):
		if self.editor == EDITOR_MAP:
			print "mouse down"

	def drawMapEditor(self):
		print "test"

	#############
	# FUNCTIONS #
	#############
	def isInBounds(self):
		if g.gameEngine.graphicsEngine.surfaceRect.collidepoint((g.cursorX, g.cursorY)):
			return True

	def drawTileOutline(self):
		# TODO: Fix the game screen offset problem (-16)
		if not self.isInBounds():
			return

		x = (g.cursorX-16) / PIC_X
		y = (g.cursorY-16) / PIC_Y

		if x >= 0 and x < MAX_MAPX:
			if y >= 0 and y < MAX_MAPY:
				self.graphicsEnginesurface.blit(self.tileOutlineSurface, (MapTilePosition[x][y].x, MapTilePosition[x][y].y))


	##############
	# MAP EDITOR #
	##############

	def mapEditorInit(self):
		self.editor = EDITOR_MAP

		self.graphicsEngine.drawMapEditor()
		self.graphicsEngine.drawTileOutline()

	def mapEditorSend(self):
		g.tcpConn.sendMap()

	def mapEditorCancel(self):
		self.editor = EDITOR_NONE

	def mapEditorClearLayer(self):
		for x in range(MAX_MAPX):
			for y in range(MAX_MAPY):
				Map.tile[x][y].ground = 0
				Map.tile[x][y].mask = 0
				Map.tile[x][y].anim = 0
				Map.tile[x][y].fringe = 0

		calcTilePositions()

	def mapEditorFillLayer(self):
		for x in range(MAX_MAPX):
			for y in range(MAX_MAPY):
				Map.tile[x][y].ground = 1

		calcTilePositions()

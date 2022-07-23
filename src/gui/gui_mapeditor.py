import pygame
from pygame.locals import *
from pgu import gui

from .python_gui import *
from gamelogic import *
from objects import *
from constants import *
import global_vars as g

STATE_PROPERTIES = 0
PLACE_TILE  = 1
PLACE_BLOCK = 2
PLACE_WARP  = 3
PLACE_ITEM  = 4

UI_FONT_COLOR = (251, 230, 204)

class EmptyFieldAlertDialog(gui.Dialog):
    def __init__(self, **params):
        title = gui.Label("Error")

        t = gui.Table()

        t.tr()
        e = gui.Button('Choose map')
        t.td(e)

        e = gui.Button('Cancel')
        e.connect(gui.CLICK, self.close, None)
        t.td(e)

        t.tr()
        t.td(gui.Spacer(10, 10))

        gui.Dialog.__init__(self, title, t)

class MapSelectorDialog(gui.Dialog):
    def __init__(self, inputfield, **params):
        self.inpField = inputfield

        self._count = 1

        title = gui.Label("Map Selector")

        t = gui.Table()

        t.tr()
        t.td(gui.Label('Select a map:'), colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        self.mapList = gui.List(width=200, height=140)
        t.td(self.mapList, colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        e = gui.Button('Choose map')
        e.connect(gui.CLICK, self.setInput, None)
        t.td(e)

        e = gui.Button('Cancel')
        e.connect(gui.CLICK, self.close, None)
        t.td(e)

        t.tr()
        t.td(gui.Spacer(10, 10))

        gui.Dialog.__init__(self, title, t)

    def setInput(self, value):
        listValue = self.mapList.value

        if listValue:
            self.inpField.value = str(listValue)
            self.close()

    def openDialog(self, value):
        #self.loadMaps()
        self.open()
        self.loadMaps()

    def loadMaps(self):
        self.clearList()

        for i in range(1, len(g.mapNames)):
            if g.mapNames[i] != '':
                self.addItem(str(i) + ' - "' + str(g.mapNames[i]) + '"')

    def addItem(self, item):
        self.mapList.add(item, value=self._count)
        self.mapList.resize()
        self.mapList.repaint()
        self._count += 1

    def clearList(self):
        self.mapList.clear()
        self.mapList.resize()
        self.mapList.repaint()
        self._count = 1


class OpenItemDialog(gui.Dialog):
    def __init__(self, engine, **params):
        self.engine = engine

        self._count = 0

        title = gui.Label("Open Item")

        t = gui.Table()

        t.tr()
        t.td(gui.Label('Select an item:'), colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        self.itemList = gui.List(width=200, height=140)
        t.td(self.itemList, colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        e = gui.Button('Open item')
        e.connect(gui.CLICK, self.openItem, None)
        t.td(e)

        e = gui.Button('Cancel')
        e.connect(gui.CLICK, self.close, None)
        t.td(e)

        t.tr()
        t.td(gui.Spacer(10, 10))

        gui.Dialog.__init__(self, title, t)

    def openItem(self, value):
        listValue = self.itemList.value

        if listValue != None:
            self.engine.openItem(itemNum=listValue)
            self.close()

    def openDialog(self, value):
        self.loadItems()
        self.open()

    def loadItems(self):
        self.clearList()
        for i in range(MAX_ITEMS):
            if Item[i].name != '':
                self.addItem(str(i) + ' - "' + Item[i].name + '"')

        self.itemList.resize()
        self.itemList.repaint()

    def addItem(self, item):
        self.itemList.add(gui.Label(item), value=self._count)
        self._count += 1

    def clearList(self):
        self.itemList.clear()
        self.itemList.resize()
        self.itemList.repaint()
        self._count = 0

class OpenNPCDialog(gui.Dialog):
    def __init__(self, engine, **params):
        self.engine = engine

        self._count = 0

        title = gui.Label("Open NPC")

        t = gui.Table()

        t.tr()
        t.td(gui.Label('Select a NPC:'), colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        self.npcList = gui.List(width=200, height=140)
        t.td(self.npcList, colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        t.tr()
        e = gui.Button('Add NPC')
        e.connect(gui.CLICK, self.openNPC, None)
        t.td(e)

        e = gui.Button('Cancel')
        e.connect(gui.CLICK, self.close, None)
        t.td(e)

        t.tr()
        t.td(gui.Spacer(10, 10))

        gui.Dialog.__init__(self, title, t)

    def openNPC(self, value):
        listValue = self.npcList.value

        if listValue != None:
            self.engine.addNpc(listValue)
            self.close()

    def openDialog(self, value):
        self.loadNPCs()
        self.open()

    def loadNPCs(self):
        self.clearList()
        for i in range(MAX_NPCS):
            if NPC[i].name != '':
                self.addItem(str(i) + ' - "' + NPC[i].name + '"')

        self.npcList.resize()
        self.npcList.repaint()

    def addItem(self, item):
        self.npcList.add(gui.Label(item), value=self._count)
        self._count += 1

    def clearList(self):
        self.npcList.clear()
        self.npcList.resize()
        self.npcList.repaint()
        self._count = 0

class propertiesControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)

        self.listCount = 0

        # dialogs
        openNpcDialog = OpenNPCDialog(self)

        self.value = gui.Form()

        self.tr()
        self.td(gui.Label("Map Name:", color=UI_FONT_COLOR))
        self.td(gui.Input("", size=16, name="inpMapName"))

        self.tr()
        self.td(gui.Label("Warp Up:", color=UI_FONT_COLOR))
        self.td(gui.Input("0", size=4, name="inpMapUp"))

        self.tr()
        self.td(gui.Label("Warp Down:", color=UI_FONT_COLOR))
        self.td(gui.Input("0", size=4, name="inpMapDown"))

        self.tr()
        self.td(gui.Label("Warp Left:", color=UI_FONT_COLOR))
        self.td(gui.Input("0", size=4, name="inpMapLeft"))

        self.tr()
        self.td(gui.Label("Warp Right:", color=UI_FONT_COLOR))
        self.td(gui.Input("0", size=4, name="inpMapRight"))

        self.tr()
        self.td(gui.Spacer(10, 10))

        # npc list
        self.tr()
        e = gui.Button('Add NPC...', width=80)
        e.connect(gui.CLICK, openNpcDialog.openDialog, None)
        self.td(e)

        e = gui.Button('Remove', width=80)
        e.connect(gui.CLICK, self.removeNpc, None)
        self.td(e)

        self.tr()
        self.npcList = gui.List(width=200, height=80, name='lstNpcs')
        self.td(self.npcList, colspan=2)

        self.loadProperties()

    def loadProperties(self):
        self.value["inpMapName"].value = Map.name
        self.value["inpMapUp"].value = str(Map.up)
        self.value["inpMapDown"].value = str(Map.down)
        self.value["inpMapLeft"].value = str(Map.left)
        self.value["inpMapRight"].value = str(Map.right)

        # load npcs
        self.npcList.clear()
        for i in range(MAX_MAP_NPCS):
            if Map.npc[i] != None:
                self.npcList.add(gui.Label(str(i) + ' - "' + NPC[Map.npc[i]].name + '"'), value=Map.npc[i])

    def addNpc(self, npcNum):
        self.npcList.add(str(npcNum) + ' - "' + str(NPC[npcNum].name) + '"', value=npcNum)
        self.npcList.resize()
        self.npcList.repaint()
        self.listCount += 1

    def removeNpc(self, arg):
        item = self.npcList.value

        if item:
            self.npcList.remove(item)
            self.npcList.resize()
            self.npcList.repaint()

class placeTileControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)

        self.value = gui.Form()

        '''self.content = gui.Table()
        self.scrollArea = gui.ScrollArea(self.content, width=270, height=372, hscrollbar=False)

        self.tr()
        self.td(self.scrollArea)

        self.tr()
        g = gui.Group(name="grpTileType")

        self.content.td(gui.Label("Ground", color=UI_FONT_COLOR))
        self.content.td(gui.Spacer(10, 0))
        e = gui.Radio(g, value=1)
        e.click()
        self.content.td(e)

        self.content.tr()
        self.content.td(gui.Label("Fringe", color=UI_FONT_COLOR))
        self.content.td(gui.Spacer(10, 0))
        self.content.td(gui.Radio(g, value=2))

        '''

        self.tr()
        g = gui.Group(name="grpTileType")

        self.td(gui.Label("Ground", color=UI_FONT_COLOR))
        self.td(gui.Spacer(10, 0))
        e = gui.Radio(g, value=1)
        e.click()
        self.td(e)

        self.tr()
        self.td(gui.Label("Fringe", color=UI_FONT_COLOR))
        self.td(gui.Spacer(10, 0))
        self.td(gui.Radio(g, value=2))

        e = gui.Select(name='selTileType')
        e.add('Layer 1', 0)
        e.add('Layer 2', 1)
        e.add('Layer 3', 2)
        e.add('Fringe', 3)
        e.value = 0
        self.td(e)
        

class placeBlockControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)

        self.value = gui.Form()

        self.tr()
        label = gui.Label("Left click to add block", color=UI_FONT_COLOR)
        self.td(label)

        self.tr()
        label = gui.Label("Right click to remove block", color=UI_FONT_COLOR)
        self.td(label)


class placeWarpControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)

        self.value = gui.Form()

        self.tr()
        self.td(gui.Label("Map ID: ", color=UI_FONT_COLOR), colspan=2)

        self.tr()
        self.inpMapID = gui.Input('0', size=8, name='inpWarpMapID')
        self.td(self.inpMapID, colspan=2)

        # used for selecting the map - todo
        mapDialog = MapSelectorDialog(self.inpMapID)

        self.tr()
        e = gui.Button('Choose map...')
        e.connect(gui.CLICK, mapDialog.openDialog, None)
        self.td(e, colspan=2)

        self.tr()
        self.td(gui.Spacer(10, 20))

        self.tr()
        self.td(gui.Label("Warp-To Position", color=UI_FONT_COLOR), colspan=2)

        self.tr()
        self.td(gui.Label("X: ", color=UI_FONT_COLOR))
        self.td(gui.Input("0", size=4, name="inpWarpX"))

        self.tr()
        self.td(gui.Label("Y: ", color=UI_FONT_COLOR))
        self.td(gui.Input("0", size=4, name="inpWarpY"))

        self.tr()
        self.td(gui.Spacer(10, 20))

        self.tr()
        label = gui.Label("Left click to add warp", color=UI_FONT_COLOR)
        self.td(label, colspan=2)

        self.tr()
        label = gui.Label("Right click to remove warp", color=UI_FONT_COLOR)
        self.td(label, colspan=2)

        # initialize the alert dialog
        self.alertDialog = EmptyFieldAlertDialog()


class placeItemControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)

        self.value = gui.Form()

        # item information
        self.itemNum = 0
        self.itemVal = 0

        # dialogs
        openItemDialog = OpenItemDialog(self)

        self.tr()
        e = gui.Button("Open item...", width=100)
        e.connect(gui.CLICK, openItemDialog.openDialog, None)
        self.td(e)

        self.tr()
        self.td(gui.Spacer(10, 20))

        self.tr()
        self.td(gui.Label('Select an item to spawn', color=UI_FONT_COLOR, name='lblItemName'))

        self.tr()
        self.td(gui.Spacer(10, 80))

    def openItem(self, itemNum):
        # redraw selected sprite
        #g.gameEngine.graphicsEngine.gameGUI.itemEditorGUI.selectedSpriteNum = Item[itemNum].pic
        #g.gameEngine.graphicsEngine.gameGUI.itemEditorGUI.draw()

        if self.find('lblItemName'):
            self.value['lblItemName'].set_text(Item[itemNum].name)

        # set type and data
        typeValue = Item[itemNum].type

        if typeValue == ITEM_TYPE_CURRENCY:
            # do stuff
            print("todo: add value scroller")

        # update item num
        self.itemNum = itemNum
        self.itemVal = 0


class MapEditorContainer(gui.Container):
    def __init__(self, engine, **params):
        gui.Container.__init__(self, **params)

        self.engine = engine

        # menus
        self.propertiesCtrl = propertiesControl(name="propertiesCtrl")
        self.tileCtrl       = placeTileControl(name="tileCtrl")
        self.blockCtrl      = placeBlockControl(name="blockCtrl")
        self.warpCtrl       = placeWarpControl(name="warpCtrl")
        self.itemCtrl       = placeItemControl(name='itemCtrl')

        # menu title
        self.tTitle = gui.Table(width=272, height=32)

        self.tTitle.tr()
        self.tTitle.td(gui.Label("Map Editor", name='mapTitle', color=UI_FONT_COLOR))

        # buttons
        self.t = gui.Table(width=272, height=50)

        self.t.tr()
        e = gui.Button("Map Properties", width=200)
        e.connect(gui.CLICK, self.toggleProperties, None)
        self.t.td(e, colspan=4)

        self.t.tr()
        e = gui.Button("Tile", width=40)
        e.connect(gui.CLICK, self.toggleTile, None)
        self.t.td(e)

        e = gui.Button("Block", width=40)
        e.connect(gui.CLICK, self.toggleBlock, None)
        self.t.td(e)

        e = gui.Button("Warp", width=40)
        e.connect(gui.CLICK, self.toggleWarp, None)
        self.t.td(e)

        e = gui.Button("Item", width=40)
        e.connect(gui.CLICK, self.toggleItem, None)
        self.t.td(e)

        self.tContent = gui.Table(width=272, height=318)

        self.tBottom = gui.Table(width=272, height=200)

        self.tBottom.tr()
        e = gui.Button("Save", width=100, height=40)
        e.connect(gui.CLICK, self.saveMap, None)
        self.tBottom.td(e)

        e = gui.Button("Cancel", width=100, height=40)
        e.connect(gui.CLICK, self.cancelMap, None)
        self.tBottom.td(e)

        #self.t.td()

        self.add(self.tTitle, 0, 0)
        self.add(self.t, 0, 48)
        self.add(self.tContent, 0, 110)
        self.add(self.tBottom, 0, 368)

    def saveMap(self, value):
        # save properties
        Map.name  = self.propertiesCtrl.value["inpMapName"].value
        Map.up    = int(self.propertiesCtrl.value["inpMapUp"].value)
        Map.down  = int(self.propertiesCtrl.value["inpMapDown"].value)
        Map.left  = int(self.propertiesCtrl.value["inpMapLeft"].value)
        Map.right = int(self.propertiesCtrl.value["inpMapRight"].value)

        # retrieve the npcs from the list
        npcList = []
        for item in self.propertiesCtrl.value['lstNpcs'].items:
            npcList.append(item.value)

        # add them to the map
        for i in range(MAX_MAP_NPCS):
            try:
                Map.npc[i] = npcList[i]
            except:
                Map.npc[i] = None

        # send the map
        g.tcpConn.sendMap()

        # quit editor
        self.toggleProperties(None)
        self.quitEditor()

    def getTileType(self):
        return self.tileCtrl.value['selTileType'].value

    def cancelMap(self, value):
        self.toggleProperties(None)
        self.quitEditor()

    def quitEditor(self):
        g.gameEngine.graphicsEngine.gameGUI.setState(0)
        g.gameEngine.graphicsEngine.gameGUI.guiContainer.closeEditor()
        g.editor = EDITOR_NONE
        loadMap(getPlayerMap(g.myIndex))
        initMapData()
        g.canMoveNow = True

    def hideAll(self):
        if self.tContent.find("propertiesCtrl"):
            self.tContent.remove(self.tContent.find("propertiesCtrl"))

        if self.tContent.find("tileCtrl"):
            self.tContent.remove(self.tContent.find("tileCtrl"))

        if self.tContent.find("blockCtrl"):
            self.tContent.remove(self.tContent.find("blockCtrl"))

        if self.tContent.find("warpCtrl"):
            self.tContent.remove(self.tContent.find("warpCtrl"))

        if self.tContent.find("itemCtrl"):
            self.tContent.remove(self.tContent.find("itemCtrl"))

    def toggleProperties(self, value):
        self.engine.setState(None)
        self.engine.draw()

        self.hideAll()
        self.tContent.tr()
        self.tContent.td(self.propertiesCtrl, valign=-1)
        self.propertiesCtrl.loadProperties()

    def toggleTile(self, value):
        self.engine.setState(PLACE_TILE)
        self.engine.draw()

        self.hideAll()
        self.tContent.tr()
        self.tContent.td(self.tileCtrl, valign=-1)

    def toggleBlock(self, value):
        self.engine.setState(PLACE_BLOCK)
        self.engine.draw()

        self.hideAll()
        self.tContent.tr()
        self.tContent.td(self.blockCtrl, valign=-1)

    def toggleWarp(self, value):
        self.engine.setState(PLACE_WARP)
        self.engine.draw()

        self.hideAll()
        self.tContent.tr()
        self.tContent.td(self.warpCtrl, valign=-1)

    def toggleItem(self, value):
        self.engine.setState(PLACE_ITEM)
        self.engine.draw()

        self.hideAll()
        self.tContent.tr()
        self.tContent.td(self.itemCtrl, valign=-1)


class MapEditorGUI():
    ''' the map editor gui '''

    def __init__(self, surface):
        self.surface = surface

        self.state = PLACE_TILE

        # todo: remove this
        self.gameSurfaceRect = g.gameSurface.get_rect()
        self.gameSurfaceRect.top = 16
        self.gameSurfaceRect.left = 16

        ##############
        # PLACE TILE #
        ##############

        # selected tile
        self.selectedTileX = 0
        self.selectedTileY = 0
        self.selectedTileSurface = pygame.Surface((PIC_X, PIC_Y))
        self.selectedTileRect = pygame.Rect((632, 175, 32, 32))

        # tileset
        self.tilesetOffsetX = 0
        self.tilesetOffsetY = 0

        self.tilesetImg = pygame.image.load(g.dataPath + '/tilesets/Tiles1.png').convert()
        self.tilesetImgRect = self.tilesetImg.get_rect()

        self.tilesetSurfaceRect = pygame.Rect((540, 212, PIC_X*6, PIC_Y*4))

        # scroll buttons
        # - scroll buttons (place them near self.tileSurfaceRect)
        btnScrollLeft = pygButton((self.tilesetSurfaceRect.x, (self.tilesetSurfaceRect.y+self.tilesetSurfaceRect.height), 32, 32), fgcolor=(255, 255, 255), normal=g.dataPath + '/themes/default/hslider.left.tga')
        btnScrollRight = pygButton((self.tilesetSurfaceRect.x + (self.tilesetSurfaceRect.width-16), (self.tilesetSurfaceRect.y+self.tilesetSurfaceRect.height), 32, 32), fgcolor=(255, 255, 255), normal=g.dataPath + '/themes/default/hslider.right.tga')
        btnScrollUp = pygButton((self.tilesetSurfaceRect.x + (self.tilesetSurfaceRect.width), self.tilesetSurfaceRect.y, 32, 32), fgcolor=(255, 255, 255), normal=g.dataPath + '/themes/default/vslider.up.tga')
        btnScrollDown = pygButton((self.tilesetSurfaceRect.x + (self.tilesetSurfaceRect.width), (self.tilesetSurfaceRect.y+self.tilesetSurfaceRect.height-16), 32, 32), fgcolor=(255, 255, 255), normal=g.dataPath + '/themes/default/vslider.down.tga')

        self.tileButtons = (btnScrollLeft, btnScrollRight, btnScrollUp, btnScrollDown)

    def init(self):
        self.setState(STATE_PROPERTIES)

        # set PROPERTIES ctrl as default
        g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.toggleProperties(None)

        # write hotkeys
        addText('Tip: Hold SHIFT while placing a tile to fill the whole layer.', textColor.YELLOW)
        addText('Tip: Hold CTRL while removing a tile to clear the whole layer.', textColor.YELLOW)

        self.draw()

    def draw(self):
        g.gameEngine.graphicsEngine.gameGUI.reset()

        if self.state == PLACE_TILE:
            self.surface.blit(self.selectedTileSurface, self.selectedTileRect)
            self.surface.blit(self.tilesetImg, self.tilesetSurfaceRect, (self.tilesetOffsetX, self.tilesetOffsetY, self.tilesetSurfaceRect.width, self.tilesetSurfaceRect.height))

            self.drawElements()

    def drawElements(self):
        # todo: this is required to keep performance low (only update elements)
        if self.state == PLACE_TILE:
            for button in self.tileButtons:
                button.draw(self.surface)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            # mouse scroll down
            if self.tilesetOffsetY < (self.tilesetImgRect.height - self.tilesetSurfaceRect.height):
                self.tilesetOffsetY += PIC_Y
            self.draw()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            # mouse scroll up
            if self.tilesetOffsetY > 0:
                self.tilesetOffsetY -= PIC_Y
            self.draw()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # mouse click
            self.handleMouseDown(event)

        if self.state == PLACE_TILE:
            if 'click' in self.tileButtons[0].handleEvents(event):
                # scroll to the left
                if self.tilesetOffsetX > 0:
                    self.tilesetOffsetX -= PIC_X

                self.draw()

            if 'click' in self.tileButtons[1].handleEvents(event):
                # scroll to the right
                if self.tilesetOffsetX < (self.tilesetImgRect.width - self.tilesetSurfaceRect.width):
                    self.tilesetOffsetX += PIC_X

                self.draw()

            if 'click' in self.tileButtons[2].handleEvents(event):
                # scroll up
                if self.tilesetOffsetY > 0:
                    self.tilesetOffsetY -= PIC_Y

                self.draw()

            if 'click' in self.tileButtons[3].handleEvents(event):
                # scroll down
                if self.tilesetOffsetY < (self.tilesetImgRect.height - self.tilesetSurfaceRect.height):
                    self.tilesetOffsetY += PIC_Y

                self.draw()

    def fillLayer(self):
        ''' fills the layer with the currently selected tile '''
        if g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 0:
            for x in range(MAX_MAPX):
                for y in range(MAX_MAPY):
                    Map.tile[x][y].layer1 = self.selectedTileY * TILESHEET_WIDTH + self.selectedTileX

        elif g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 1:
            for x in range(MAX_MAPX):
                for y in range(MAX_MAPY):
                    Map.tile[x][y].layer2 = self.selectedTileY * TILESHEET_WIDTH + self.selectedTileX

        elif g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 2:
            for x in range(MAX_MAPX):
                for y in range(MAX_MAPY):
                    Map.tile[x][y].layer3 = self.selectedTileY * TILESHEET_WIDTH + self.selectedTileX

        elif g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 3:
            for x in range(MAX_MAPX):
                for y in range(MAX_MAPY):
                    Map.tile[x][y].fringe = self.selectedTileY * TILESHEET_WIDTH + self.selectedTileX

        calcTilePositions()
        g.gameEngine.graphicsEngine.redrawMap()

    def clearLayer(self):
        ''' clears the layer '''
        if g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 0:
            for x in range(MAX_MAPX):
                for y in range(MAX_MAPY):
                    Map.tile[x][y].layer1 = None

        elif g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 1:
            for x in range(MAX_MAPX):
                for y in range(MAX_MAPY):
                    Map.tile[x][y].layer2 = None

        elif g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 2:
            for x in range(MAX_MAPX):
                for y in range(MAX_MAPY):
                    Map.tile[x][y].layer3 = None

        # fill fringe layer
        elif g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 3:
            for x in range(MAX_MAPX):
                for y in range(MAX_MAPY):
                    Map.tile[x][y].fringe = None

        calcTilePositions()
        g.gameEngine.graphicsEngine.redrawMap()

    def handleMouseDown(self, event):
        # todo: better mouse rightclick/leftclick
        # todo: the linking to g.gameEngine.graphicsEngine.gameGUI blabhalbha is WAY too stupid
        if not self.isInBounds(self.tilesetSurfaceRect) and not self.isInBounds(self.gameSurfaceRect):
            return

        if self.isInBounds(self.tilesetSurfaceRect):
            self.chooseTile(g.cursorX, g.cursorY)
            self.draw()

        elif self.isInBounds(self.gameSurfaceRect):
            if event.button == 1:
                # TODO: Fix the game screen offset problem (-16)
                x = (g.cursorX-16) // PIC_X
                y = (g.cursorY-16) // PIC_Y

                if self.state == PLACE_TILE:

                    # check if shift is down
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        self.fillLayer()
                        return

                    if g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 0:
                        Map.tile[x][y].layer1 = self.selectedTileY * TILESHEET_WIDTH + self.selectedTileX

                    elif g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 1:
                        Map.tile[x][y].layer2 = self.selectedTileY * TILESHEET_WIDTH + self.selectedTileX

                    elif g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 2:
                        Map.tile[x][y].layer3 = self.selectedTileY * TILESHEET_WIDTH + self.selectedTileX

                    elif g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 3:
                        Map.tile[x][y].fringe = self.selectedTileY * TILESHEET_WIDTH + self.selectedTileX

                    calcTilePositions()

                else:
                    # clear data
                    Map.tile[x][y].type = 0
                    Map.tile[x][y].data1 = 0
                    Map.tile[x][y].data2 = 0
                    Map.tile[x][y].data3 = 0

                    if self.state == PLACE_BLOCK:
                        Map.tile[x][y].type = TILE_TYPE_BLOCKED

                    elif self.state == PLACE_WARP:
                        Map.tile[x][y].type = TILE_TYPE_WARP
                        Map.tile[x][y].data1 = int(g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.warpCtrl.value["inpWarpMapID"].value)
                        Map.tile[x][y].data2 = int(g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.warpCtrl.value["inpWarpX"].value)
                        Map.tile[x][y].data3 = int(g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.warpCtrl.value["inpWarpY"].value)

                    elif self.state == PLACE_ITEM:
                        Map.tile[x][y].type = TILE_TYPE_ITEM
                        Map.tile[x][y].data1 = int(g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.itemCtrl.itemNum)
                        Map.tile[x][y].data2 = int(g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.itemCtrl.itemVal)
                        Map.tile[x][y].data3 = 0

            elif event.button == 3:
                x = (g.cursorX-16) // PIC_X
                y = (g.cursorY-16) // PIC_Y

                if self.state == PLACE_TILE:
                    if pygame.key.get_mods() & KMOD_CTRL:
                        self.clearLayer()
                        return

                    # remove tile
                    if g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 0:
                        Map.tile[x][y].layer1 = None

                    elif g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 1:
                        Map.tile[x][y].layer2 = None

                    elif g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 2:
                        Map.tile[x][y].layer3 = None

                    elif g.gameEngine.graphicsEngine.gameGUI.guiContainer.mapEditorControl.getTileType() == 3:
                        Map.tile[x][y].fringe = None

                    calcTilePositions()

                else:
                    Map.tile[x][y].type = 0
                    Map.tile[x][y].data1 = 0
                    Map.tile[x][y].data2 = 0
                    Map.tile[x][y].data3 = 0

            # assume something has happened, so redraw map
            g.gameEngine.graphicsEngine.redrawMap()

    def setState(self, state):
        self.state = state
        #g.gameEngine.graphicsEngine.gameGUI.reset()

    def isInBounds(self, surfaceRect):
        if surfaceRect.collidepoint((g.cursorX, g.cursorY)):
            return True

    def chooseTile(self, x, y):
        self.selectedTileX = (x - self.tilesetSurfaceRect.x + self.tilesetOffsetX) // PIC_X
        self.selectedTileY = (y - self.tilesetSurfaceRect.y + self.tilesetOffsetY) // PIC_Y

        self.selectedTileSurface.blit(self.tilesetImg, (0, 0), (self.selectedTileX * PIC_X, self.selectedTileY * PIC_Y, 32, 32))

    def quit(self):
        ''' quits the map editor '''
        # todo: dont use g.gameEngine...
        g.gameEngine.graphicsEngine.gameGUI.setState(0)

        g.editor = EDITOR_NONE
        loadMap(getPlayerMap(g.myIndex))
        print("load map?")
        initMapData()

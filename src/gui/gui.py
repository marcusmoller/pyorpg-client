import pygame
from pygame.locals import *
from pgu import gui

from gamelogic import *
from network.database import *
from objects import *
from constants import *
import global_vars as g
from utils.utils import countFiles

from .gui_mapeditor import MapEditorContainer, MapEditorGUI
from .gui_itemeditor import ItemEditorContainer, ItemEditorGUI
from .gui_spelleditor import SpellEditorContainer, SpellEditorGUI
from .gui_npceditor import NPCEditorContainer, NPCEditorGUI

# gui states
GUI_STATS = 0
GUI_INVENTORY = 1
GUI_SPELLBOOK = 2

GUI_MAPEDITOR = 3
GUI_ITEMEDITOR = 4
GUI_NPCEDITOR = 5
GUI_SPELLEDITOR = 6
GUI_SHOPEDITOR = 7

class QuitDialog(gui.Dialog):
    def __init__(self, **params):
        title = gui.Label(_("Exit Game"))

        t = gui.Table()

        t.tr()
        t.td(gui.Label(_("Are you sure you want to quit?")), colspan=2)

        t.tr()
        t.td(gui.Spacer(10, 20))

        def btnQuit(value):
            g.gameEngine.quitGame()

        t.tr()
        e = gui.Button(_("Quit"))
        e.connect(gui.CLICK, btnQuit, None)
        t.td(e)

        e = gui.Button(_("Cancel"))
        e.connect(gui.CLICK, self.close, None)
        t.td(e)

        t.tr()
        t.td(gui.Spacer(10, 10))

        gui.Dialog.__init__(self, title, t)


class ChatControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)
        self.value = gui.Form()
        self.engine = None

        self._data = ''

        self._count = 1
        self.focused = False

        def clickChatMsg(value):
            # disable movement when chat msg is mouse clicked
            if self.focused:
                self.focused = False
            else:
                self.focused = True

            g.canMoveNow = False

        self.tr()
        self.chatMsg = gui.Input(maxlength=128, width=468, focusable=False)
        self.chatMsg.connect(gui.CLICK, clickChatMsg, None)
        self.chatMsg.connect(gui.KEYDOWN, self.lkey)
        self.td(self.chatMsg)

        self.tr()
        self.chatList = gui.Table()
        self.box = gui.ScrollArea(self.chatList, width=480, height=172, hscrollbar=False)
        self.td(self.box)

        self.tr()

        class Hack(gui.Spacer):
            def __init__(self, box):
                super(gui.Spacer, self).__init__()
                self.box = box

            def resize(self, width=None, height=None):
                self.box.set_vertical_scroll(65535)
                return 1, 1

        dirtyHack = Hack(self.box)
        self.td(dirtyHack)

    def lkey(self, _event):
        e = _event

        if e.key == K_RETURN:
            if self.chatMsg.value != '':
                handleMsg(self.chatMsg.value)
                self.chatMsg.value = ''

                g.canMoveNow = True

    def addText(self, text, color=(0, 0, 0)):
        def write(text, color):
            self.chatList.tr()
            self.chatList.td(gui.Label(str(text), antialias=0, color=color, font=g.chatFont), align=-1)
            self.box.resize()

        # check if textlength is greater than the chat list length
        textLength = g.chatFont.size(text)[0]

        if textLength > 459:
            # todo: allow custom size chat list (459 is found with GIMP)
            # todo: optimize the loop

            lines = ['']

            words = text.split()
            curLine = 0
            curLineLength = 0

            for i in range(len(words)):
                word = words[i]

                # if adding the new word to the current line would be too long,
                # then put it on a new line
                wordLength = g.chatFont.size(word)[0]

                if (curLineLength + wordLength) > 400: # todo: why does it only work with 400?

                    # only move down to a new line if we have text on the current line
                    lines.append('')
                    curLine += 1
                    curLineLength = 0

                lines[curLine] += word + ' '
                curLineLength += wordLength

            for line in lines:
                write(line, color)

        else:
            # text fits, so just print it
            write(text, color)

    def clearChat(self):
        print("todo")


class uiContainer(gui.Container):
    def __init__(self, engine, **params):
        gui.Container.__init__(self, **params)

        self.engine = engine

        # menu title
        self.tTitle = gui.Table(width=272, height=32)

        # navigation
        self.tBottom = gui.Table(width=272, height=200)

        self.tBottom.tr()
        e = gui.Button(_("Stats"), width=100, height=40)
        e.connect(gui.CLICK, self.toggleStats, None)
        self.tBottom.td(e)
        e = gui.Button(_("Inventory"), width=100, height=40)
        e.connect(gui.CLICK, self.toggleInventory, None)
        self.tBottom.td(e)

        self.tBottom.tr()
        e = gui.Button(_('Spellbook'), width=100, height=40)
        e.connect(gui.CLICK, self.toggleSpellbook, None)
        self.tBottom.td(e, colspan=2)

        self.tBottom.tr()
        e = gui.Button(_('Settings'), width=100, height=40)
        e.connect(gui.CLICK, self.toggleSettings, None)
        self.tBottom.td(e, colspan=2)

        self.add(self.tTitle, 0, 0)
        self.add(self.tBottom, 0, 368)

        # default UI view, todo
        #self.toggleStats()

    def toggleStats(self, value=0):
        self.engine.setState(GUI_STATS)

        plrName = getPlayerName(g.myIndex)

        self.updateTitle(plrName)

    def toggleInventory(self, value):
        self.engine.setState(GUI_INVENTORY)
        self.updateTitle(_('Inventory'))

    def toggleSpellbook(self, value):
        self.engine.setState(GUI_SPELLBOOK)
        self.updateTitle(_('Spellbook'))
        g.tcpConn.sendRequestSpells()

    def toggleSettings(self, value):
        self.engine.setState(GUI_STATS)
        self.updateTitle(_('Settings'))

    def updateTitle(self, title, titleColor=(251, 230, 204)):
        if self.tTitle.find('uiTitle'):
            self.tTitle.remove(self.tTitle.find('uiTitle'))

        self.tTitle.tr()
        self.tTitle.td(gui.Label(title, name='uiTitle', color=titleColor))


class GUIContainer(gui.Container):
    def __init__(self, engine, **params):
        gui.Container.__init__(self, **params)

        self.engine = engine

        self.chatCtrl = ChatControl(name="chatCtrl")
        self.uiCtrl = uiContainer(self.engine, name="uiCtrl")

        self.mapEditorControl = MapEditorContainer(self.engine.mapEditorGUI, name="mapEditorCtrl")
        self.itemEditorControl = ItemEditorContainer(self.engine.itemEditorGUI, name='itemEditorCtrl')
        self.spellEditorControl = SpellEditorContainer(self.engine.spellEditorGUI, name='spellEditorCtrl')
        self.npcEditorControl = NPCEditorContainer(self.engine.npcEditorGUI, name='npcEditorCtrl')

        # default controls
        self.add(self.chatCtrl, 16, 384)
        self.add(self.uiCtrl, 512, 16)

    # map editor
    def openEditor(self, value=0):
        self.add(self.mapEditorControl, 512, 16)
        g.canMoveNow = False

        # close ui
        self.remove(self.find("uiCtrl"))

    def closeEditor(self, value=0):
        self.remove(self.find("mapEditorCtrl"))

        # add ui
        self.add(self.uiCtrl, 512, 16)

    # item editor
    def openItemEditor(self, value=0):
        self.add(self.itemEditorControl, 512, 16)
        g.canMoveNow = False

        # close ui
        self.remove(self.find('uiCtrl'))

    def closeItemEditor(self, value=0):
        self.remove(self.find('itemEditorCtrl'))

        # add ui
        self.add(self.uiCtrl, 512, 16)

    # spell editor
    def openSpellEditor(self, value=0):
        self.add(self.spellEditorControl, 512, 16)
        self.engine.spellEditorGUI.init()
        g.canMoveNow = False

        # close ui
        self.remove(self.find('uiCtrl'))

    def closeSpellEditor(self, value=0):
        self.remove(self.find('spellEditorCtrl'))

        # add ui
        self.add(self.uiCtrl, 512, 16)

    # npc editor
    def openNpcEditor(self, value=0):
        self.add(self.npcEditorControl, 512, 16)
        g.canMoveNow = False

        # close ui
        self.remove(self.find('uiCtrl'))

    def closeNpcEditor(self, value=0):
        self.remove(self.find('npcEditorCtrl'))

        # add ui
        self.add(self.uiCtrl, 512, 16)

    def updateEngines(self):
        # dirty hack
        self.uiCtrl.engine = self.engine


class GameGUI():
    def __init__(self, graphicsEngine):
        self.graphicsEngine = graphicsEngine
        self.state = GUI_STATS

        self.background = pygame.image.load(g.dataPath + '/gui/bg_ingame.png')
        g.guiSurface.blit(self.background, (0, 0))

        # events
        self.pressedKeys = []

        # inventory boxes
        self.inventoryBoxes = []
        for y in range(0, 3):
            for x in range(0, 3):
                self.inventoryBoxes.append(pygame.Rect((524 + x*(66+24) + 1, 90 + y*(66+24) + 1, 64, 64)))

        self.emptySlotSurface = pygame.image.load(g.dataPath + '/gui/empty_slot.png').convert_alpha()

        # spellbook boxes
        # inventory boxes
        self.spellbookBoxes = []
        for y in range(0, 3):
            for x in range(0, 3):
                self.spellbookBoxes.append(pygame.Rect((524 + x*(66+24) + 1, 90 + y*(66+24) + 1, 64, 64)))

        # inventory tooltip
        self.tooltipRect = pygame.Rect((0, 0, 128, 64))

        # game GUIs
        self.mapEditorGUI = MapEditorGUI(g.guiSurface)
        self.itemEditorGUI = ItemEditorGUI(g.guiSurface)
        self.spellEditorGUI = SpellEditorGUI(g.guiSurface)
        self.npcEditorGUI = NPCEditorGUI(g.guiSurface)

        # GUI
        self.app = gui.App()

        self.guiContainer = GUIContainer(self, align=-1, valign=-1)
        self.guiContainer.updateEngines()

        self.app.init(self.guiContainer)

        # dialogs
        self.quitDialog = QuitDialog()

        # dirty
        self.isDirty = True

        # init
        self.itemSprites = []
        self.spellSprites = []
        self.loadSprites()

    def loadSprites(self):
        spritesAmount = countFiles(g.dataPath + '/items/')

        for i in range(spritesAmount):
            tempImage = pygame.image.load(g.dataPath + '/items/' + str(i) + '.png').convert_alpha()
            self.itemSprites.append(tempImage)

        spritesAmount = countFiles(g.dataPath + '/spells/')

        for i in range(spritesAmount):
            tempImage = pygame.image.load(g.dataPath + '/spells/' + str(i) + '.bmp').convert()
            self.spellSprites.append(tempImage)

    def setState(self, state):
        ''' sets UI engine state '''
        self.state = state
        self.reset()

    def setUIState(self, state):
        ''' sets UI rendering state '''
        if state == GUI_INVENTORY:
            self.guiContainer.uiCtrl.toggleInventory(0)


    def draw(self, surface, surfaceRect):
        # surface and surfaceRect is a part of a stupid hack. See graphics.py

        # render ui (SHOULD BE REMOVED DUE TO CPU USAGE)
        #g.guiSurface.blit(self.background, (0, 0))
        self.drawUI()

        # part of the hack. game map is blitted so that the gui (app.paint) is ABOVE the game screen
        g.screenSurface.blit(surface, surfaceRect)

        # render gui
        self.app.paint()

    def update(self, event):
        def pressed(key):
            keys = pygame.key.get_pressed()

            if keys[key]:
                return True
            else:
                return False

        self.app.event(event)
        #self.graphicsEngine.dirtyRects = self.app.update()

        if event.type == KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(self.guiContainer.chatCtrl.focused)
                if self.guiContainer.chatCtrl.focused == False:
                    self.guiContainer.chatCtrl.chatMsg.focus()
                    self.guiContainer.chatCtrl.focused = True
                    g.canMoveNow = False
                elif self.guiContainer.chatCtrl.focused == True:
                    self.guiContainer.chatCtrl.chatMsg.blur()
                    self.guiContainer.chatCtrl.focused = False
                    g.canMoveNow = True

            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                if self.guiContainer.chatCtrl.focused == False:
                    if not self.quitDialog.is_open():
                        self.quitDialog.open()

        if self.state == GUI_STATS or self.state == GUI_INVENTORY or self.state == GUI_SPELLBOOK:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # mouse click
                self.handleMouseTargetClick(event.button)

        if self.state == GUI_INVENTORY:
            # show item information
            for i in range(len(self.inventoryBoxes)):
                if self.inventoryBoxes[i].collidepoint(g.cursorX, g.cursorY):

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # mouse click
                        self.handleInventoryMouseClick(event.button, i)

        elif self.state == GUI_SPELLBOOK:
            # show item information
            for i in range(len(self.spellbookBoxes)):
                if self.spellbookBoxes[i].collidepoint(g.cursorX, g.cursorY):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for key in g.SPELLBOOK_HOTKEYS.keys():
                            if pressed(key):
                                setSpellbookHotkey(i, key)

                        # mouse click
                        self.handleSpellbookMouseClick(event.button, i)

        elif self.state == GUI_MAPEDITOR:
            self.mapEditorGUI.update(event)

        elif self.state == GUI_ITEMEDITOR:
            self.itemEditorGUI.update(event)

        elif self.state == GUI_SPELLEDITOR:
            self.spellEditorGUI.update(event)

        elif self.state == GUI_NPCEDITOR:
            self.npcEditorGUI.update(event)

    def handleMouseTargetClick(self, button):
        # left click - target npc/player
        if button == 1:
            # make sure we are clicking inside the game
            if g.gameSurface.get_rect().collidepoint((g.cursorX, g.cursorY)):
                # calculate mouse tile pos
                x = (g.cursorX-16) // PIC_X
                y = (g.cursorY-16) // PIC_Y

                # find target
                findTarget(x, y)

                return

    def handleInventoryMouseClick(self, button, invNum):
        # right click - use inventory item
        if button == 3:
            g.tcpConn.sendUseItem(invNum)
            return

    def handleSpellbookMouseClick(self, button, spellNum):
        # right click - cast spell
        if button == 3:
            castSpell(spellNum)
            return

    ##############
    # INTERFACES #
    ##############

    def reset(self):
        ''' resets the whole surface '''
        g.guiSurface.blit(self.background, (0, 0))
        self.drawUI()

    def drawUI(self):
        ''' renders the ui depending on the menu state '''
        if self.state == GUI_STATS:
            self.drawStats()
            self.drawEquipment()

        elif self.state == GUI_INVENTORY:
            g.guiSurface.blit(self.background, (513, 17), (513, 17, 274, 365))

            # todo: render the empty slots once
            self.drawInventorySlots()

            self.drawInventoryUI()

        elif self.state == GUI_SPELLBOOK:
            g.guiSurface.blit(self.background, (513, 17), (513, 17, 274, 365))

            # todo: render the empty slots once
            self.drawSpellbookSlots()

            self.drawSpellbookUI()

        # EDITORS

        elif self.state == GUI_MAPEDITOR:
            #self.mapEditorGUI.draw()
            self.mapEditorGUI.drawElements()

        elif self.state == GUI_ITEMEDITOR:
            self.itemEditorGUI.drawElements()

        elif self.state == GUI_NPCEDITOR:
            self.npcEditorGUI.drawElements()

        elif self.state == GUI_SPELLEDITOR:
            self.spellEditorGUI.drawElements()

        g.screenSurface.blit(g.guiSurface, (0, 0))

    def drawStats(self):
        ''' the stats interface '''
        self.drawHealthBar()
        self.drawManaBar()
        self.drawLevelText()
        self.drawStatText()
        self.drawStatIcons()

    def drawInventoryUI(self):
        ''' the inventory interface '''
        #self.drawGold()
        self.drawInventory()

        for i in range(len(self.inventoryBoxes)):
            if self.inventoryBoxes[i].collidepoint(g.cursorX, g.cursorY):
                self.drawInventoryTooltip(i)

    def drawSpellbookUI(self):
        self.drawSpellbook()

        for i in range(len(self.spellbookBoxes)):
            if self.spellbookBoxes[i].collidepoint(g.cursorX, g.cursorY):
                self.drawSpellbookTooltip(i)

    #############
    # FUNCTIONS #
    #############

    def drawLevelText(self):
        font = g.nameFont
        fontColor = (251, 230, 204)

        label = font.render('Level ' + str(getPlayerLevel(g.myIndex)) + ' (' + str(getPlayerExp(g.myIndex)) +'/' + str(g.expToNextLvl) + ')', 0, fontColor)
        labelRect = label.get_rect()
        labelRect.centerx = 648
        labelRect.centery = 130
        g.guiSurface.blit(label, labelRect)

    def drawStatText(self):
        font = g.nameFont
        fontColor = (251, 230, 204)

        label = font.render('STR - ' + str(getPlayerStat(g.myIndex, Stats.strength)), 0, fontColor)
        labelRect = label.get_rect()
        labelRect.centerx = 590
        labelRect.centery = 150
        g.guiSurface.blit(label, labelRect)

        label = font.render('DEF - ' + str(getPlayerStat(g.myIndex, Stats.defense)), 0, fontColor)
        labelRect = label.get_rect()
        labelRect.centerx = 590
        labelRect.centery = 170
        g.guiSurface.blit(label, labelRect)

        label = font.render('SPD - ' + str(getPlayerStat(g.myIndex, Stats.speed)), 0, fontColor)
        labelRect = label.get_rect()
        labelRect.centerx = 705
        labelRect.centery = 150
        g.guiSurface.blit(label, labelRect)

        label = font.render('MAG - ' + str(getPlayerStat(g.myIndex, Stats.magic)), 0, fontColor)
        labelRect = label.get_rect()
        labelRect.centerx = 705
        labelRect.centery = 170
        g.guiSurface.blit(label, labelRect)

    def drawStatIcons(self):
        attributeStrength = pygame.image.load(g.dataPath + '/gui/attribute_strength.png').convert_alpha()
        attributeDefense = pygame.image.load(g.dataPath + '/gui/attribute_defense.png').convert_alpha()

        # calculate positions
        strRect = attributeStrength.get_rect()
        strRect.centerx = 590 - 50
        strRect.centery = 150

        defRect = attributeDefense.get_rect()
        defRect.centerx = 590 - 50
        defRect.centery = 170

        # render it all
        g.guiSurface.blit(attributeStrength, strRect)
        g.guiSurface.blit(attributeDefense, defRect)

    def drawHealthBar(self):
        emptyBarSurface = pygame.image.load(g.dataPath + '/gui/bar_empty.png').convert_alpha()
        redBarSurface = pygame.image.load(g.dataPath + '/gui/bar_red.png').convert_alpha()

        pos = (544, 75)
        healthBarWidth = 208*Player[g.myIndex].vitals[Vitals.hp]/Player[g.myIndex].maxHP

        # render text
        hpText = str(Player[g.myIndex].vitals[Vitals.hp]) + '/' + str(Player[g.myIndex].maxHP)
        img = g.tooltipFont.render(hpText, 0, (255, 255, 255))
        imgRect = img.get_rect()
        imgRect.centerx = pos[0] + emptyBarSurface.get_rect().w / 2
        imgRect.centery = pos[1] + emptyBarSurface.get_rect().h / 2

        # blit onto gui
        g.guiSurface.blit(emptyBarSurface, pos)
        g.guiSurface.blit(redBarSurface, pos, (0, 0, healthBarWidth, 28))
        g.guiSurface.blit(img, imgRect)

    def drawManaBar(self):
        emptyBarSurface = pygame.image.load(g.dataPath + '/gui/bar_empty.png').convert_alpha()
        blueBarSurface = pygame.image.load(g.dataPath + '/gui/bar_blue.png').convert_alpha()

        pos = (544, 100)
        manaBarWidth = 208*Player[g.myIndex].vitals[Vitals.mp]/Player[g.myIndex].maxMP

        # render text
        mpText = str(Player[g.myIndex].vitals[Vitals.mp]) + '/' + str(Player[g.myIndex].maxMP)
        img = g.tooltipFont.render(mpText, 0, (255, 255, 255))
        imgRect = img.get_rect()
        imgRect.centerx = pos[0] + emptyBarSurface.get_rect().w / 2
        imgRect.centery = pos[1] + emptyBarSurface.get_rect().h / 2

        # blit onto gui
        g.guiSurface.blit(emptyBarSurface, pos)
        g.guiSurface.blit(blueBarSurface, pos, (0, 0, manaBarWidth, 28))
        g.guiSurface.blit(img, imgRect)

    def drawEquipment(self):
        # load resources
        # todo: only load data files on initialization
        slotHelmet = pygame.image.load(g.dataPath + '/gui/equipment_helmet.png').convert()
        slotHelmetRect = slotHelmet.get_rect()
        slotArmor = pygame.image.load(g.dataPath + '/gui/equipment_armor.png').convert()
        slotArmorRect = slotArmor.get_rect()
        slotWeapon = pygame.image.load(g.dataPath + '/gui/equipment_weapon.png').convert()
        slotWeaponRect = slotWeapon.get_rect()
        slotShield = pygame.image.load(g.dataPath + '/gui/equipment_shield.png').convert()
        slotShieldRect = slotShield.get_rect()

        # positions
        slotHelmetRect.centerx = 648
        slotHelmetRect.centery = 240

        slotArmorRect.centerx = 648
        slotArmorRect.centery = 324

        slotWeaponRect.centerx = 574
        slotWeaponRect.centery = 324

        slotShieldRect.centerx = 722
        slotShieldRect.centery = 324

        # render everything
        g.guiSurface.blit(slotHelmet, slotHelmetRect)
        g.guiSurface.blit(slotArmor, slotArmorRect)
        g.guiSurface.blit(slotWeapon, slotWeaponRect)
        g.guiSurface.blit(slotShield, slotShieldRect)

        for i in range(Equipment.equipment_count):
            if getPlayerEquipmentSlot(g.myIndex, i) != None:
                invNum = getPlayerEquipmentSlot(g.myIndex, i)
                itemNum = getPlayerInvItemNum(g.myIndex, invNum)

                # render the item
                if Item[itemNum].type == ITEM_TYPE_HELMET:
                    itemPic = Item[itemNum].pic

                    tempSurface = self.itemSprites[itemPic]
                    tempSurface = pygame.transform.scale2x(tempSurface)

                    tempRect = tempSurface.get_rect()
                    tempRect.centerx = 648
                    tempRect.centery = 240

                    g.guiSurface.blit(tempSurface, tempRect)

                elif Item[itemNum].type == ITEM_TYPE_ARMOR:
                    itemPic = Item[itemNum].pic

                    tempSurface = self.itemSprites[itemPic]
                    tempSurface = pygame.transform.scale2x(tempSurface)

                    tempRect = tempSurface.get_rect()
                    tempRect.centerx = 648
                    tempRect.centery = 324

                    g.guiSurface.blit(tempSurface, tempRect)

                elif Item[itemNum].type == ITEM_TYPE_WEAPON:
                    itemPic = Item[itemNum].pic

                    tempSurface = self.itemSprites[itemPic]
                    tempSurface = pygame.transform.scale2x(tempSurface)

                    tempRect = tempSurface.get_rect()
                    tempRect.centerx = 574
                    tempRect.centery = 324

                    g.guiSurface.blit(tempSurface, tempRect)

                elif Item[itemNum].type == ITEM_TYPE_SHIELD:
                    itemPic = Item[itemNum].pic

                    tempSurface = self.itemSprites[itemPic]
                    tempSurface = pygame.transform.scale2x(tempSurface)

                    tempRect = tempSurface.get_rect()
                    tempRect.centerx = 722
                    tempRect.centery = 324

                    g.guiSurface.blit(tempSurface, tempRect)

    def drawGold(self):
        # icon
        goldSurface = pygame.image.load(g.dataPath + '/items/2.bmp').convert()
        goldSurface.set_colorkey((0, 0, 0))
        goldSurfaceRect = goldSurface.get_rect()
        goldSurfaceRect.centerx = 665
        goldSurfaceRect.centery = 90

        g.guiSurface.blit(goldSurface, goldSurfaceRect)

        # text
        textSurface = g.nameFont.render("203", 0, textColor.YELLOW)
        textSurfaceRect = textSurface.get_rect()
        textSurfaceRect.centerx = 630
        textSurfaceRect.centery = 90

        g.guiSurface.blit(textSurface, textSurfaceRect)

    def drawInventorySlots(self):
        ''' render the empty inventory slots before the items '''
        for y in range(0, 3):
            for x in range(0, 3):
                tempPos = (524 + x*(66+24), 90 + y*(66+24))
                g.guiSurface.blit(self.emptySlotSurface, tempPos)

    def drawInventory(self):
        ''' render the items within the emtpy inventory slots '''
        curItemSlot = 0

        # get all equipped items
        equippedItems = getPlayerEquipmentSlot(g.myIndex, Equipment.weapon), getPlayerEquipmentSlot(g.myIndex, Equipment.armor), getPlayerEquipmentSlot(g.myIndex, Equipment.helmet), getPlayerEquipmentSlot(g.myIndex, Equipment.shield)

        for y in range(0, 3):
            for x in range(0, 3):
                if getPlayerInvItemNum(g.myIndex, curItemSlot) != None:
                    itemNum = getPlayerInvItemNum(g.myIndex, curItemSlot)
                    itemPic = Item[itemNum].pic

                    tempSurface = self.itemSprites[itemPic]
                    tempSurface = pygame.transform.scale2x(tempSurface)

                    tempPos = (524 + x*(66+24) + 1, 90 + y*(66+24) + 1)

                    # if item is equipped, then mark it
                    if curItemSlot in equippedItems:
                        pygame.draw.rect(tempSurface, (255, 0, 0), (0, 0, 64, 64), 1)

                    g.guiSurface.blit(tempSurface, tempPos)

                curItemSlot += 1

    def drawInventoryTooltip(self, itemSlot):
        ''' draw a tooltip when the mouse is hovering over an item in the inventory '''

        def generateTooltip(itemNum, itemSlot):
            # determine rect size
            itemName = Item[itemNum].name
            textSize = g.tooltipFont.size(itemName)

            # determine name color
            itemType = Item[itemNum].type

            if itemType == ITEM_TYPE_WEAPON or itemType == ITEM_TYPE_ARMOR or itemType == ITEM_TYPE_HELMET or itemType == ITEM_TYPE_SHIELD:
                nameColor = (33, 96, 167)  # textColor.BLUE

                # calculate stats string length
                strString = '+' + str(Item[itemNum].data2) + _(' strength')
                strDurability = str(getPlayerInvItemDur(g.myIndex, itemSlot)) + '/' + str(Item[itemNum].data1) + _(' durability')

                statStrSize = g.tooltipFont.size(strString)
                statDurSize = g.tooltipFont.size(strDurability)

                # calculate the largest width/height
                if statStrSize[0] > statDurSize[0]:
                    statTextSize = statStrSize
                else:
                    statTextSize = statDurSize

                if textSize[0] > statTextSize[0]:
                    tempSurface = pygame.Surface((textSize[0] + 10, textSize[1] + statStrSize[1] + statDurSize[1] + 10))
                else:
                    tempSurface = pygame.Surface((statTextSize[0] + 10, textSize[1] + statStrSize[1] + statDurSize[1] + 10))

                tempSurface.fill((0, 0, 0))

                # draw border
                pygame.draw.rect(tempSurface, (100, 100, 100), (0, 0, tempSurface.get_rect().w, tempSurface.get_rect().h), 1)

                # render information
                # - name
                img = g.tooltipFont.render(itemName, 0, nameColor)
                imgRect = img.get_rect()
                imgRect.x = 5
                imgRect.centery = tempSurface.get_rect().h / 4

                tempSurface.blit(img, imgRect)

                # - strength
                img = g.tooltipFont.render(strString, 0, (255, 255, 255))
                imgRect = img.get_rect()
                imgRect.x = 5
                imgRect.centery = (tempSurface.get_rect().h / 4) * 2

                tempSurface.blit(img, imgRect)

                # - durability
                img = g.tooltipFont.render(strDurability, 0, (255, 255, 255))
                imgRect = img.get_rect()
                imgRect.x = 5
                imgRect.centery = (tempSurface.get_rect().h / 4) * 3

                tempSurface.blit(img, imgRect)

            elif itemType == ITEM_TYPE_CURRENCY:
                nameColor = textColor.YELLOW

                strValue = _('Amount: ') + str(getPlayerInvItemValue(g.myIndex, itemSlot))
                strValueSize = g.tooltipFont.size(strValue)

                # draw surface
                if textSize[0] > strValueSize[0]:
                    tempSurface = pygame.Surface((textSize[0] + 10, textSize[1] + strValueSize[1] + 10))
                else:
                    tempSurface = pygame.Surface((strValueSize[0] + 10, textSize[1] + strValueSize[1] + 10))

                tempSurface.fill((0, 0, 0))

                # draw border
                pygame.draw.rect(tempSurface, (100, 100, 100), (0, 0, tempSurface.get_rect().w, tempSurface.get_rect().h), 1)

                # render information
                # - name
                img = g.tooltipFont.render(itemName, 0, nameColor)
                imgRect = img.get_rect()
                imgRect.x = 5
                imgRect.centery = tempSurface.get_rect().h / 3

                tempSurface.blit(img, imgRect)

                # - value
                img = g.tooltipFont.render(strValue, 0, (255, 255, 255))
                imgRect = img.get_rect()
                imgRect.x = 5
                imgRect.centery = (tempSurface.get_rect().h / 3) * 2

                tempSurface.blit(img, imgRect)

            else:
                nameColor = textColor.GREY

                # draw surface
                tempSurface = pygame.Surface((textSize[0] + 10, textSize[1] + 10))
                tempSurface.fill((0, 0, 0))

                # draw border
                pygame.draw.rect(tempSurface, (100, 100, 100), (0, 0, tempSurface.get_rect().w, tempSurface.get_rect().h), 1)


                # render information
                # - name
                img = g.tooltipFont.render(itemName, 0, nameColor)
                imgRect = img.get_rect()
                imgRect.centerx = tempSurface.get_rect().w / 2
                imgRect.centery = tempSurface.get_rect().h / 2

                tempSurface.blit(img, imgRect)

            return tempSurface

        if getPlayerInvItemNum(g.myIndex, itemSlot) != None:
            # generate tooltip
            itemNum = getPlayerInvItemNum(g.myIndex, itemSlot)
            tooltipSurface = generateTooltip(itemNum, itemSlot)

            # position the tooltip at the mouse
            self.tooltipRect.x = g.cursorX
            self.tooltipRect.y = g.cursorY - tooltipSurface.get_rect().h

            # render tooltip on surface
            g.guiSurface.blit(tooltipSurface, self.tooltipRect)

    def drawSpellbookSlots(self):
        ''' render the empty inventory slots before the items '''
        for y in range(0, 3):
            for x in range(0, 3):
                tempPos = (524 + x*(66+24), 90 + y*(66+24))
                g.guiSurface.blit(self.emptySlotSurface, tempPos)

    def drawSpellbook(self):
        ''' render the items within the empty spellbook slots '''
        curSpellSlot = 0

        for y in range(0, 3):
            for x in range(0, 3):

                if PlayerSpells[curSpellSlot] is not None:
                    spellNum = PlayerSpells[curSpellSlot]
                    spellPic = Spell[spellNum].pic

                    tempSurface = self.spellSprites[spellPic]
                    tempSurface = pygame.transform.scale2x(tempSurface)

                    tempPos = (524 + x*(66+24) + 1, 90 + y*(66+24) + 1)

                    g.guiSurface.blit(tempSurface, tempPos, (0, 0, 64, 64))

                # check if theres a hotkey attached to the slot
                if curSpellSlot in g.SPELLBOOK_HOTKEYS.values():
                    # find the key
                    for key, spellSlot in g.SPELLBOOK_HOTKEYS.items():
                        if spellSlot == curSpellSlot:
                            img = g.tooltipFont.render(g.SPELLBOOK_HOTKEYS_STRINGS[key], 0, (255, 255, 255))
                            imgPos = (524 + x*(66+24) + 1, 90 + y*(66+24) + 1)

                            g.guiSurface.blit(img, (imgPos[0] + 5, imgPos[1] + 5))



                curSpellSlot += 1

                # todo: make grey if out of mana

    def drawSpellbookTooltip(self, spellSlot):
        ''' draw a tooltip when the mouse is hovering over a spell in the spellbook '''

        def generateTooltip(spellNum, spellSlot):
            # determine rect size
            spellName = Spell[spellNum].name
            textSize = g.tooltipFont.size(spellName)

            # determine name color
            spellType = Spell[spellNum].type

            if spellType != SPELL_TYPE_GIVEITEM:
                nameColor = textColor.WHITE

                # create strings
                strReqMp = str(Spell[spellNum].reqMp) + _(' Mana')
                if spellType == SPELL_TYPE_ADDHP:
                    strEffect = 'Effect: +' + str(Spell[spellNum].data1) + ' HP'
                elif spellType == SPELL_TYPE_ADDMP:
                    strEffect = 'Effect: +' + str(Spell[spellNum].data1) + ' MP'
                elif spellType == SPELL_TYPE_ADDSP:
                    strEffect = 'Effect: +' + str(Spell[spellNum].data1) + ' SP'
                elif spellType == SPELL_TYPE_SUBHP:
                    strEffect = 'Effect: -' + str(Spell[spellNum].data1) + ' HP'
                elif spellType == SPELL_TYPE_SUBMP:
                    strEffect = 'Effect: -' + str(Spell[spellNum].data1) + ' MP'
                elif spellType == SPELL_TYPE_SUBSP:
                    strEffect = 'Effect: -' + str(Spell[spellNum].data1) + ' SP'

                strReqMpSize = g.tooltipFont.size(strReqMp)
                strEffectSize = g.tooltipFont.size(strEffect)

                # get largest width/height
                if strReqMpSize[0] > strEffectSize[0]:
                    infoTextSize = strReqMpSize
                else:
                    infoTextSize = strEffectSize

                if textSize[0] > infoTextSize[0]:
                    tempSurface = pygame.Surface((textSize[0] + 10, textSize[1] + strReqMpSize[1] + strEffectSize[1] + 10))
                else:
                    tempSurface = pygame.Surface((infoTextSize[0] + 10, textSize[1] + strReqMpSize[1] + strEffectSize[1] + 10))

                tempSurface.fill((0, 0, 0))

                # border
                pygame.draw.rect(tempSurface, (100, 100, 100), (0, 0, tempSurface.get_rect().w, tempSurface.get_rect().h), 1)

                # render information
                # - name
                img = g.tooltipFont.render(spellName, 0, nameColor)
                imgRect = img.get_rect()
                imgRect.x = 5
                imgRect.centery = tempSurface.get_rect().h / 4

                tempSurface.blit(img, imgRect)

                # - mana required
                img = g.tooltipFont.render(strReqMp, 0, textColor.BRIGHT_BLUE)
                imgRect = img.get_rect()
                imgRect.x = 5
                imgRect.centery = (tempSurface.get_rect().h / 4) * 2

                tempSurface.blit(img, imgRect)

                # - effect
                img = g.tooltipFont.render(strEffect, 0, textColor.YELLOW)
                imgRect = img.get_rect()
                imgRect.x = 5
                imgRect.centery = (tempSurface.get_rect().h / 4) * 3

                tempSurface.blit(img, imgRect)

            return tempSurface


        if PlayerSpells[spellSlot] != None:
            # generate tooltip
            spellNum = PlayerSpells[spellSlot]
            tooltipSurface = generateTooltip(spellNum, spellSlot)

            # position the tooltip at the mouse
            self.tooltipRect.x = g.cursorX
            self.tooltipRect.y = g.cursorY - tooltipSurface.get_rect().h

            # render tooltip on surface
            g.guiSurface.blit(tooltipSurface, self.tooltipRect)
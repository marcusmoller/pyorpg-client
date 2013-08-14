import pygame
from pygame.locals import *

import global_vars as g

pygame.font.init()

FONT = g.systemFont
SYSFONT = g.systemFont

#colors
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
YELLOW = (  0, 255, 255)

# CONSTANTS
ALIGN_RIGHT = 0
ALIGN_LEFT = 1
ALIGN_CENTER = 2

MSGBOX_OK = 0
MSGBOX_CANCEL = 1

class pygClassClickable(object):
    def __init__(self):

        self._visible = True

        # state of button
        self.buttonDown = False
        self.mouseOverButton = False
        self.lastMouseDownOverButton = False


    def mouseClick(self, event):
        pass
    def mouseEnter(self, event):
        pass
    def mouseMove(self, event):
        pass
    def mouseExit(self, event):
        pass
    def mouseDown(self, event):
        pass
    def mouseUp(self, event):
        pass

    def handleEvents(self, event):
        if event.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
            return []

        returnValue = []
        hasExited = False

        if not self.mouseOverButton and self._rect.collidepoint(event.pos):
            # mouse enter
            self.mouseOverButton = True
            self.mouseEnter(event)
            returnValue.append('enter')

        elif self.mouseOverButton and not self._rect.collidepoint(event.pos):
            # mouse exit
            self.mouseOverButton = False
            hasExited = True

        if self._rect.collidepoint(event.pos):
            if event.type == MOUSEMOTION:
                self.mouseMove(event)
                returnValue.append('move')
            elif event.type == MOUSEBUTTONDOWN:
                self.buttonDown = True
                self.lastMouseDownOverButton = True
                self.mouseDown(event)
                returnValue.append('down')
        else:
            if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                self.lastMouseDownOverButton = False

        doMouseClick = False

        if event.type == MOUSEBUTTONUP:
            if self.lastMouseDownOverButton:
                doMouseClick = True

            self.lastMouseDownOverButton = False

            if self.buttonDown:
                self.buttonDown = False
                self.mouseUp(event)
                returnValue.append('up')

            if doMouseClick:
                self.buttonDown = False
                self.mouseClick(event)
                returnValue.append('click')

        if hasExited:
            self.mouseExit(event)
            returnValue.append('exit')

        return returnValue

############
# pygLabel #
############
class pygLabel():
    ''' a text label '''

    def __init__(self, rect, text, color=(255, 255, 255), font=SYSFONT, fontsize=24, align=ALIGN_RIGHT):
        self.rect = pygame.Rect(rect)
        self.x = self.rect.x
        self.y = self.rect.y

        self.text = text
        self.color = color
        self.font = font
        self.fontSize = fontsize
        self.align = align

        # initialize label
        self.labelSurface = self.font.render(self.text, 1, self.color)
        self.labelRect = self.labelSurface.get_rect()

        if self.align == ALIGN_RIGHT:
            self.labelRect.x = self.rect.x
            self.labelRect.y = self.rect.y
        elif self.align == ALIGN_CENTER:
            self.labelRect.center = self.rect.x+(self.rect.width/2), self.rect.y-10


    def draw(self, surface):
        surface.blit(self.labelSurface, self.labelRect)

    def update(self):
        self.labelSurface = self.font.render(self.text, 1, self.color)
        self.labelRect = self.labelSurface.get_rect()

        if self.align == ALIGN_RIGHT:
            self.labelRect.x = self.rect.x
            self.labelRect.y = self.rect.y
        elif self.align == ALIGN_CENTER:
            self.labelRect.center = self.rect.x+(self.rect.width/2), self.rect.y-10

    def setText(self, text):
        self.text = text
        self.update()


#############
# pygBUTTON #
#############
class pygButton(object):
    def __init__(self, rect=None, caption='', bgcolor=WHITE, fgcolor=BLACK, font=None, normal=None, down=None, highlight=None):
        if rect is None:
            self._rect = pygame.rect(0, 0, 30, 60)

        else:
            self._rect = pygame.Rect(rect)

        self._caption = caption
        self._bgcolor = bgcolor
        self._fgcolor = fgcolor

        if font is None:
            self._font = SYSFONT
        else:
            self._font = font

        self._visible = True

        # state of button
        self.buttonDown = False
        self.mouseOverButton = False
        self.lastMouseDownOverButton = False
        self.customSurfaces = False

        if normal is None:
            # not a custom button
            self.surfaceNormal = pygame.Surface(self._rect.size)
            self.surfaceDown = pygame.Surface(self._rect.size)
            self.surfaceHighlight = pygame.Surface(self._rect.size)
            self._update()

        else:
            self.setSurfaces(normal, down, highlight)
            self._update()

    def setColor(self, color):
        self._bgcolor = color
        self._update()

    def setCaption(self, caption):
        self._caption = caption
        self._update()

    def setSurfaces(self, normalSurface, downSurface=None, highlightSurface=None):
        ''' Custom image rather than text button '''
        if downSurface is None:
            downSurface = normalSurface

        if highlightSurface is None:
            highlightSurface = normalSurface

        if type(normalSurface) == str:
            self.origSurfaceNormal = pygame.image.load(normalSurface).convert_alpha()

        if type(downSurface) == str:
            self.origSurfaceDown = pygame.image.load(downSurface).convert_alpha()

        if type(highlightSurface) == str:
            self.origSurfaceHighlight = pygame.image.load(highlightSurface).convert_alpha()

        if self.origSurfaceNormal.get_size() != self.origSurfaceDown.get_size() != self.origSurfaceHighlight.get_size():
            raise Exception("Custom surfaces must be same size")

        self.surfaceNormal = self.origSurfaceNormal
        self.surfaceDown = self.origSurfaceDown
        self.surfaceHighlight = self.origSurfaceHighlight

        self.customSurfaces = True

        self._rect = pygame.Rect((self._rect.left, self._rect.top, self.surfaceNormal.get_width(), self.surfaceNormal.get_height()))

    def draw(self, surfaceObj):
        if self._visible:
            if self.buttonDown:
                surfaceObj.blit(self.surfaceDown, self._rect)
            elif self.mouseOverButton:
                surfaceObj.blit(self.surfaceHighlight, self._rect)
            else:
                surfaceObj.blit(self.surfaceNormal, self._rect)

    def _update(self):
        ''' redraws the surface object '''
        if self.customSurfaces:
            self.surfaceNormal = pygame.transform.smoothscale(self.origSurfaceNormal, self._rect.size)
            self.surfaceDown = pygame.transform.smoothscale(self.origSurfaceDown, self._rect.size)
            self.surfaceHighlight = pygame.transform.smoothscale(self.origSurfaceHighlight, self._rect.size)

            # draw caption...
            w = self._rect.width
            h = self._rect.height

            captionSurf = self._font.render(self._caption, True, self._fgcolor)
            captionRect = captionSurf.get_rect()
            captionRect.center = int(w/2), int(h/2)
            self.surfaceNormal.blit(captionSurf, captionRect)
            self.surfaceDown.blit(captionSurf, captionRect)
            self.surfaceHighlight.blit(captionSurf, captionRect)

            return

        w = self._rect.width
        h = self._rect.height

        # fill bg color
        self.surfaceNormal.fill(self._bgcolor)
        self.surfaceDown.fill(self._bgcolor)
        self.surfaceHighlight.fill(self._bgcolor)

        # draw caption
        captionSurf = self._font.render(self._caption, True, self._fgcolor, self._bgcolor)
        captionRect = captionSurf.get_rect()
        captionRect.center = int(w/2), int(h/2)
        self.surfaceNormal.blit(captionSurf, captionRect)
        self.surfaceDown.blit(captionSurf, captionRect)

        # draw border for normal button
        pygame.draw.rect(self.surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1)

        # draw border for down button
        pygame.draw.rect(self.surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1)

        # draw border for highlight button
        self.surfaceHighlight = self.surfaceNormal

    ##########
    # EVENTS #
    ##########

    def mouseClick(self, event):
        pass
    def mouseEnter(self, event):
        pass
    def mouseMove(self, event):
        pass
    def mouseExit(self, event):
        pass
    def mouseDown(self, event):
        pass
    def mouseUp(self, event):
        pass

    def handleEvents(self, event):
        if event.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self._visible:
            return []

        returnValue = []
        hasExited = False

        if not self.mouseOverButton and self._rect.collidepoint(event.pos):
            # mouse enter
            self.mouseOverButton = True
            self.mouseEnter(event)
            returnValue.append('enter')

        elif self.mouseOverButton and not self._rect.collidepoint(event.pos):
            # mouse exit
            self.mouseOverButton = False
            hasExited = True

        if self._rect.collidepoint(event.pos):
            if event.type == MOUSEMOTION:
                self.mouseMove(event)
                returnValue.append('move')
            elif event.type == MOUSEBUTTONDOWN:
                self.buttonDown = True
                self.lastMouseDownOverButton = True
                self.mouseDown(event)
                returnValue.append('down')
        else:
            if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                self.lastMouseDownOverButton = False

        doMouseClick = False

        if event.type == MOUSEBUTTONUP:
            if self.lastMouseDownOverButton:
                doMouseClick = True

            self.lastMouseDownOverButton = False

            if self.buttonDown:
                self.buttonDown = False
                self.mouseUp(event)
                returnValue.append('up')

            if doMouseClick:
                self.buttonDown = False
                self.mouseClick(event)
                returnValue.append('click')

        if hasExited:
            self.mouseExit(event)
            returnValue.append('exit')

        return returnValue
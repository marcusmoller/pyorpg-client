import pygame
from pygame.locals import *

import global_vars as g

pygame.font.init()

FONT = pygame.font.SysFont(None, 24)
SYSFONT = pygame.font.SysFont(None, 24)

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

###############
# pygCheckbox #
###############
class pygCheckBox(pygClassClickable):
    ''' a checkbox '''
    def __init__(self, rect, text, checked=False, color=(255, 255, 255), font=SYSFONT, fontsize=24, align=ALIGN_RIGHT):
        super(pygCheckBox, self).__init__()

        self.rect = pygame.Rect(rect)
        self._rect = self.rect
        self.x = self.rect.x
        self.y = self.rect.y

        self.text = text
        self.color = color
        self.font = font
        self.fontSize = fontsize
        self.align = align

        self.checked = checked

        # initialize box
        self.boxRect = pygame.Rect(self.rect.x, self.rect.y, 20, 20)
        self.markedRect = pygame.Rect(self.rect.x, self.rect.y, 10, 10)
        self.markedRect.centerx = self.boxRect.x + (self.boxRect.width / 2)
        self.markedRect.centery = self.boxRect.y + (self.boxRect.height / 2)

        # initialize label
        self.labelSurface = self.font.render(self.text, 1, self.color)
        self.labelRect = self.labelSurface.get_rect()

        if self.align == ALIGN_RIGHT:
            self.labelRect.x = self.rect.x
            self.labelRect.y = self.rect.y
        elif self.align == ALIGN_CENTER:
            self.labelRect.center = self.rect.x+(self.rect.width/2), self.rect.y-10


    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.boxRect, 0)

        if self.checked:
            pygame.draw.rect(surface, BLACK, self.markedRect, 0)

        surface.blit(self.labelSurface, (self.labelRect.x+30, self.labelRect.y, self.labelRect.width, self.labelRect.height))

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

    def mouseClick(self, event):
        self.checked = True

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
# pygMsgBox #
#############

class pygMsgBox():
    ''' a popup box containing text '''

    def __init__(self, rect, msg, type):
        self.rect = pygame.Rect(rect)
        self.x = self.rect.x
        self.y = self.rect.y

        self.msg = msg
        self.type = type

        self.font = pygame.font.SysFont(None, 18)

        if self.type == MSGBOX_OK:
            self.button = pygButton((275, 375, 60, 30), 'OK', fgcolor=(255, 255, 255), normal='data/gui/menu_enabled.png', down='data/gui/menu_mousedown.png', highlight='data/gui/menu_mouseover.png')
        elif self.type == MSGBOX_CANCEL:
            self.button = pygButton((275, 375, 60, 30), 'CANCEL', fgcolor=(255, 255, 255), normal='data/gui/menu_enabled.png', down='data/gui/menu_mousedown.png', highlight='data/gui/menu_mouseover.png')

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect, 0)
        pygame.draw.rect(surface, WHITE, self.rect, 1)

        textSurface = self.font.render(self.msg, 1, (255, 255, 255))
        surface.blit(textSurface, (self.rect.left + 5, y, self.rect.width, self.rect.top))

        if self.type == MSGBOX_OK:
            print "test"

###########
# pygList #
###########

class pygList():
    ''' list of text '''
    #todo: dont use an array of colors...

    def __init__(self, rect, color):
        self.rect = pygame.Rect(rect)
        self.x = self.rect.x
        self.y = self.rect.y

        self.font = pygame.font.SysFont(None, 18)
        self.color = color

        self.items = []
        self.textColors = []

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect, 0)
        pygame.draw.rect(surface, WHITE, self.rect, 1)

        for i in range(len(self.items[-10:])):
            y = self.rect.top + 16*i

            if y > (self.rect.top + self.rect.height - 16):
                return

            textSurface = self.font.render(self.items[-10:][i], 1, self.textColors[-10:][i])
            surface.blit(textSurface, (self.rect.left + 5, y, self.rect.width, self.rect.top))


    def _setPos(self, x, y):
        self.x = x
        self.y = y

    def add(self, text, color):
        textSurface = self.font.render(text, 1, color)
        if textSurface.get_rect().width > self.rect.width:
            print "Oh oh"

        self.items.append(text)
        self.textColors.append(color)


#################
# pygInputField #
#################

class pygInputField(pygClassClickable):
    ''' text input field '''
    ''' credits: eztext.py '''

    def __init__(self, rect, prompt, maxlength, color, focus=False):
        super(pygInputField, self).__init__()
        self.rect = pygame.Rect(rect)
        self._rect = self.rect # todo, remove
        self.x = self.rect.x
        self.y = self.rect.y

        self.font = pygame.font.Font(None, 24)
        self.maxLength = maxlength
        self.color = color

        self.focus = focus
        self.mouseOverButton = False

        self.restricted = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.prompt = prompt
        self.value = ''

        self.shifted = False

    def _setPos(self, x, y):
        self.x = x
        self.y = y

    def _setFont(self, font):
        self.font = pygame.font.Font(font, 24)

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect, 0)

        if self.focus:
            pygame.draw.rect(surface, YELLOW, self.rect, 1)
        else:
            pygame.draw.rect(surface, WHITE, self.rect, 1)

        textSurface = self.font.render(self.value, 1, self.color)

        labelSurface = self.font.render(self.prompt, 1, self.color)
        labelRect = labelSurface.get_rect()
        labelRect.center = self.rect.x+(self.rect.width/2), self.rect.y-10

        surface.blit(labelSurface, labelRect)
        surface.blit(textSurface, (self.rect.x+5, self.rect.y+1, self.rect.width, self.rect.height))

    def mouseClick(self, event):
        if self.focus:
            self.focus = False
        else:
            self.focus = True

    def checkFocus(self, event):
        if event.type != MOUSEBUTTONDOWN:
            return

        hasExited = False

        if not self.mouseOverButton and self.rect.collidepoint(event.pos):
            # mouse enters
            self.mouseOverButton = True
            return

        if self.mouseOverButton and not self.rect.collidepoint(event.pos):
            # mouse moved away
            self.mouseOverButton = False
            hasExited = True

        if self.rect.collidepoint(event.pos):
            if event.type == MOUSEBUTTONDOWN:
                if self.focus:
                    self.focus = False
                else:
                    self.focus = True

    def update(self, event):
        # check if mousedown
        if event.type == KEYUP:
            if event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = False
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE: self.value = self.value[:-1]
            elif event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = True
            elif event.key == K_SPACE: self.value += ' '
            if not self.shifted:
                if event.key == K_a and 'a' in self.restricted: self.value += 'a'
                elif event.key == K_b and 'b' in self.restricted: self.value += 'b'
                elif event.key == K_c and 'c' in self.restricted: self.value += 'c'
                elif event.key == K_d and 'd' in self.restricted: self.value += 'd'
                elif event.key == K_e and 'e' in self.restricted: self.value += 'e'
                elif event.key == K_f and 'f' in self.restricted: self.value += 'f'
                elif event.key == K_g and 'g' in self.restricted: self.value += 'g'
                elif event.key == K_h and 'h' in self.restricted: self.value += 'h'
                elif event.key == K_i and 'i' in self.restricted: self.value += 'i'
                elif event.key == K_j and 'j' in self.restricted: self.value += 'j'
                elif event.key == K_k and 'k' in self.restricted: self.value += 'k'
                elif event.key == K_l and 'l' in self.restricted: self.value += 'l'
                elif event.key == K_m and 'm' in self.restricted: self.value += 'm'
                elif event.key == K_n and 'n' in self.restricted: self.value += 'n'
                elif event.key == K_o and 'o' in self.restricted: self.value += 'o'
                elif event.key == K_p and 'p' in self.restricted: self.value += 'p'
                elif event.key == K_q and 'q' in self.restricted: self.value += 'q'
                elif event.key == K_r and 'r' in self.restricted: self.value += 'r'
                elif event.key == K_s and 's' in self.restricted: self.value += 's'
                elif event.key == K_t and 't' in self.restricted: self.value += 't'
                elif event.key == K_u and 'u' in self.restricted: self.value += 'u'
                elif event.key == K_v and 'v' in self.restricted: self.value += 'v'
                elif event.key == K_w and 'w' in self.restricted: self.value += 'w'
                elif event.key == K_x and 'x' in self.restricted: self.value += 'x'
                elif event.key == K_y and 'y' in self.restricted: self.value += 'y'
                elif event.key == K_z and 'z' in self.restricted: self.value += 'z'
                elif event.key == K_0 and '0' in self.restricted: self.value += '0'
                elif event.key == K_1 and '1' in self.restricted: self.value += '1'
                elif event.key == K_2 and '2' in self.restricted: self.value += '2'
                elif event.key == K_3 and '3' in self.restricted: self.value += '3'
                elif event.key == K_4 and '4' in self.restricted: self.value += '4'
                elif event.key == K_5 and '5' in self.restricted: self.value += '5'
                elif event.key == K_6 and '6' in self.restricted: self.value += '6'
                elif event.key == K_7 and '7' in self.restricted: self.value += '7'
                elif event.key == K_8 and '8' in self.restricted: self.value += '8'
                elif event.key == K_9 and '9' in self.restricted: self.value += '9'
                elif event.key == K_BACKQUOTE and '`' in self.restricted: self.value += '`'
                elif event.key == K_MINUS and '-' in self.restricted: self.value += '-'
                elif event.key == K_EQUALS and '=' in self.restricted: self.value += '='
                elif event.key == K_LEFTBRACKET and '[' in self.restricted: self.value += '['
                elif event.key == K_RIGHTBRACKET and ']' in self.restricted: self.value += ']'
                elif event.key == K_BACKSLASH and '\\' in self.restricted: self.value += '\\'
                elif event.key == K_SEMICOLON and ';' in self.restricted: self.value += ';'
                elif event.key == K_QUOTE and '\'' in self.restricted: self.value += '\''
                elif event.key == K_COMMA and ',' in self.restricted: self.value += ','
                elif event.key == K_PERIOD and '.' in self.restricted: self.value += '.'
                elif event.key == K_SLASH and '/' in self.restricted: self.value += '/'
            elif self.shifted:
                if event.key == K_a and 'A' in self.restricted: self.value += 'A'
                elif event.key == K_b and 'B' in self.restricted: self.value += 'B'
                elif event.key == K_c and 'C' in self.restricted: self.value += 'C'
                elif event.key == K_d and 'D' in self.restricted: self.value += 'D'
                elif event.key == K_e and 'E' in self.restricted: self.value += 'E'
                elif event.key == K_f and 'F' in self.restricted: self.value += 'F'
                elif event.key == K_g and 'G' in self.restricted: self.value += 'G'
                elif event.key == K_h and 'H' in self.restricted: self.value += 'H'
                elif event.key == K_i and 'I' in self.restricted: self.value += 'I'
                elif event.key == K_j and 'J' in self.restricted: self.value += 'J'
                elif event.key == K_k and 'K' in self.restricted: self.value += 'K'
                elif event.key == K_l and 'L' in self.restricted: self.value += 'L'
                elif event.key == K_m and 'M' in self.restricted: self.value += 'M'
                elif event.key == K_n and 'N' in self.restricted: self.value += 'N'
                elif event.key == K_o and 'O' in self.restricted: self.value += 'O'
                elif event.key == K_p and 'P' in self.restricted: self.value += 'P'
                elif event.key == K_q and 'Q' in self.restricted: self.value += 'Q'
                elif event.key == K_r and 'R' in self.restricted: self.value += 'R'
                elif event.key == K_s and 'S' in self.restricted: self.value += 'S'
                elif event.key == K_t and 'T' in self.restricted: self.value += 'T'
                elif event.key == K_u and 'U' in self.restricted: self.value += 'U'
                elif event.key == K_v and 'V' in self.restricted: self.value += 'V'
                elif event.key == K_w and 'W' in self.restricted: self.value += 'W'
                elif event.key == K_x and 'X' in self.restricted: self.value += 'X'
                elif event.key == K_y and 'Y' in self.restricted: self.value += 'Y'
                elif event.key == K_z and 'Z' in self.restricted: self.value += 'Z'
                elif event.key == K_0 and ')' in self.restricted: self.value += ')'
                elif event.key == K_1 and '!' in self.restricted: self.value += '!'
                elif event.key == K_2 and '@' in self.restricted: self.value += '@'
                elif event.key == K_3 and '#' in self.restricted: self.value += '#'
                elif event.key == K_4 and '$' in self.restricted: self.value += '$'
                elif event.key == K_5 and '%' in self.restricted: self.value += '%'
                elif event.key == K_6 and '^' in self.restricted: self.value += '^'
                elif event.key == K_7 and '/' in self.restricted: self.value += '/'
                elif event.key == K_8 and '*' in self.restricted: self.value += '*'
                elif event.key == K_9 and '(' in self.restricted: self.value += '('
                elif event.key == K_BACKQUOTE and '~' in self.restricted: self.value += '~'
                elif event.key == K_MINUS and '_' in self.restricted: self.value += '_'
                elif event.key == K_EQUALS and '+' in self.restricted: self.value += '+'
                elif event.key == K_LEFTBRACKET and '{' in self.restricted: self.value += '{'
                elif event.key == K_RIGHTBRACKET and '}' in self.restricted: self.value += '}'
                elif event.key == K_BACKSLASH and '|' in self.restricted: self.value += '|'
                elif event.key == K_SEMICOLON and ':' in self.restricted: self.value += ':'
                elif event.key == K_QUOTE and '"' in self.restricted: self.value += '"'
                elif event.key == K_COMMA and '<' in self.restricted: self.value += '<'
                elif event.key == K_PERIOD and '>' in self.restricted: self.value += '>'
                elif event.key == K_SLASH and '?' in self.restricted: self.value += '?'

        if len(self.value) > self.maxLength and self.maxLength >= 0: self.value = self.value[:-1]

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
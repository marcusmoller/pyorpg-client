import pygame, sys
from pygame.locals import *
from pgu import gui
from twisted.internet import reactor

import global_vars as g
from constants import *

from gui.dialogs import alertLengthDialog

class registerControl(gui.Table):
	def __init__(self, **params):
		gui.Table.__init__(self, **params)
		self.value = gui.Form()
		self.engine = None

		def btnRegister(btn):
			def isLoginLegal(username, password):
				if len(username) > 3 and len(password) > 3:
					return True
				else:
					print "username and password must be larger 3 characters"

			def isStringLegal(string):
				restricted = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

				for i in range(len(string)):
					if string[i] not in restricted:
						# todo: msgbox (not valid)
						print "name is not valid"
						return False

				return True

			def checkPasswords(password1, password2):
				if password1 == password2:
					return True


			username = self.value.items()[0][1]
			password = self.value.items()[1][1]
			passwordConfirm = self.value.items()[2][1]

			if isLoginLegal(username, password):
				if checkPasswords(password, passwordConfirm):
					if isStringLegal(username):
						g.tcpConn.sendNewAccount(username, password)
						print "Created user " + username

						# return to login screen
						g.gameState = MENU_LOGIN
				else:
					# todo: msgbox
					print "passwords didn't match"

		def btnCancel(btn):
			g.gameState = MENU_LOGIN

		self.tr()
		self.td(gui.Label('Username:', color=(255, 255, 255)))
		self.tr()
		self.td(gui.Input(name="username", value="Username"))

		self.tr()
		self.td(gui.Spacer(0, 20))

		self.tr()
		self.td(gui.Label('Password:', color=(255, 255, 255)))
		self.tr()
		self.td(gui.Password(name="password", value="password"))

		self.tr()
		self.td(gui.Spacer(0, 10))

		self.tr()
		self.td(gui.Label('Confirm password:', color=(255, 255, 255)))
		self.tr()
		self.td(gui.Password(name="passwordConfirm", value="password"))

		self.tr()
		self.td(gui.Spacer(0, 30))


		self.tr()
		btn = gui.Button("Create", width=120)
		btn.connect(gui.CLICK, btnRegister, None)
		self.td(btn)

		self.tr()
		self.td(gui.Spacer(0, 5))

		self.tr()
		btn = gui.Button("Cancel", width=120)
		btn.connect(gui.CLICK, btnCancel, None)
		self.td(btn)

class menuRegister():
	def __init__(self, surface):
		self.surface = surface
		self.backgroundImage = pygame.image.load(g.dataPath + '/gui/menu_background.png')

		# GUI
		self.app = gui.App()

		regControl = registerControl()
		regControl.engine = self

		self.c = gui.Container(align=0, valign=0)
		self.c.add(regControl, 0, 0)

		self.app.init(self.c)

	def draw(self):
		# background
		self.surface.blit(self.backgroundImage, (0, 0))
		self.app.paint()

		pygame.display.update()

	def _handleEvents(self, event):
		# keyboard shortcuts
		self.app.event(event)
		
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			g.gameState = MENU_LOGIN
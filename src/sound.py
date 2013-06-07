import random
import pygame
import pygame.mixer
from pygame.locals import *

import global_vars as g


class SoundEngine():
	def __init__(self):
		if not pygame.mixer: print "Warning, sounds are disabled!"
		pygame.mixer.init()

		self.playingSound = False
		self.muted = False

		self.soundList = []
		self.musicList = []

		self.attackSounds = []

	def loadSounds(self):
		self.soundList.append(self.loadFile(g.dataPath + "/music/0.ogg"))
		self.soundList.append(self.loadFile(g.dataPath + "/music/1.ogg"))

		self.attackSounds.append(self.loadFile(g.dataPath + "/sounds/swing_1.ogg"))
		self.attackSounds.append(self.loadFile(g.dataPath + "/sounds/swing_2.ogg"))
		self.attackSounds.append(self.loadFile(g.dataPath + "/sounds/swing_3.ogg"))

	def loadFile(self, filename):
		sound = pygame.mixer.Sound(filename)
		return sound

	def play(self, sound, loops=False, fade_in=False):
		if fade_in == True:
			fade_ms = 1000
		else:
			fade_ms = 0

		if not self.muted:
			pygame.mixer.fadeout(1000)
			self.soundList[sound].play(loops, fade_ms=fade_ms)

	def mute(self):
		pygame.mixer.stop()


	##############################
	# various sound events below #
	##############################

	def playAttack(self):
		''' plays (random) attack sound '''
		rand = random.randint(0, 2)
		self.attackSounds[rand].play()


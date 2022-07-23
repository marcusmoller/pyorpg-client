import random
import pygame
import pygame.mixer
from pygame.locals import *

from constants import *
import global_vars as g


class SoundEngine():
    def __init__(self):
        if not pygame.mixer: print("Warning, sounds are disabled!")
        pygame.mixer.init()

        # states
        self.playingSound = False
        self.sfxMuted = False
        self.musicMuted = False

        # sounds
        self.soundList = []
        self.musicList = []
        self.attackSounds = []
        self.spellSounds = []

    def loadSounds(self):
        self.soundList.append(self.loadFile(g.dataPath + "/music/0.ogg"))
        self.soundList.append(self.loadFile(g.dataPath + "/music/1.ogg"))

        self.attackSounds.append(self.loadFile(g.dataPath + "/sounds/swing_1.ogg"))
        self.attackSounds.append(self.loadFile(g.dataPath + "/sounds/swing_2.ogg"))
        self.attackSounds.append(self.loadFile(g.dataPath + "/sounds/swing_3.ogg"))

        self.spellSounds.append(self.loadFile(g.dataPath + "/sounds/spell.ogg"))
        self.spellSounds.append(self.loadFile(g.dataPath + "/sounds/spell_subhp.ogg"))

    def loadFile(self, filename):
        sound = pygame.mixer.Sound(filename)
        return sound

    def play(self, sound, loops=False, fade_in=False):
        if not self.musicMuted:
            if fade_in == True:
                fade_ms = 1000
            else:
                fade_ms = 0

            pygame.mixer.fadeout(1000)
            self.soundList[sound].play(loops, fade_ms=fade_ms)

            print('PLAYING SOUND: ' + str(sound))

    def mute(self):
        pygame.mixer.stop()


    ##############################
    # various sound events below #
    ##############################

    def playAttack(self):
        ''' plays (random) attack sound '''
        if not self.sfxMuted:
            rand = random.randint(0, 2)
            self.attackSounds[rand].play()

    def playSpell(self, soundNum=0):
        ''' plays spell sound '''
        if not self.sfxMuted:
            self.spellSounds[soundNum].play()

    def playSpellHit(self, spellType):
        if not self.sfxMuted:
            if spellType == SPELL_TYPE_ADDHP:
                self.spellSounds[0].play()

            elif spellType == SPELL_TYPE_SUBHP:
                self.spellSounds[1].play()
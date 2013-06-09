import pickle
import global_vars as g
from objects import *


def saveMap(mapNum):
    pickle.dump(Map, open(g.dataPath + "/maps/" + str(mapNum) + ".pom", 'wb'))


def loadMap(mapNum):
    Map = pickle.load(open(g.dataPath + "/maps/" + str(mapNum) + ".pom", 'rb'))


def clearPlayer(index):
    Player[index] = PlayerClass()

def clearMap():
    Map = MapClass()


''' Player name '''
def getPlayerName(index):
    return Player[index].Name

def setPlayerName(index, name):
    Player[index].Name = name


''' player class '''
def getPlayerClass(index):
    return Player[index].Class

def setPlayerClass(index, newClass):
    Player[index].Class = newClass


''' Player sprite '''
def getPlayerSprite(index):
    return Player[index].sprite

def setPlayerSprite(index, sprite):
    Player[index].sprite = sprite


''' player level '''
def getPlayerLevel(index):
    return Player[index].level

def setPlayerLevel(index, level):
    Player[index].level = level


''' player exp '''
def getPlayerExp(index):
    return Player[index].exp

def setPlayerExp(index, exp):
    Player[index].exp = exp


''' player access '''
def getPlayerAccess(index):
    return Player[index].access

def setPlayerAccess(index, access):
    Player[index].access = access
    print access


''' player vital '''
def getPlayerVital(index, vital):
    return Player[index].vitals[vital]

def setPlayerVital(index, vital, value):
    Player[index].vitals[vital] = value

    if getPlayerVital(index, vital) > getPlayerMaxVital(index, vital):
        Player[index].vitals[vital] = getPlayerMaxVital(index, vital)


''' player max vital '''
def getPlayerMaxVital(index, vital):
    if vital == Vitals.hp:
        return Player[index].maxHP
    elif vital == Vitals.mp:
        return Player[index].maxMP
    elif vital == Vitals.sp:
        return Player[index].maxSP

''' player stats '''
def getPlayerStat(index, stat):
    return Player[index].stats[stat]

def setPlayerStat(index, stat, value):
    Player[index].stats[stat] = value


''' player stats points '''
def getPlayerPoints(index):
    return Player[index].statsPoints

def setPlayerPoints(index, points):
    Player[index].statsPoints = points


''' player direction '''
def getPlayerDir(index):
    return Player[index].Dir

def setPlayerDir(index, direction):
    Player[index].Dir = direction


''' player map '''
def getPlayerMap(index):
    return Player[index].Map

def setPlayerMap(index, mapNum):
    Player[index].Map = mapNum


''' Player x '''
def getPlayerX(index):
    return Player[index].x

def setPlayerX(index, x):
    Player[index].x = x


''' Player y '''
def getPlayerY(index):
    return Player[index].y

def setPlayerY(index, y):
    Player[index].y = y
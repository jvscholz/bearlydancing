import math, pygame, sys, random

from Game import Game
from FRect import FRect

from .GridGame import GridGame
from .SubGrid import SubGrid
from .Lava import Lava, zeroposfunction
from .Ship import Ship
from .simulatedifficulty import simulatedifficulty
from .randomsubgrid import randomgrid


def crazysquare(time):
    
    time = (time / 1000.0) % 2

    if time < 1:
        return (0, -time/4.0)
    else:
        return (0, -(1 - (time-1))/4.0)


# first test simulateddifficulty
# testlavas = [Lava(FRect(.5, .5, .5, .5), crazysquare)]

#print(simulatedifficulty(SubGrid(FRect(0,0,1.5,1), testlavas), 1000, None, 0.05))


# all coordinates are expressed as a fraction of screen height

currentgame = None
pixelsize = 0.05
gamestarttime = None

def gettime(outsidetime):
    global gamestarttime
    if gamestarttime == None:
        gamestarttime = outsidetime
        return 0
    else:
        return outsidetime-gamestarttime

    
def generatenewgame():

    currentdifficulty = 0.5
    subgrids = []
    #for i in range(2):
    #    subgrids.append(randomgrid(1.4, 0.4, currentdifficulty, pixelsize))
    subgrids.append(SubGrid(FRect(0,0,1,1), [Lava(FRect(0.5, 0.5, 0.2, 0.2), zeroposfunction)]))
    subgrids.append(SubGrid(FRect(0,0,1,1), [Lava(FRect(0.5, 0.5, 0.2, 0.2), zeroposfunction)]))
    subgrids.append(SubGrid(FRect(0,0,1,1), [Lava(0.5, 0.5, 0.2, 0.2)]))
    global gamestarttime
    gamestarttime = None
        
    return GridGame(subgrids, Ship())


def initgridgame(screen):
    global currentgame
    currentgame = generatenewgame()

    
def onkey(outsidetime, settings, event):
    time = gettime(outsidetime)
    global currentgame
    currentgame = currentgame.onkey(time, settings, event, pixelsize)

    
def ontick(outsidetime, settings):
    time = gettime(outsidetime)
    global currentgame
    currentgame = currentgame.ontick(time, settings)
    
    if currentgame.gameoverp(time, settings, pixelsize):
        pygame.quit()
        sys.exit()
        

def ondraw(outsidetime, settings, screen):
    time = gettime(outsidetime)
    screen.fill((0,0,0))
    currentgame.draw(time, settings, screen, pixelsize)

def onunpause(time):
    pass

def creategame():
    return Game("gridgame", initgridgame, onkey, ontick, ondraw, onunpause)

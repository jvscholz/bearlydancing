import pygame
from collections import OrderedDict
from FrozenClass import FrozenClass

class Settings(FrozenClass):

    def __init__(self):
        # keybindings
        self.keydict = OrderedDict()
        self.keydict["up"] =[pygame.K_UP, pygame.K_w]
        self.keydict["down"] = [pygame.K_DOWN, pygame.K_s]
        self.keydict["left"] = [pygame.K_LEFT, pygame.K_a]
        self.keydict["right"] = [pygame.K_RIGHT, pygame.K_d]
        self.keydict["action"] = [pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER]
        self.keydict["zoom"] = [pygame.K_z]
        self.keydict["note1"] = [pygame.K_a]
        self.keydict["note2"] = [pygame.K_s]
        self.keydict["note3"] = [pygame.K_d]
        self.keydict["note4"] = [pygame.K_f]
        self.keydict["note5"] = [pygame.K_j]
        self.keydict["note6"] = [pygame.K_k]
        self.keydict["note7"] = [pygame.K_l]
        self.keydict["note8"] = [pygame.K_SEMICOLON]
        self.keydict["notemodifier"] = [pygame.K_SPACE]
        self.keydict["note1modified"] = [pygame.K_w]
        self.keydict["note2modified"] = [pygame.K_e]
        self.keydict["note3modified"] = [pygame.K_r]
        self.keydict["note4modified"] = [pygame.K_t]
        self.keydict["note5modified"] = [pygame.K_i]
        self.keydict["note6modified"] = [pygame.K_o]
        self.keydict["note7modified"] = [pygame.K_p]
        self.keydict["note8modified"] = [pygame.K_LEFTBRACKET]
        
        self.keydict["escape"] = [pygame.K_ESCAPE]


        # normal setting stuff
        self.windowmode = "fullscreen"
        self.volume = 0.5
        self.autosavep = True

        # state can be world, battle, game, or conversation
        self.state = "world"
        self.backgroundstate = "world"
        self.menuonq = True

        # zoom level is for viewing the world- gets added to the display scale
        self.zoomlevel = 0

        #possible soundpacks can be seen by listing the keys in all_sounds in play_sound
        self.soundpack = "sine"

        # the index in the player.scales currently chosen
        self.scaleindex = 0
        
        # the number of (length 1) notes that can be shown on screen at once before the pad
        self.notes_per_screen = 6

        # maximum number of volume envelopes to apply per frame,
        # since it is expensive
        self.maxvolumeenvelopesperframe = 1

        self.username = "Greg" # the names should always end up overwritten
        self.bearname = "Honey"

        # master clock
        self.current_time = 0

        # this is an offset for all enemy levels
        self.difficulty = 0

        self.dancepadmodep = True

        # gamedata is a dict that can be populated by Game objects
        self.gamedata = {}
        self.currentgame = None
        
        self._freeze()

    def iskey(self,binding, pygamekey):
        return pygamekey in self.keydict[binding]
        
    def soundonp(self):
        return self.volume != 0

    def updatezoom(self, displayscale):
        self.zoomlevel = self.zoomlevel+1
        if self.zoomlevel == 2:
            self.zoomlevel += 1
        elif self.zoomlevel > 2:
            self.zoomlevel = 0

    def setgamedata(gamename, gamedata):
        self.gamedata[gamename] = gamedata

    def getgamedata(gamename):
        return self.gamedata[gamename]

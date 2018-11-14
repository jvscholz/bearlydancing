import pygame, variables, random, os
from graphics import drawwave
from Soundpack import Soundpack

from pygame import Rect

# nessoundfont = "soundfonts/The_Nes_Soundfont.sf2"


# each soundpack is a list of sounds from A3 to A6
# value of 0 corresponds to A4, -12 is A3
all_tones = {"sine": Soundpack("sine", 1), "square": Soundpack("square", 25),
             "triangle": Soundpack("triangle", 30), "sawtooth": Soundpack("sawtooth", 30),
             "random":Soundpack("random", 8)}

def currentsoundpack():
    return all_tones[variables.settings.soundpack]

# all possible soundpacks
soundpackkeys = list(all_tones.keys())

scales = {"C major" : [2, 2, 1, 2, 2, 2, 1],
          "C minor" : [2, 1, 2, 2, 1, 3, 1],
          "chromatic" : [1, 1, 1, 6, 1, 1, 1]}# list of offsets for the scale

def loadmusic(filename):
    return pygame.mixer.Sound(os.path.join(variables.pathtoself, "music/", filename))

onedrum = loadmusic("onedrum.wav")
menumusic = loadmusic("menu.wav")
bearhome = loadmusic("bearhome.wav")
engagebattle = loadmusic("encounterenemy.wav")

channels = []
for x in range(37):
    channels.append(pygame.mixer.Channel(x))

# stores time in milliseconds of the current end of the music queued on the channel
# none if not playing
channeltimes = [None]*37

musicchannel = pygame.mixer.Channel(37)
soundeffectchannel = pygame.mixer.Channel(38)

def buffertosound(b):
    return pygame.sndarray.make_sound(b)

def play_tone(tonein, volenvelope):
    t = tonein
    # make t always in range if out of range
    if t+12>=len(all_tones[variables.settings.soundpack].loopbuffers):
        t = len(all_tones[variables.settings.soundpack].loopbuffers)-1-12
    elif t+12 < 0:
        t = 0-12

    # add because values are centered on 0
    sp = all_tones[variables.settings.soundpack]
    channels[t+12].set_volume(variables.settings.volume) # balance volume
    buf = sp.getbufferattime(t+12, 0, volenvelope, True)
    channels[t+12].play(buffertosound(buf))
    displaywave(buf, t+12, 0)
 
    channeltimes[t+12] = sp.loopbufferdurationmillis[t+12]

# tonein is a index of the tone to play
# volenvelope is the name of the volenvelope to use
# numofupdatetonessofar is how many times we have called it so far
# this allows us to put a cap on the number of
# volumeenvelopes to apply, since it is expensive
def update_tone(tonein, volenvelope, numofupdatetonessofar):
    updatevolenvelopep = numofupdatetonessofar < variables.settings.maxvolumeenvelopesperframe
    
    t = tonein
    if t+12>=len(all_tones[variables.settings.soundpack].loopbuffers):
        t = len(all_tones[variables.settings.soundpack].loopbuffers)-1-12
    elif t+12 < 0:
        t = 0-12

    c = channels[t+12]
    sp = all_tones[variables.settings.soundpack]

    if channeltimes[t+12] == None:
        channeltimes[t+12] = 0
    
    c.set_volume(variables.settings.volume)
    if c.get_queue() == None:
        buf = sp.getbufferattime(t+12, channeltimes[t+12], volenvelope, updatevolenvelopep)
        c.queue(buffertosound(buf))
        channeltimes[t+12] += sp.loopbufferdurationmillis[t+12]
        displaywave(buf, t+12, numofupdatetonessofar)

def stop_tone(tonein):
    t = tonein
    if t+12>=len(all_tones[variables.settings.soundpack].loopbuffers):
        t = len(all_tones[variables.settings.soundpack].loopbuffers)-1-12
    elif t+12 < 0:
        t = 0-12
    if not t == None:
        channels[t+12].stop()
        channeltimes[t+12] = None
        stopdisplaywave(t+12)

displaytuples = [None] * 37
displaywavex = 0
        
def displaywave(buf, channel, drawnsofar):
    global displaywavex
    t = displaytuples[channel]
    waveamp = variables.gettextsize()
    if t == None:
        # init a new display tuple
        displaytuples[channel] = (0, random.randint(waveamp, int(variables.getpadypos() -waveamp)), (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        t = displaytuples[channel]

    wavex = displaywavex
    wavey = t[1]
    # make it so that each second crosses .2 of the width of the screen
    wavelen = (buf.size/2)/variables.sample_rate * 0.2 * variables.width
    skiplen = len(buf)/wavelen
    drawwave(buf, skiplen, wavex, wavey, waveamp, wavelen, t[2], False)

    # now just update once and let it stay on screen
    pygame.display.update(Rect(wavex, wavey-waveamp, wavelen, waveamp*2))

    displaytuples[channel] = (wavex+wavelen, wavey, t[2])

    if drawnsofar == 0:
        displaywavex = (displaywavex + wavelen)
        maxwavex = (variables.width*9/12)
        if displaywavex > maxwavex:
            displaywavex -= maxwavex
            variables.dirtyrects = [Rect(0,0,variables.width,variables.height)]
        
        

def stopdisplaywave(channel):
    displaytuples[channel] = None

def getsoundvar(s):
    g = globals()
    return g[s]
        
def play_effect(s):
    sound = getsoundvar(s)
    soundeffectchannel.set_volume(variables.settings.volume)
    soundeffectchannel.play(sound)

def play_music(s):
    sound = getsoundvar(s)
    musicchannel.set_volume(variables.settings.volume)
    musicchannel.play(sound, loops=-1)

def stop_music():
    musicchannel.stop()

def stop_effect():
    soundeffectchannel.stop()

############################################ grassland music #########################################
finalgrassmelody = pygame.mixer.Sound(os.path.join(variables.pathtoself, "music/modmusicgrassland/melodyfinal.wav"))
grassmelodys = []
INDEXES = []
for x in range(13):
    grassmelodys.append(pygame.mixer.Sound(os.path.join(variables.pathtoself, "music/modmusicgrassland/melody" + str(x) + ".wav")))
    INDEXES.append(x)
    
indexes_left = INDEXES.copy()

grassdrums = []
for x in range(6):
    grassdrums.append(pygame.mixer.Sound(os.path.join(variables.pathtoself, "music/modmusicgrassland/drum" + str(x) + ".wav")))

def initiatedrums():
    sound = random.choice(grassdrums)
    soundeffectchannel.set_volume(variables.settings.volume)
    soundeffectchannel.play(sound)
    
def nextgrasslandsound():
    global indexes_left
    if len(indexes_left) > 0:
        index = random.choice(indexes_left)
        indexes_left.remove(index)
        return grassmelodys[index]
    else:
        indexes_left = INDEXES.copy()
        return finalgrassmelody

def initiatemelody():
    indexes_left = INDEXES.copy()
    sound = nextgrasslandsound()
    musicchannel.set_volume(variables.settings.volume)
    musicchannel.play(sound)
    
def initiategrasslandmusic():
    initiatemelody()
    initiatedrums()

def grasslandmusictick():
    if not musicchannel.get_busy():
        initiatemelody()
        initiatedrums()
    elif musicchannel.get_queue() == None:
        sound = nextgrasslandsound()
        musicchannel.set_volume(variables.settings.volume)
        musicchannel.queue(sound)

    if not soundeffectchannel.get_busy():
        initiatedrums()
    elif soundeffectchannel.get_queue() == None:
        sound = random.choice(grassdrums)
        soundeffectchannel.set_volume(variables.settings.volume)
        soundeffectchannel.queue(sound)

def setnewvolume():
    musicchannel.set_volume(variables.settings.volume)
    soundeffectchannel.set_volume(variables.settings.volume)
        

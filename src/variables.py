import pygame, ctypes, os, pickle
from pygame import Rect
from Settings import Settings
from Properties import Properties

# Setup
pygame.mixer.pre_init(22050, -16, 2, 128)
pygame.mixer.init()
pygame.init()
pygame.mixer.set_num_channels(46)

# Set the width and height of the screen [width,height]
modes = pygame.display.list_modes()
ctypes.windll.user32.SetProcessDPIAware()
mode = modes[0]
height = int(mode[1]/2)
width = int(mode[0]/2)
hh = height/2
hw = width/2
flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
screen = pygame.display.set_mode(mode, flags)
#screen = pygame.Surface([height, width])

unrounded_displayscale = height*0.0025
displayscale = round(unrounded_displayscale) #the master scaling factor for importing pixel art

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 255, 0)

#general
scaleoffset = 1
fontlist = pygame.font.get_fonts()
fontname = "use default"
if "orangekidregular" in fontlist:
    fontname = "orangekidregular"
font = pygame.font.SysFont(fontname, 30)
newworldeachloadq = False

# map stuff
# pinetreesused is used to keep track of how many random trees are used
pinetreesused = 0
grasslandsused = 0
greyrocksused = 0

def num_of_generated_graphics_used():
    return pinetreesused + grasslandsused + greyrocksused

basemapsize = 360

TREEWIDTH = 100
TREEHEIGHT = 200
TREECOLLIDESECTION = [0, 18.5 / 20, 1, 1.5 / 20]

# battle
healthanimationspeed = 2000# time in milliseconds for the health bar animation to go
expanimationspeed = 3000
dancespeed = height/8 * 0.001# factor for displaying notes
padypos = height*(13/16)

generic_specs = {'maxtime' : 20, 'lv' : 0, 'rules' : []}
melodic_specs = {'maxtime' : 20, 'lv' : 0, 'rules' : ['melodic']}
maxvalue = 14
minvalue = -7

perfect_value = 2
good_value = 1
ok_value = 0.6
miss_value = 0
perfect_range = height/100
good_range = height/60
ok_range = height/25
miss_range = height/15

battle_volume = 0.1

notes_colors = [ORANGE, BLUE, RED, GREEN, GREEN, RED, BLUE, ORANGE]

#conversation
textbox_height = height*1/4
photo_size = width/6

#world
playerspeed = height/800 * 0.2#height/800 * 0.1 changed for development #factor against time
#encountering enemies
encounter_check_rate = 100 #rate of check in milliseconds
encounter_chance = 0.002#chance per check

settings = Settings()
properties = Properties()
properties_filename = "properties.txt"

def load_properties():
    global properties
    if os.path.isfile(os.path.abspath(properties_filename)):
        if os.path.getsize(os.path.abspath(properties_filename)) > 0:
            f = open(properties_filename, "rb")
            properties = pickle.load(f)

def save_properties():
    properties.num_of_generated_graphics = num_of_generated_graphics_used()
    with open("properties.txt", "wb") as f:
        pickle.dump(properties, f)

def draw_loading_text(string):
    text = pygame.transform.scale2x(font.render(string, 0, WHITE))
    xpos = int((width / 2) - (text.get_width() / 2))
    ypos = int((height / 2) - text.get_height() - height/10)
    screen.fill(BLACK, Rect(xpos-text.get_width(), ypos, text.get_width()*3, text.get_height()*2))
    screen.blit(text, [xpos, ypos])

def draw_progress_bar():
    numused = num_of_generated_graphics_used()
    estimated = properties.num_of_generated_graphics
    
    if numused == 1:
        draw_loading_text("generating world (2/2)")
        if estimated == None:
            pygame.display.flip()
    
    if not estimated == None:
        percent_complete = numused / estimated

        progresstext = pygame.transform.scale2x(font.render(str(numused) + "/" + str(estimated), 0, WHITE))

        texty = int(height/2 + height/5)
        
        screen.fill(BLUE, Rect(0, int(height/2), width*percent_complete, height/10))
        
        screen.fill(BLACK, Rect(0, int(height/2 + height/10), width, int(height/2 + progresstext.get_height()*2)))
        
        screen.blit(progresstext, [int(width/2 - progresstext.get_width()/2), texty])
        pygame.display.flip()

#helpful functions
def smaller(a, b):
    if a<b:
        return a
    else:
        return b

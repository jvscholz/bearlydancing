import pygame
import variables


def value_to_screenvalue(v):
    sv = v % 7
    if (sv == 0 and v >= 7):
        sv = 7
    elif (sv < 0):
        sv += 7
    return sv


class Note:
    # if they miss the note or stop playing it halfway ison will turn false and they will miss the note
    ison = True

    beginning_score = None
    end_score = None
    # pos is the coordinates of the bottom of the note
    pos = [0, 0]

    # drawing
    height_offset = 0

    def __init__(self, value, time, duration):
        # value is the placement in the current scale (instrument) that the note is, 0 is the first note, can go neg
        self.value = value
        self.screenvalue = None # until initialized
    
        # time is the value in number of beats from beginning
        self.time = time
        self.duration = duration

        # set in initialization
        self.shape = None
        self.secondshape = None

    # needs to be called after beatmap is created or changed
    def initialize(self):
        def beatshape(beatplace):
            if beatplace == 0:
                return "square"
            elif beatplace == 0.5:
                return "triangle"
            else:
                return "round"

        self.screenvalue = value_to_screenvalue(self.value)
        self.shape = beatshape(time%1)
        self.secondshape = beatshape((time+duration)%1)

    # still needs to be initialized after
    def newvalue(newval):
        self.value = newval
        

    def height(self, tempo):
        return self.duration * (variables.padypos / variables.settings.notes_per_screen)

    # bottom end of note included, top of note goes over height
    # detection is by the bottom of each end of the note
    def draw(self, tempo):
        
        width = variables.width / 20
        height = self.height(tempo)

        # subtract height to y because the pos is the bottom of the rectangle
        if self.ison:
            color = variables.notes_colors[self.screenvalue]
        else:
            color = variables.GREY

        darkercolor = []
        for rgbval in color:
            if rgbval -50 < 0:
                darkercolor.append(0)
            else:
                darkercolor.append(rgbval-50)

        end_height = variables.height / 80

        p = self.pos

        topendy = p[1] - height - end_height
        endx = p[0] - width/8
        endwidth = width * 1.25

        def drawend(x, y, color, endshape):
            if endshape == "square":
                pygame.draw.rect(variables.screen, color,
                                 [x, y, endwidth, end_height])
            elif endshape == "triangle":
                fourthx = endwidth/4
                centery = y + end_height/2
                pygame.draw.polygon(variables.screen, color,
                                    [[x, centery], [x+fourthx, y], [x+3*fourthx, y],
                                     [x+endwidth, centery], [x+3*fourthx, y+end_height], [x+fourthx, y+end_height]])
            elif endshape == "round":
                pygame.draw.ellipse(variables.screen, color,
                                    [x, y, endwidth, end_height])

        def drawmid(y, mheight, color):
            if mheight > 0:
                if self.shape == "square":
                    pygame.draw.rect(variables.screen, color, [p[0], y, width, mheight])
                elif self.shape == "triangle":
                    fourthx = width/4
                    pygame.draw.polygon(variables.screen, color,
                                        [[p[0]+3*fourthx, y], [p[0]+fourthx, y], [p[0], y + mheight/2],
                                         [p[0]+fourthx, y+mheight], [p[0]+3*fourthx, y+mheight], [p[0]+width, y + mheight/2]])
                elif self.shape == "round":
                    ellipsesurface = pygame.Surface((width, mheight), pygame.SRCALPHA)
                    pygame.draw.ellipse(ellipsesurface, color,
                                        [0, -20, width, mheight+40])
                    variables.screen.blit(ellipsesurface, [p[0], y])
                

        # subtract height from y because the pos is the bottom of the rectangle
        # the first case is if the note is currently being played
        if self.ison and variables.padypos > p[1] - height and self.beginning_score != None and self.end_score == None:
            mheight = height+1 - (p[1]-variables.padypos)
            drawmid(p[1]-height-1, mheight, darkercolor)
            drawend(endx, topendy, color, self.secondshape)
            #variables.dirtyrects.append(pygame.Rect(endx, topendy, endwidth, mheight+end_height))

        # second case is if the note was interrupted in the middle and counted as a miss
        elif not self.height_offset == 0:
            if (height - self.height_offset > 1):
                drawmid(p[1]-height-1, height+1-self.height_offset, darkercolor)
                drawend(endx, topendy, color, self.secondshape)
             #   variables.dirtyrects.append(pygame.Rect(endx, topendy, endwidth, height+end_height+1+self.height_offset))

        # third case is if it has either been missed or has not been played yet (normal draw)
        elif self.beginning_score == None or self.beginning_score == variables.miss_value or self.end_score == variables.miss_value:
            #middle of note
            drawmid(p[1]-height-1, height+2-end_height, darkercolor)
            #top
            drawend(endx, topendy, color, self.secondshape)
            #bottom of note
            drawend(endx, p[1]-end_height, color, self.shape)
            #variables.dirtyrects.append(pygame.Rect(endx, topendy, endwidth, height+end_height+2))

        #don't draw it if it has been played

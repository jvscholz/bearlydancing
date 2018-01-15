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
        # time is time in the whole song it is
        self.newvalue(value)
        self.time = time
        self.duration = duration

    def newvalue(self, v):
        self.value = v
        # from 0-7 even if it is out of those bounds so it can be played on the screen
        self.screenvalue = value_to_screenvalue(self.value)

    def height(self, tempo):
        return self.duration * (variables.padypos / variables.settings.notes_per_screen)

    # the ends of the notes are included in the height, and do not go out of it.
    def draw(self, tempo):
        width = variables.width / 20
        height = self.height(tempo)

        # subtract height to y because the pos is the bottom of the rectangle
        if self.ison:
            color = variables.notes_colors[self.screenvalue]
        else:
            color = variables.GRAY

        end_height = variables.height / 80

        p = self.pos

        # subtract height from y because the pos is the bottom of the rectangle
        # the first case is if the note is currently being played
        if self.ison and variables.padypos > p[1] - height and self.beginning_score != None and self.end_score == None:
            pygame.draw.rect(variables.screen, color,
                             [p[0] - width / 8, p[1] - height - end_height, width * 1.25, end_height])
            pygame.draw.rect(variables.screen, color, [p[0], p[1] - height - end_height, width,
                                                       height + end_height - (p[1] - variables.padypos)])

        # second case is if the note was interrupted in the middle and counted as a miss
        elif not self.height_offset == 0:
            if (height - self.height_offset > 1):
                pygame.draw.rect(variables.screen, color,
                                 [p[0] - width / 8, p[1] - height - end_height, width * 1.25, end_height])
                pygame.draw.rect(variables.screen, color,
                                 [p[0], p[1] - height - end_height, width, height + end_height - self.height_offset])

        # third case is if it has either been missed or has not been played yet (normal draw)
        elif self.beginning_score == None or self.beginning_score == variables.miss_value or self.end_score == variables.miss_value:
            #top of note
            pygame.draw.rect(variables.screen, color, [p[0], p[1] - height - end_height / 2, width, height])
            #middle
            pygame.draw.rect(variables.screen, color,
                             [p[0] - width / 8, p[1] - height - end_height, width * 1.25, end_height])
            #bottom of note
            pygame.draw.rect(variables.screen, color,
                             [p[0] - width / 8, p[1] - end_height, width * 1.25, end_height])

        #don't draw it if it has been played

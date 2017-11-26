#!/usr/bin/python
#Oliver Flatt works on Classes
import variables, pygame, graphics

class Speak():

    def __init__(self, pic, dialogue, side = None, bottomp = True):
        #dialogue is a list of strings, one per line. Writer has to make sure they fit
        self.pic = graphics.scale_pure(pic["img"], variables.photo_size)
        self.dialogue = dialogue
        self.side = side
        # can be a list of keys that work to exit the conversation
        self.specialexitkeys = None
        self.bottomp = bottomp
        self.releaseexit = False

        self.line = 0
        self.textsize = 0.5
        self.releaseexit = False

    def lines_in_sceen(self):
        line1 = graphics.sscale_customfactor(variables.font.render(self.dialogue[0], 0, variables.WHITE),
                                             self.textsize, False)
        return int(variables.textbox_height/line1.get_height())

    def draw(self):
        yoffset = 0
        if not self.bottomp:
            yoffset = -variables.height + variables.textbox_height
        #text
        line1 = graphics.sscale_customfactor(variables.font.render(self.dialogue[0], 0, variables.WHITE),
                                             self.textsize, False)
        line_height = line1.get_height()
        h = variables.height
        w = variables.width
        b = h-variables.textbox_height
        pygame.draw.rect(variables.screen, variables.BLACK, [0, b+yoffset, w, variables.textbox_height])
        numoflines = self.lines_in_sceen()
        if numoflines > len(self.dialogue):
            numoflines = len(self.dialogue)
        for x in range(0, numoflines):
            text = variables.font.render(self.dialogue[self.line+x], 0, variables.WHITE)
            line = graphics.sscale_customfactor(text, self.textsize)
            variables.screen.blit(line, [w/2 - line.get_width()/2, b+(line_height*x)+yoffset])

    def keypress(self, key):
        if self.line < len(self.dialogue) - self.lines_in_sceen():
            self.line += 1
            return "talking"
        elif self.specialexitkeys != None:
            if key in self.specialexitkeys:
                self.line = 0
                return "done"
        elif key in variables.settings.enterkeys:
            self.line = 0
            return "done"

    def keyrelease(self, key):
        self.keypress(key)

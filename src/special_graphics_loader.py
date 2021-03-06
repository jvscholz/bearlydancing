import pygame


import variables

def addsurfaceGR(GR, s, name, dimensions = None):
    if dimensions == None:
        dimensions = [s.get_width(), s.get_height()]
    GR[name] = {"img":s,"w":dimensions[0],"h":dimensions[1]}
    

def load_special_graphics(GR):
    # duplicate and rotate the left arrow
    leftdancearrow = GR["leftdancearrow"]["img"]
    rightdancearrow = pygame.transform.rotate(leftdancearrow,180)
    downdancearrow = pygame.transform.rotate(leftdancearrow,270)
    updancearrow = pygame.transform.rotate(leftdancearrow,90)

    leftdancearrowdark = leftdancearrow.copy()
    rightdancearrowdark = rightdancearrow.copy()
    updancearrowdark = updancearrow.copy()
    downdancearrowdark = downdancearrow.copy()

    pygame.PixelArray(leftdancearrow).replace((255,255,255), variables.brighten(variables.notes_colors[0], -40))
    pygame.PixelArray(rightdancearrow).replace((255,255,255), variables.brighten(variables.notes_colors[3], -40))
    pygame.PixelArray(updancearrow).replace((255,255,255), variables.brighten(variables.notes_colors[2], -40))
    pygame.PixelArray(downdancearrow).replace((255,255,255), variables.brighten(variables.notes_colors[1], -40))

    pygame.PixelArray(leftdancearrowdark).replace((255,255,255), variables.brighten(variables.notes_colors[0], -100))
    pygame.PixelArray(rightdancearrowdark).replace((255,255,255), variables.brighten(variables.notes_colors[3], -100))
    pygame.PixelArray(updancearrowdark).replace((255,255,255), variables.brighten(variables.notes_colors[2], -100))
    pygame.PixelArray(downdancearrowdark).replace((255,255,255), variables.brighten(variables.notes_colors[1], -100))

    pygame.PixelArray(leftdancearrow).replace((0,0,0), variables.notes_colors[0])
    pygame.PixelArray(rightdancearrow).replace((0,0,0), variables.notes_colors[3])
    pygame.PixelArray(updancearrow).replace((0,0,0), variables.notes_colors[2])
    pygame.PixelArray(downdancearrow).replace((0,0,0), variables.notes_colors[1])

    pygame.PixelArray(leftdancearrowdark).replace((0,0,0), variables.brighten(variables.notes_colors[0], -50))
    pygame.PixelArray(rightdancearrowdark).replace((0,0,0), variables.brighten(variables.notes_colors[3], -50))
    pygame.PixelArray(updancearrowdark).replace((0,0,0), variables.brighten(variables.notes_colors[2], -50))
    pygame.PixelArray(downdancearrowdark).replace((0,0,0), variables.brighten(variables.notes_colors[1], -50))


    GR["leftdancearrow"]["img"] = leftdancearrow
    addsurfaceGR(GR, rightdancearrow, "rightdancearrow")
    addsurfaceGR(GR, updancearrow, "updancearrow")
    addsurfaceGR(GR, downdancearrow, "downdancearrow")

    addsurfaceGR(GR, leftdancearrowdark, "leftdancearrowdark")
    addsurfaceGR(GR, rightdancearrowdark, "rightdancearrowdark")
    addsurfaceGR(GR, updancearrowdark, "updancearrowdark")
    addsurfaceGR(GR, downdancearrowdark, "downdancearrowdark")

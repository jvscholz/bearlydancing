#!/usr/bin/python
import pygame, variables

LOADINGTEXT = pygame.transform.scale2x(variables.font.render("LOADING...", 0, variables.WHITE))
variables.screen.blit(LOADINGTEXT, [0,0])
variables.wide_screen.blit(LOADINGTEXT, [0, 0])
pygame.display.flip()

import maps
import conversations, classvar, Menu

Menu.load()

pygame.display.set_caption("Bearly Dancing")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

maps.new_scale_offset()

menu = Menu.Menu()

#clear all the events so it does not mess up the game when it loads
pygame.event.get()

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing- this is like keyPressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and event.key in variables.settings.enterkeys and variables.settings.menuonq and \
                        menu.options[menu.option] == "exit":
            done = True

        # User pressed down on a key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                #if we are turning on the menu pause the beatmaps
                if(not variables.settings.menuonq):
                    if(not isinstance(classvar.battle, str)):
                        classvar.battle.pause()
                else:
                    if (not isinstance(classvar.battle, str)):
                        classvar.battle.unpause()
                variables.settings.menuonq = not variables.settings.menuonq
                classvar.player.change_of_state()
            if (not variables.settings.menuonq):
                if variables.settings.state == "conversation":
                    conversations.currentconversation.keypress(event.key)
                elif variables.settings.state == "world":
                    classvar.player.keypress(event.key)
                    maps.on_key(event.key)
                elif variables.settings.state == "battle":
                    classvar.battle.onkey(event.key)
            else:
                menu.onkey(event.key)


        # User let up on a key
        elif event.type == pygame.KEYUP:
            if (not variables.settings.menuonq):
                if variables.settings.state == "world":
                    classvar.player.keyrelease(event.key)
                elif variables.settings.state == "battle":
                    classvar.battle.onrelease(event.key)

    # --- Game Logic
    if (not variables.settings.menuonq):
        if variables.settings.state == "world":
            classvar.player.move()
            maps.checkexit()
            maps.current_map.on_tick()
            maps.checkconversation()
        elif variables.settings.state == "battle":
            classvar.battle.ontick()

    # --- Drawing Code
    variables.screen.fill(variables.WHITE)
    if variables.settings.state == "conversation":
        maps.current_map.draw(classvar.player.xpos, classvar.player.ypos)
        classvar.player.draw()
        maps.current_map.draw_foreground()
        conversations.currentconversation.draw()
    elif variables.settings.state == "world":
        maps.current_map.draw(classvar.player.xpos, classvar.player.ypos)
        classvar.player.draw()
        maps.current_map.draw_foreground()
    elif variables.settings.state == "battle":
        classvar.battle.draw()

    if (variables.settings.menuonq):
        menu.draw()

    # put the screen on the widescreen
    pygame.draw.rect(variables.wide_screen, variables.BLACK, [0, 0, variables.mode[0], variables.mode[1]])
    variables.wide_screen.blit(variables.screen, [int(variables.mode[0] / 2 - variables.width / 2), 0])

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

    # add the past tick to the current time
    variables.settings.current_time += clock.get_time()

# Close the window and quit, this is after the main loop has finished
pygame.quit()

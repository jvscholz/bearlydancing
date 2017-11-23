#!/usr/bin/python
import pygame, variables, copy
from pygame import Rect

variables.load_properties()
variables.draw_loading_text("importing graphics (1/2)")
pygame.display.flip()

# now go ahead and load everything in
import maps
import conversations, classvar, Menu

# save the properties to record how many things needed to be loaded
variables.save_properties()

pygame.display.set_caption("Bearly Dancing")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

maps.new_scale_offset()

#clear all the events so it does not mess up the game when it loads
pygame.event.get()

menu = Menu.load()

# -------- Main Program Loop -----------
while not done:
    # add the past tick to the current time
    variables.settings.current_time += clock.get_time()
    
    # --- Event Processing- this is like keyPressed
    for event in pygame.event.get():
        #first check for saving and exiting
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and event.key in variables.settings.enterkeys and variables.settings.menuonq:
            if menu.options[menu.option] == "exit":
                done = True
            elif menu.options[menu.option] == "save":
                Menu.save(menu)

        # User pressed down on a key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                #if we are turning on the menu pause the beatmaps
                if(not variables.settings.menuonq):
                    if(not isinstance(classvar.battle, str)):
                        classvar.battle.pause()
                else:
                    if (not isinstance(classvar.battle, str)):
                        classvar.battle.unpause()
                variables.settings.menuonq = not variables.settings.menuonq
                menu.reset()
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
            maps.checkconversation()
            maps.checkexit()
            maps.current_map.on_tick()
        elif variables.settings.state == "battle":
            classvar.battle.ontick()

    # --- Drawing Code

    def draw_world():
        classvar.player.update_drawpos()
        maps.current_map.draw([classvar.player.mapdrawx, classvar.player.mapdrawy])
        classvar.player.draw()
        maps.current_map.draw_foreground([classvar.player.mapdrawx, classvar.player.mapdrawy])

        #fill edges in with black
        screenxoffset = maps.current_map.screenxoffset
        if screenxoffset != 0:
            variables.screen.fill(variables.BLACK,
                                  Rect(0, 0, screenxoffset, variables.height))
            variables.screen.fill(variables.BLACK,
                                  Rect(variables.width-screenxoffset-1, 0, screenxoffset+1, variables.height))
    
    if variables.settings.state == "conversation":
        if variables.settings.backgroundstate == "world":
            draw_world()
        else:
            variables.screen.fill(variables.BLACK)
            classvar.battle.draw()
        conversations.currentconversation.draw()
    elif variables.settings.state == "world":
        draw_world()
    elif variables.settings.state == "battle":
        variables.screen.fill(variables.BLACK)
        classvar.battle.draw()

    if (variables.settings.menuonq):
        menu.draw()


    # blit fps
    variables.screen.blit(variables.font.render(str(clock.get_fps()), 0, variables.WHITE), [20, 20])
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit frames per second
    clock.tick(240)

# Close the window and quit, this is after the main loop has finished
pygame.quit()

import pygame
from pygame.locals import *
from editordummy import Dummy
from camera import Camera

def run(clock, states, level):

    # Set up the window for this game state
    gameWindow = pygame.display.get_surface()
    pygame.display.set_caption("Editor: " + level)

    # Set up sprite groups
    sprites = pygame.sprite.Group()
    dummies = pygame.sprite.Group()
    Dummy.containers = sprites, dummies

    # Load and parse the level text file
    leveltext = open(level, "r")
    for line in leveltext:
        line = line.split()
        if len(line) > 0:
            if line[0] == "dimensions":
                LEVEL_WIDTH, LEVEL_HEIGHT = int(line[1]), int(line[2])
            else:
                Dummy(line)

    # Create the camera
    camera = Camera(0, 0, LEVEL_WIDTH, LEVEL_HEIGHT)

    # Create the variables to track editor tools
    clickStart = [0, 0]
    justSaved = False

    while True:

        # Get events on the event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                return states["quit"]
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return states["menu"]
                elif event.key == K_w:
                    camera.setSpeedY(camera.getSpeedY() - 5)
                elif event.key == K_a:
                    camera.setSpeedX(camera.getSpeedX() - 5)
                elif event.key == K_s:
                    if pygame.key.get_mods() & KMOD_CTRL:
                        leveltext = open(level, "w")
                        # Save level dimensions
                        leveltext.write("dimensions " + str(LEVEL_WIDTH) + " " + str(LEVEL_HEIGHT) + "\n")
                        # Add all dummy objects to level data
                        for dummy in dummies:
                            if dummy.getType() == "platform":
                                leveltext.write(dummy.getType() + " " + str(dummy.rect.left) + " " + str(dummy.rect.top) + " " + str(dummy.rect.width) + " " + str(dummy.rect.height) + "\n")
                            elif dummy.getType() == "enemy":
                                leveltext.write(dummy.getType() + " " + str(dummy.rect.left) + " " + str(dummy.rect.top) + "\n")
                        justSaved = True
                        print "Level saved as " + level
                    else:
                        camera.setSpeedY(camera.getSpeedY() + 5)
                elif event.key == K_d:
                    camera.setSpeedX(camera.getSpeedX() + 5)
            elif event.type == KEYUP:
                if event.key == K_w:
                    camera.setSpeedY(camera.getSpeedY() + 5)
                elif event.key == K_a:
                    camera.setSpeedX(camera.getSpeedX() + 5)
                elif event.key == K_s:
                    if not justSaved:
                        camera.setSpeedY(camera.getSpeedY() - 5)
                    else:
                        justSaved = False
                elif event.key == K_d:
                    camera.setSpeedX(camera.getSpeedX() - 5)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    clickStart = [mouse[0] + camera.getX(), mouse[1] + camera.getY()]
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    clickEnd = [mouse[0] + camera.getX(), mouse[1] + camera.getY()]
                    if clickEnd[0] < clickStart[0]:
                        clickEnd[0], clickStart[0] = clickStart[0], clickEnd[0]
                    if clickEnd[1] < clickStart[1]:
                        clickEnd[1], clickStart[1] = clickStart[1], clickEnd[1]
                    Dummy(["platform", clickStart[0], clickStart[1], clickEnd[0] - clickStart[0], clickEnd[1] - clickStart[1]])

        camera.move()

        gameWindow.fill((18, 188, 255))
        for sprite in sprites:
            gameWindow.blit(sprite.image, (sprite.rect.left - camera.getX(), sprite.rect.top - camera.getY()))

        if pygame.mouse.get_pressed()[0]:
            mouse = pygame.mouse.get_pos()
            pygame.draw.rect(gameWindow, (212, 79, 12), (clickStart[0] - camera.getX(), clickStart[1] - camera.getY(), mouse[0] - (clickStart[0] - camera.getX()), mouse[1] - (clickStart[1] - camera.getY())))

        pygame.draw.line(gameWindow, (255, 0, 0), (-camera.getX(), -camera.getY()), (LEVEL_WIDTH - camera.getX(), -camera.getY()), 2)
        pygame.draw.line(gameWindow, (255, 0, 0), (-camera.getX(), -camera.getY()), (-camera.getX(), LEVEL_HEIGHT - camera.getY()), 2)
        pygame.draw.line(gameWindow, (255, 0, 0), (-camera.getX(), LEVEL_HEIGHT - camera.getY()), (LEVEL_WIDTH - camera.getX(), LEVEL_HEIGHT - camera.getY()), 2)
        pygame.draw.line(gameWindow, (255, 0, 0), (LEVEL_WIDTH - camera.getX(), -camera.getY()), (LEVEL_WIDTH - camera.getX(), LEVEL_HEIGHT - camera.getY()), 2)

        clock.tick(60)
        
        pygame.display.flip()


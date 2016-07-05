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
    Dummy.containers = sprites

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
    clickStart = (0, 0)

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
                    camera.setSpeedY(camera.getSpeedY() + 5)
                elif event.key == K_d:
                    camera.setSpeedX(camera.getSpeedX() + 5)
            elif event.type == KEYUP:
                if event.key == K_w:
                    camera.setSpeedY(camera.getSpeedY() + 5)
                elif event.key == K_a:
                    camera.setSpeedX(camera.getSpeedX() + 5)
                elif event.key == K_s:
                    camera.setSpeedY(camera.getSpeedY() - 5)
                elif event.key == K_d:
                    camera.setSpeedX(camera.getSpeedX() - 5)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    clickStart = (mouse[0] - camera.getX(), mouse[1] - camera.getY())
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    Dummy(["platform", clickStart[0], clickStart[1], mouse[0], mouse[1]])

        camera.move()

        gameWindow.fill((18, 188, 255))
        for sprite in sprites:
            gameWindow.blit(sprite.image, (sprite.rect.left - camera.getX(), sprite.rect.top - camera.getY()))

        pygame.draw.line(gameWindow, (255, 0, 0), (-camera.getX(), -camera.getY()), (LEVEL_WIDTH - camera.getX(), -camera.getY()), 2)
        pygame.draw.line(gameWindow, (255, 0, 0), (-camera.getX(), -camera.getY()), (-camera.getX(), LEVEL_HEIGHT - camera.getY()), 2)
        pygame.draw.line(gameWindow, (255, 0, 0), (-camera.getX(), LEVEL_HEIGHT - camera.getY()), (LEVEL_WIDTH - camera.getX(), LEVEL_HEIGHT - camera.getY()), 2)
        pygame.draw.line(gameWindow, (255, 0, 0), (LEVEL_WIDTH - camera.getX(), -camera.getY()), (LEVEL_WIDTH - camera.getX(), LEVEL_HEIGHT - camera.getY()), 2)

        clock.tick(60)
        
        pygame.display.flip()

import pygame
from pygame.locals import *

def run(states):

    # Set up the window for this game state
    gameWindow = pygame.display.get_surface()
    pygame.display.set_caption("Menu")

    # Create Pygame clock to regulate frames
    clock = pygame.time.Clock()

    # Load needed images
    title = pygame.image.load("./rsc/title.png")
    kevin = pygame.image.load("./rsc/kevin.png")
    jing = pygame.image.load("./rsc/jing.png")

    while True:

        # Get events on the event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                return states["quit"]
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return states["quit"]
                elif event.key == K_SPACE:
                    return states["level"]
                elif event.key == K_z:
                    return states["level"]
                elif event.key == K_RETURN:
                    return states["editor"]
        
        clock.tick(60)

        # Draw the title screen
        gameWindow.fill((0, 0, 255))
        gameWindow.blit(title, (160, 90))
        gameWindow.blit(kevin, (180, 110))
        gameWindow.blit(jing, (670, 190))
        pygame.display.flip()

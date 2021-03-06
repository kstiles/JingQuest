import pygame, os, traceback
from pygame.locals import *

#import loading
import menu
import level
import leveleditor
#import results

def main():

    # Initialize Pygame
    pygame.init()

    # Create the window
    SCREEN_WIDTH = 960
    SCREEN_HEIGHT = 540
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    gameWindow = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create Pygame clock to regulate frames
    clock = pygame.time.Clock()

    # Create a list of game states and a variable to track current state
    states = {"quit" : -1,
              "loading" : 0,
              "menu" : 1,
              "level" : 2,
              "results" : 3,
              "editor" : 4
              }
    
    gameState = states["menu"]

    while gameState != states["quit"]:
        if gameState == states["loading"]:
            pass
        elif gameState == states["menu"]:
            gameState = menu.run(states)
        elif gameState == states["level"]:
            gameState = level.run(states)
        elif gameState == states["editor"]:
            gameState = leveleditor.run(states, "./levels/level.lvl")

    

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
    

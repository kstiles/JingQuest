import pygame
from pygame.locals import *
from editordummy import Dummy
from camera import Camera
from toolbar import Toolbar

def run(states, level):

    # Set up the window for this game state
    gameWindow = pygame.display.get_surface()
    pygame.display.set_caption("Editor: " + level)

    # Get the window width and height
    rect = gameWindow.get_rect()
    SCREEN_WIDTH = rect.width
    SCREEN_HEIGHT = rect.height

    # Create Pygame clock to regulate frames
    clock = pygame.time.Clock()

    # Set up sprite groups
    sprites = pygame.sprite.Group()
    dummies = pygame.sprite.Group()
    Dummy.containers = sprites, dummies

    player = None

    # Load and parse the level text file
    leveltext = open(level, "r")
    for line in leveltext:
        line = line.split()
        if len(line) > 0:
            if line[0] == "dimensions":
                LEVEL_WIDTH, LEVEL_HEIGHT = int(line[1]), int(line[2])
            elif line[0] == "player":
                if player != None:
                    player.kill()
                player = Dummy(line)
            else:
                Dummy(line)

    # Create the camera
    camera = Camera(0, 0, LEVEL_WIDTH, LEVEL_HEIGHT)

    # Create the toolbar
    toolbar = Toolbar(SCREEN_WIDTH)

    # Create the variables for editor tools
    clickStart = [0, 0]
    justSaved = False
    
    makingPlatform = False

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
                            leveltext.write(dummy.getDataString())
                        justSaved = True
                        print "Level saved as " + level
                    else:
                        camera.setSpeedY(camera.getSpeedY() + 5)
                elif event.key == K_d:
                    camera.setSpeedX(camera.getSpeedX() + 5)
                elif event.key == K_SPACE:
                    toolbar.toggle()
                elif event.key == K_1:
                    toolbar.setTool("player")
                elif event.key == K_2:
                    toolbar.setTool("platform")
                elif event.key == K_3:
                    toolbar.setTool("enemy")
                elif event.key == K_4:
                    toolbar.setTool("datboi")
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
                    toolbarButton = toolbar.handleMouse(mouse, event.button)
                    
                    if toolbarButton == "none":
                        clickStart = snapToGrid([mouse[0] + camera.getX(), mouse[1] + camera.getY()])
                        if toolbar.getTool() == "platform":
                            makingPlatform = True
                        elif toolbar.getTool() == "enemy":
                            Dummy(["enemy", str(clickStart[0]), str(clickStart[1])])
                        elif toolbar.getTool() == "datboi":
                            Dummy(["datboi", str(clickStart[0]), str(clickStart[1] - 32)])
                        elif toolbar.getTool() == "player":
                            # Replace the old player dummy with the new one
                            if player != None:
                                player.kill()
                            player = Dummy(["player", str(clickStart[0]), str(clickStart[1])])

                    elif toolbarButton == "quit":

                        return states["menu"]
                            
                    elif toolbarButton == "save":
                        leveltext = open(level, "w")
                        # Save level dimensions
                        leveltext.write("dimensions " + str(LEVEL_WIDTH) + " " + str(LEVEL_HEIGHT) + "\n")
                        # Add all dummy objects to level data
                        for dummy in dummies:
                            leveltext.write(dummy.getDataString())
                        print "Level saved as " + level
                    
                elif event.button == 3:
                    mouse = pygame.mouse.get_pos()
                    for dummy in dummies:
                        if dummy.rect.left <= camera.getX() + mouse[0] <= dummy.rect.right and dummy.rect.top <= camera.getY() + mouse[1] <= dummy.rect.bottom:
                            dummy.kill()
                            break
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if toolbar.getTool() == "platform" and makingPlatform:
                        createPlatform(camera, clickStart)
                    makingPlatform = False

        camera.move()

        gameWindow.fill((18, 188, 255))
        for sprite in sprites:
            gameWindow.blit(sprite.image, (sprite.rect.left - camera.getX() + sprite.getOffset()[0], sprite.rect.top - camera.getY() + sprite.getOffset()[1]))

        if toolbar.getTool() == "platform" and pygame.mouse.get_pressed()[0] and makingPlatform:
            drawPreviewRect(gameWindow, camera, clickStart)

        drawGuidelines(gameWindow, camera, SCREEN_WIDTH, SCREEN_HEIGHT)
        drawBorderlines(gameWindow, camera, LEVEL_WIDTH, LEVEL_HEIGHT)

        toolbar.draw(gameWindow)

        clock.tick(60)
        
        pygame.display.flip()

def snapToGrid(point):

    return [int(point[0] / 32) * 32, int(point[1] / 32) * 32]

def drawPreviewRect(surface, camera, clickStart):

    mouse = pygame.mouse.get_pos()
    clickEnd = snapToGrid([mouse[0] + camera.getX(), mouse[1] + camera.getY()])

    # Correct the rectangle based on start and end click points
    # Case 1: clickStart top left, clickEnd bottom right
    if clickStart[0] <= clickEnd[0] and clickStart[1] <= clickEnd[1]:
        rectTopLeft = clickStart
        rectBottomRight = [clickEnd[0] + 32, clickEnd[1] + 32]
    # Case 2: clickStart top right, clickEnd bottom left
    elif clickStart[0] > clickEnd[0] and clickStart[1] <= clickEnd[1]:
        rectTopLeft = [clickEnd[0], clickStart[1]]
        rectBottomRight = [clickStart[0] + 32, clickEnd[1] + 32]
    # Case 3: clickStart bottom left, clickEnd top right
    elif clickStart[0] <= clickEnd[0] and clickStart[1] > clickEnd[1]:
        rectTopLeft = [clickStart[0], clickEnd[1]]
        rectBottomRight = [clickEnd[0] + 32, clickStart[1] + 32]
    # Case 4: clickStart bottom right, clickEnd top left
    elif clickStart[0] > clickEnd[0] and clickStart[1] > clickEnd[1]:
        rectTopLeft = clickEnd
        rectBottomRight = [clickStart[0] + 32, clickStart[1] + 32]
        
    pygame.draw.rect(surface, (212, 79, 12), (rectTopLeft[0] - camera.getX(), rectTopLeft[1] - camera.getY(), rectBottomRight[0] - rectTopLeft[0], rectBottomRight[1] - rectTopLeft[1]))    

def createPlatform(camera, clickStart):

    mouse = pygame.mouse.get_pos()
    clickEnd = snapToGrid([mouse[0] + camera.getX(), mouse[1] + camera.getY()])

    # Correct the rectangle based on start and end click points
    # Case 1: clickStart top left, clickEnd bottom right
    if clickStart[0] <= clickEnd[0] and clickStart[1] <= clickEnd[1]:
        rectTopLeft = clickStart
        rectBottomRight = [clickEnd[0] + 32, clickEnd[1] + 32]
    # Case 2: clickStart top right, clickEnd bottom left
    elif clickStart[0] > clickEnd[0] and clickStart[1] <= clickEnd[1]:
        rectTopLeft = [clickEnd[0], clickStart[1]]
        rectBottomRight = [clickStart[0] + 32, clickEnd[1] + 32]
    # Case 3: clickStart bottom left, clickEnd top right
    elif clickStart[0] <= clickEnd[0] and clickStart[1] > clickEnd[1]:
        rectTopLeft = [clickStart[0], clickEnd[1]]
        rectBottomRight = [clickEnd[0] + 32, clickStart[1] + 32]
    # Case 4: clickStart bottom right, clickEnd top left
    elif clickStart[0] > clickEnd[0] and clickStart[1] > clickEnd[1]:
        rectTopLeft = clickEnd
        rectBottomRight = [clickStart[0] + 32, clickStart[1] + 32]

    Dummy(["platform", rectTopLeft[0], rectTopLeft[1], rectBottomRight[0] - rectTopLeft[0], rectBottomRight[1] - rectTopLeft[1]])

def drawGuidelines(surface, camera, width, height):

    # Draw vertical gridlines
    for i in range(width / 32 + 1):
        pygame.draw.line(surface, (255, 255, 255), (32 * i - camera.getX() % 32, 0) , (32 * i - camera.getX() % 32, height))

    # Draw horizontal gridlines
    for i in range(height / 32 + 2):
        pygame.draw.line(surface, (255, 255, 255), (0, 32 * i - camera.getY() % 32), (width, 32 * i - camera.getY() % 32))

def drawBorderlines(surface, camera, width, height):
    # Draw the level borders
    pygame.draw.line(surface, (255, 0, 0), (-camera.getX(), -camera.getY()), (width - camera.getX(), -camera.getY()), 3)
    pygame.draw.line(surface, (255, 0, 0), (-camera.getX(), -camera.getY()), (-camera.getX(), height - camera.getY()), 3)
    pygame.draw.line(surface, (255, 0, 0), (-camera.getX(), height - camera.getY()), (width - camera.getX(), height - camera.getY()), 3)
    pygame.draw.line(surface, (255, 0, 0), (width - camera.getX(), -camera.getY()), (width - camera.getX(), height - camera.getY()), 3)

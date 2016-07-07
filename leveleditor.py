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

    # Create the variables for editor tools
    clickStart = [0, 0]
    justSaved = False
    
    currentTool = "platform"

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
                elif event.key == K_1:
                    currentTool = "platform"
                    print "tool set to platform"
                elif event.key == K_2:
                    currentTool = "enemy"
                    print "tool set to enemy"
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
                    clickStart[0] = int(clickStart[0] / 32) * 32
                    clickStart[1] = int(clickStart[1] / 32) * 32
                    if currentTool == "enemy":
                        Dummy(["enemy", str(clickStart[0]), str(clickStart[1])])
                elif event.button == 3:
                    mouse = pygame.mouse.get_pos()
                    for dummy in dummies:
                        if dummy.rect.left <= camera.getX() + mouse[0] <= dummy.rect.right and dummy.rect.top <= camera.getY() + mouse[1] <= dummy.rect.bottom:
                            dummy.kill()
                            break
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if currentTool == "platform":
                        createPlatform(camera, clickStart)

        camera.move()

        gameWindow.fill((18, 188, 255))
        for sprite in sprites:
            gameWindow.blit(sprite.image, (sprite.rect.left - camera.getX(), sprite.rect.top - camera.getY()))

        if currentTool == "platform" and pygame.mouse.get_pressed()[0]:
            drawPreviewRect(gameWindow, camera, clickStart)

        drawGuidelines(gameWindow, camera, LEVEL_WIDTH, LEVEL_HEIGHT)

        clock.tick(60)
        
        pygame.display.flip()

def drawPreviewRect(surface, camera, clickStart):

    mouse = pygame.mouse.get_pos()
    clickEnd = [mouse[0] + camera.getX(), mouse[1] + camera.getY()]
    clickEnd[0] = int(clickEnd[0] / 32) * 32
    clickEnd[1] = int(clickEnd[1] / 32) * 32

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
    clickEnd = [mouse[0] + camera.getX(), mouse[1] + camera.getY()]
    clickEnd[0] = int(clickEnd[0] / 32) * 32
    clickEnd[1] = int(clickEnd[1] / 32) * 32

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

    # Draw horizontal gridlines
    for i in range(width / 32):
        pygame.draw.line(surface, (255, 255, 255), (32 * i - camera.getX() % 32, 0) , (32 * i - camera.getX() % 32, height))

    # Draw vertical gridlines
    for i in range(height / 32 + 2):
        pygame.draw.line(surface, (255, 255, 255), (0, 32 * i - camera.getY() % 32), (width, 32 * i - camera.getY() % 32))

    # Draw the level borders
    pygame.draw.line(surface, (255, 0, 0), (-camera.getX(), -camera.getY()), (width - camera.getX(), -camera.getY()), 3)
    pygame.draw.line(surface, (255, 0, 0), (-camera.getX(), -camera.getY()), (-camera.getX(), height - camera.getY()), 3)
    pygame.draw.line(surface, (255, 0, 0), (-camera.getX(), height - camera.getY()), (width - camera.getX(), height - camera.getY()), 3)
    pygame.draw.line(surface, (255, 0, 0), (width - camera.getX(), -camera.getY()), (width - camera.getX(), height - camera.getY()), 3)

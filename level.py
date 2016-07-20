import pygame
from pygame.locals import *
from platform import Platform
from player import Player
from camera import Camera
from enemy import Enemy
from datboi import DatBoi
from friendlybullet import FriendlyBullet

def run(states):

    # Set up the window for this game state
    gameWindow = pygame.display.get_surface()
    pygame.display.set_caption("Level")

    # Create Pygame clock to regulate frames
    clock = pygame.time.Clock()

    # Set up sprite groups
    sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    friendlyBullets = pygame.sprite.Group()
    
    Player.containers = sprites, players
    Platform.containers = sprites, platforms
    Enemy.containers = sprites, enemies
    DatBoi.containers = sprites, enemies
    FriendlyBullet.containers = sprites, friendlyBullets

    # Load and parse the level text file
    leveltext = open("./levels/level.lvl", "r")
    for line in leveltext:
        line = line.split()
        if len(line) > 0:
            if line[0] == "platform":
                Platform(int(line[1]), int(line[2]), int(line[3]), int(line[4]))
            elif line[0] == "dimensions":
                LEVEL_WIDTH, LEVEL_HEIGHT = int(line[1]), int(line[2])
            elif line[0] == "enemy":
                Enemy(int(line[1]), int(line[2]))
            elif line[0] == "datboi":
                DatBoi(int(line[1]), int(line[2]))
            elif line[0] == "player":
                player = Player(int(line[1]), int(line[2]))

    # Create the camera
    camera = Camera(0, 0, LEVEL_WIDTH, LEVEL_HEIGHT)

    # Other level variables to be implemented
    gravity = 0.5

    while True:

        # Get events on the event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                return states["quit"]
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return states["menu"]
                elif event.key == K_z or event.key == K_UP:
                    player.jump()
                elif event.key == K_x:
                    player.shoot()

        # Move enemies with collision detection for platforms
        for enemy in enemies:
            enemy.moveX(platforms)
            enemy.moveY(platforms, gravity)
            
            # Refresh enemy images in case some enemies are damaged
            enemy.updateImage()

        # Move player bullets
        for bullet in friendlyBullets:
            bullet.move(enemies, platforms)

        # Move player with collision detection for platforms
        player.moveX(platforms)
        player.moveY(platforms, gravity)

        # Check for player hitting enemies
        player.checkEnemies(enemies)

        # Keep the player in the center of the screen
        camera.follow(player)
                
        # Refresh the window and redraw everything
        gameWindow.fill((18, 188, 255))
        for sprite in sprites:
            gameWindow.blit(sprite.image, (sprite.rect.left - camera.getX() + sprite.getOffset()[0], sprite.rect.top - camera.getY() + sprite.getOffset()[1]))
            #if type(sprite) is not Platform:
                #pygame.draw.rect(gameWindow, (255, 0, 0), (sprite.rect.left - camera.getX(), sprite.rect.top - camera.getY(), sprite.rect.width, sprite.rect.height), 2)

        # Limit FPS to 60 before displaying the next frame
        clock.tick(60)

        # Display the next frame
        pygame.display.flip()

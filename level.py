import pygame
from pygame.locals import *
from platform import Platform
from player import Player
from camera import Camera
from enemy import Enemy

def run(clock, states):

    # Set up the window for this game state
    gameWindow = pygame.display.get_surface()
    pygame.display.set_caption("Level")

    # Set up sprite groups
    sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    Player.containers = sprites, players
    Platform.containers = sprites, platforms
    Enemy.containers = sprites, enemies

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

    # Create the camera
    camera = Camera(0, 0, LEVEL_WIDTH, LEVEL_HEIGHT)

    # Other level variables to be implemented
    gravity = 0.5

    # Create the player
    player = Player()

    while True:

        # Get events on the event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                return states["quit"]
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return states["menu"]
                elif event.key == K_SPACE or event.key == K_UP:
                    if player.getCanJump():
                        player.setCanJump(False)
                        player.setSpeedY(-player.getMaxSpeedY())
                elif event.key == K_LEFT:
                    player.setSpeedX(player.getSpeedX() - player.getMaxSpeedX())
                elif event.key == K_RIGHT:
                    player.setSpeedX(player.getSpeedX() + player.getMaxSpeedX())
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    player.setSpeedX(player.getSpeedX() + player.getMaxSpeedX())
                elif event.key == K_RIGHT:
                    player.setSpeedX(player.getSpeedX() - player.getMaxSpeedX())

        """ IMPORTANT: NEED TO MOVE ALL COLLISION DETECTION TO SEPARATE FILES
            BEFORE IMPLEMENTING ANY NEW COLLIDABLE OBJECTS, OTHERWISE CODE
            WILL BECOME UNMANAGEABLE """

        # Move enemies horizontally with collision detection for platforms
        for enemy in enemies:
            enemy.moveX()
            if len(pygame.sprite.spritecollide(enemy, platforms, False)) > 0:
                while len(pygame.sprite.spritecollide(enemy, platforms, False)) > 0:
                    if enemy.getSpeedX() < 0:
                        enemy.rect.centerx += 1
                    elif enemy.getSpeedX() >= 0:
                        enemy.rect.centerx -= 1
                enemy.setSpeedX(-enemy.getSpeedX())

        # Move enemies vertically with collision detection for platforms
        for enemy in enemies:
            enemy.moveY(gravity)
            if len(pygame.sprite.spritecollide(enemy, platforms, False)) > 0:
                while len(pygame.sprite.spritecollide(enemy, platforms, False)) > 0:
                    if enemy.getSpeedY() < 0:
                        enemy.rect.centery += 1
                    elif enemy.getSpeedY() >= 0:
                        enemy.rect.centery -= 1
                enemy.setSpeedY(0)

        # Move player horizontally with collision detection for platforms
        player.moveX()
        if len(pygame.sprite.spritecollide(player, platforms, False)) > 0:
            while len(pygame.sprite.spritecollide(player, platforms, False)) > 0:
                if player.getSpeedX() < 0:
                    player.rect.centerx += 1
                elif player.getSpeedX() >= 0:
                    player.rect.centerx -= 1

        # Move player vertically with collision detection for platforms
        keys = pygame.key.get_pressed()
        jumpHeld = keys[K_SPACE] or keys[K_UP]
        player.moveY(gravity, jumpHeld)
        if len(pygame.sprite.spritecollide(player, platforms, False)) > 0:
            while len(pygame.sprite.spritecollide(player, platforms, False)) > 0:
                if player.getSpeedY() < 0:
                    player.rect.centery += 1
                elif player.getSpeedY() >= 0:
                    player.rect.centery -= 1
            if player.getSpeedY() > 0:
                player.setCanJump(True)
            player.setSpeedY(0)
        else:
            player.rect.centery += 1
            if len(pygame.sprite.spritecollide(player, platforms, False)) == 0:
                player.setCanJump(False)
            else:
                player.setCanJump(True)
            player.rect.centery -= 1

        camera.follow(player)
                
        gameWindow.fill((18, 188, 255))
        for sprite in sprites:
            gameWindow.blit(sprite.image, (sprite.rect.left - camera.getX(), sprite.rect.top - camera.getY()))
        #sprites.draw(gameWindow)
        
        clock.tick(60)
        
        pygame.display.flip()

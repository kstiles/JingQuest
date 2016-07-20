import pygame
from pygame.locals import *
from friendlybullet import FriendlyBullet

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super(Player, self).__init__(self.containers)

        # Load the player's image
        self.originalImage = pygame.image.load("./rsc/jing_32px.png")
        self.image = self.originalImage
        self.imageRect = self.image.get_rect()

        self.blankImage = pygame.Surface((32, 32))
        self.blankImage.set_colorkey((0, 0, 0))

        # Set the offset values for the image compared to the upper left corner
        # of the hitbox
        self.offset = (-4, -4)

        # Get the bounding rect of the image and set initial coordinates
        #self.rect = self.image.get_rect()
        self.rect = pygame.Rect(0, 0, 24, 26)
        self.rect.left = x - self.offset[0]
        self.rect.bottom = y + 32

        # Load the bullets image and split it into separate images in a list
        bulletSheet = pygame.image.load("./rsc/bullets_jing_rainbow.png")
        self.bulletImages = []
        for i in range(12):
            self.bulletImages.append(pygame.Surface((8, 8), pygame.SRCALPHA))
            self.bulletImages[i].blit(bulletSheet, (0, 0), (i * 8 + i, 0, 8, 8))

        # Set a counter for the current bullet color (12 colors)
        self.bulletColor = 0

        # Create player attributes
        self.speedX = 0
        self.maxSpeedX = 4
        self.speedY = 0
        self.maxSpeedY = 12
        self.canJump = False
        self.facingRight = True
        self.maxHealth = 3
        self.health = self.maxHealth
        
        self.stunFrames = 0
        self.iFrames = 0

        self.rotation = 0
        
    def moveX(self, platforms):

        # If not currently stunned after getting hit, move based on player input
        if self.stunFrames == 0:            
            keys = pygame.key.get_pressed()
            if keys[K_LEFT] and keys[K_RIGHT]:
                self.speedX = 0
            elif keys[K_LEFT]:
                self.speedX = -self.maxSpeedX
                self.facingRight = False
            elif keys[K_RIGHT]:
                self.speedX = self.maxSpeedX
                self.facingRight = True
            else:
                self.speedX = 0

        # If stunned, knock the player backwards, overriding their controls
        else:
            self.stunFrames -= 1
            if self.facingRight:
                self.speedX = -3
            else:
                self.speedX = 3

        # Move the player
        self.rect.centerx += self.speedX
        self.animate()
            
        # Check player collision with platforms
        if len(pygame.sprite.spritecollide(self, platforms, False)) > 0:
            while len(pygame.sprite.spritecollide(self, platforms, False)) > 0:
                if self.speedX < 0:
                    self.rect.centerx += 1
                elif self.speedX >= 0:
                    self.rect.centerx -= 1

    def moveY(self, platforms, gravity):

        # Move player vertically with collision detection for platforms
        keys = pygame.key.get_pressed()
        jumpHeld = keys[K_z] or keys[K_UP]
        
        gravityMultiplier = 1
        if not jumpHeld and self.speedY < 0 and self.stunFrames == 0:
            gravityMultiplier = 3
        self.speedY += gravity * gravityMultiplier
        if self.speedY > self.maxSpeedY:
            self.speedY = self.maxSpeedY
        self.rect.centery += self.speedY

        if len(pygame.sprite.spritecollide(self, platforms, False)) > 0:
            while len(pygame.sprite.spritecollide(self, platforms, False)) > 0:
                if self.speedY < 0:
                    self.rect.centery += 1
                elif self.speedY >= 0:
                    self.rect.centery -= 1
            if self.speedY > 0:
                self.canJump = True
            self.speedY = 0
        else:
            self.rect.centery += 1
            if len(pygame.sprite.spritecollide(self, platforms, False)) == 0:
                self.canJump = False
            else:
                self.canJump = True
            self.rect.centery -= 1

    def jump(self):

        if self.canJump and self.stunFrames == 0:
            self.canJump = False
            self.speedY = -self.maxSpeedY

    def shoot(self):

        # Only shoot if not currently stunned
        if self.stunFrames == 0:
            if self.facingRight:
                FriendlyBullet(self.rect.right, self.rect.centery, self.facingRight, self.bulletImages[self.bulletColor])
            else:
                FriendlyBullet(self.rect.left, self.rect.centery, self.facingRight, self.bulletImages[self.bulletColor])
        #self.bulletColor = (self.bulletColor + 1) % 12

    def checkEnemies(self, enemies):

        # Check if player is vulnerable
        if self.iFrames == 0:

            # Check for collisions with enemies
            if len(pygame.sprite.spritecollide(self, enemies, False)) > 0:
                self.health -= 1
                self.stunFrames = 15
                self.iFrames = 60
                """
                self.speedY -= 5
                if self.speedY < -self.maxSpeedY:
                    self.speedY = -self.maxSpeedY
                """
                self.speedY = -5

        else:

            self.iFrames -= 1
            if self.iFrames % 4 < 2:
                self.image = self.blankImage
            

    def animate(self):

        if self.stunFrames == 0:
            self.rotation -= self.speedX * (5.0 / 2.0)
       
        rotated = pygame.transform.rotate(self.originalImage, self.rotation)
        rect = rotated.get_rect()

        self.image = pygame.Surface((self.imageRect.width, self.imageRect.height), pygame.SRCALPHA)
        self.image.blit(rotated, (self.imageRect.width / 2 - rect.width / 2, self.imageRect.height / 2 - rect.height / 2))

        

        

    """===== Getter and setter functions below ====="""

    def getStunFrames(self):
        return self.stunFrames

    def getMaxSpeedX(self):
        return self.maxSpeedX

    def getMaxSpeedY(self):
        return self.maxSpeedY
        
    def setSpeedX(self, speed):
        self.speedX = speed

    def getSpeedX(self):
        return self.speedX

    def setSpeedY(self, speed):
        self.speedY = speed

    def getSpeedY(self):
        return self.speedY

    def setCanJump(self, jump):
        self.canJump = jump

    def getCanJump(self):
        return self.canJump

    def getRect(self):
        return self.rect

    def getOffset(self):
        return self.offset

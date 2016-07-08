import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):

    def __init__(self):

        super(Player, self).__init__(self.containers)

        # Load the player's image
        self.originalImage = pygame.image.load("./rsc/jing_32px.png")
        self.image = self.originalImage

        # Get the bounding rect of the image
        self.rect = self.image.get_rect()

        # Set the player's initial position
        self.rect.left = 40
        self.rect.top = 40

        # Create player attributes
        self.speedX = 0
        self.maxSpeedX = 4
        self.speedY = 0
        self.maxSpeedY = 12
        self.canJump = False

        self.rotation = 0
        
    def moveX(self, platforms):

        # Move player horizontally with collision detection for platforms
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and keys[K_RIGHT]:
            self.speedX = 0
        elif keys[K_LEFT]:
            self.speedX = -self.maxSpeedX
        elif keys[K_RIGHT]:
            self.speedX = self.maxSpeedX
        else:
            self.speedX = 0
        
        self.rect.centerx += self.speedX
        if self.speedX != 0:
            self.animate()

        if len(pygame.sprite.spritecollide(self, platforms, False)) > 0:
            while len(pygame.sprite.spritecollide(self, platforms, False)) > 0:
                if self.speedX < 0:
                    self.rect.centerx += 1
                elif self.speedX >= 0:
                    self.rect.centerx -= 1

    def moveY(self, platforms, gravity):

        # Move player vertically with collision detection for platforms
        keys = pygame.key.get_pressed()
        jumpHeld = keys[K_SPACE] or keys[K_UP]
        
        gravityMultiplier = 1
        if not jumpHeld and self.speedY < 0:
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

        if self.canJump:
            self.canJump = False
            self.speedY = -self.maxSpeedY

    def animate(self):

        if self.speedX > 0:
            self.rotation -= 10
        else:
            self.rotation += 10
        rotated = pygame.transform.rotate(self.originalImage, self.rotation)
        rect = rotated.get_rect()

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.image.blit(rotated, (self.rect.width / 2 - rect.width / 2, self.rect.height / 2 - rect.height / 2))

        

        

    """===== Getter and setter functions below ====="""

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

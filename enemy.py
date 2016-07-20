import pygame

class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super(Enemy, self).__init__(self.containers)

        # Load the enemy's images
        self.originalImage = pygame.image.load("./rsc/shrek_32px.png")
        self.hurtImage = pygame.image.load("./rsc/shrek_damage_32px.png")
        self.image = self.originalImage

        # Get the bounding rect of the image
        self.rect = self.image.get_rect()

        # Set the enemy's initial position
        self.rect.left = x
        self.rect.top = y

        # Create enemy attributes
        self.speedX = -1
        self.maxSpeedX = 1
        self.speedY = 0
        self.maxSpeedY = 12
        
        self.health = 2
        self.damageFrames = 0
        self.offset = (0, 0)

    def moveX(self, platforms):

        # Move enemy horizontally with collision detection for platforms
        self.rect.centerx += self.speedX
        if len(pygame.sprite.spritecollide(self, platforms, False)) > 0:
            while len(pygame.sprite.spritecollide(self, platforms, False)) > 0:
                if self.speedX < 0:
                    self.rect.centerx += 1
                elif self.speedX >= 0:
                    self.rect.centerx -= 1
            self.speedX = -self.speedX

    def moveY(self, platforms, gravity):

        # Move enemy vertically with collision detection for platforms
        self.speedY += gravity
        if self.speedY > self.maxSpeedY:
            self.speedY = self.maxSpeedY
        self.rect.centery += self.speedY

        if len(pygame.sprite.spritecollide(self, platforms, False)) > 0:
                while len(pygame.sprite.spritecollide(self, platforms, False)) > 0:
                    if self.speedY < 0:
                        self.rect.centery += 1
                    elif self.speedY >= 0:
                        self.rect.centery -= 1
                self.speedY = 0

    def takeDamage(self, amount):

        self.health -= amount
        if self.health <= 0:
            self.kill()
        else:
            self.image = self.hurtImage
            self.damageFrames = 7

    def updateImage(self):

        if self.damageFrames == 0:
            self.image = self.originalImage
        else:
            if self.damageFrames % 2 == 1:
                self.image = self.hurtImage
            else:
                self.image = self.originalImage
            self.damageFrames -= 1
            


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

    def getOffset(self):
        return self.offset

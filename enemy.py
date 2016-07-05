import pygame

class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super(Enemy, self).__init__(self.containers)

        # Load the enemy's image
        self.image = pygame.image.load("./rsc/shrek_32px.png")

        # Get the bounding rect of the image
        self.rect = self.image.get_rect()

        # Set the enemy's initial position
        self.rect.left = x
        self.rect.top = y

        # Create enemy attributes
        self.speedX = -2
        self.maxSpeedX = 2
        self.speedY = 0
        self.maxSpeedY = 12

    def moveX(self):

        self.rect.centerx += self.speedX

    def moveY(self, gravity):

        self.speedY += gravity
        if self.speedY > self.maxSpeedY:
            self.speedY = self.maxSpeedY
        self.rect.centery += self.speedY




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

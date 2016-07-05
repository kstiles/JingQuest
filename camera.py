import pygame

class Camera():

    def __init__(self, x, y, levelWidth, levelHeight):

        self.x = x
        self.y = y
        self.width = 640
        self.height = 360

        self.levelWidth = levelWidth
        self.levelHeight = levelHeight

        self.lockX = False
        self.lockY = True

        self.speedX = 0
        self.speedY = 0

    def follow(self, sprite):

        if not self.lockX:
            self.x = sprite.rect.centerx - (self.width / 2)
            if self.x < 0:
                self.x = 0
            elif self.x > self.levelWidth - self.width:
                self.x = self.levelWidth - self.width
        if not self.lockY:
            self.y = sprite.rect.centery - (self.height / 2)
            if self.y < 0:
                self.y = 0
            elif self.y > self.levelHeight - self.height:
                self.y = self.levelHeight - self.height

    def move(self):

        self.x += self.speedX
        self.y += self.speedY

    def lockX(self):

        self.lockX = True

    def unlockX(self):

        self.lockX = False

    def lockY(self):

        self.lockY = True

    def unlockY(self):

        self.lockY = False

    def getX(self):

        return self.x

    def setX(self, x):

        self.x = x

    def getY(self):

        return self.y

    def setY(self, y):

        self.y = y

    def setSpeedX(self, x):
        self.speedX = x
    def getSpeedX(self):
        return self.speedX
    def setSpeedY(self, y):
        self.speedY = y
    def getSpeedY(self):
        return self.speedY

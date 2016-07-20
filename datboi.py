import pygame

class DatBoi(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super(DatBoi, self).__init__(self.containers)

        # Load the enemy's images
        self.imageReel = []
        for i in range(5):
            self.imageReel.append(pygame.image.load("./rsc/datboi_32px_" + str(i) + ".png"))

        self.frame = 0
        self.frameDelay = 0
        self.image = self.imageReel[self.frame]

        # Get the bounding rect of the image
        self.offset = (-8, -5)
        self.rect = pygame.Rect(0, 0, 20, 46)

        # Set the enemy's initial position
        self.rect.centerx = x + 16
        self.rect.bottom = y + 64

        # Create enemy attributes
        self.speedX = -2
        self.maxSpeedX = 2
        self.speedY = 0
        self.maxSpeedY = 12
        
        self.health = 4
        self.damageFrames = 0

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

        # Prevent dat boi from moving off of platforms on his own
        else:
            self.rect.centery += 1
            collided = pygame.sprite.spritecollide(self, platforms, False)
            if len(collided) == 1:
                if self.rect.left < collided[0].rect.left:
                    self.rect.left = collided[0].rect.left
                    if self.speedX < 0:
                        self.speedX = -self.speedX
                elif self.rect.right > collided[0].rect.right:
                    self.rect.right = collided[0].rect.right
                    if self.speedX > 0:
                        self.speedX = -self.speedX
            self.rect.centery -= 1

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

    def updateImage(self):

        self.image = self.imageReel[self.frame]
        self.frameDelay = (self.frameDelay + 1) % 4
        if self.frameDelay == 0:
            self.frame = (self.frame + 1) % 5
        if self.speedX < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            


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

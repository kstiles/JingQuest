import pygame

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
        
    def moveX(self):

        self.rect.centerx += self.speedX
        if self.speedX != 0:
            self.animate()

    def moveY(self, gravity, jumpHeld):

        gravityMultiplier = 1
        if not jumpHeld and self.speedY < 0:
            gravityMultiplier = 3
        self.speedY += gravity * gravityMultiplier
        if self.speedY > self.maxSpeedY:
            self.speedY = self.maxSpeedY
        self.rect.centery += self.speedY

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

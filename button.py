import pygame

class Button(pygame.sprite.Sprite):

    def __init__(self, name, x, y, **kwargs):

        # **kwargs contains all possible images for the button
        # recognized keys are as follows:
        # default -> default image for button, used to determine rect size
        # hover -> alternate image for mouse hovering over button
        # selected -> alternate image for when button is clicked/selected

        super(Button, self).__init__(self.containers)

        self.allImages = kwargs

        self.image = kwargs["default"]
        
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = x, y

        self.name = name
        self.state = "default"

    def checkClickOnButton(self, mouse):

        if (self.rect.left <= mouse[0] <= self.rect.right and
            self.rect.top <= mouse[1] <= self.rect.bottom):
            try:
                self.image = self.allImages["selected"]
                self.state = "selected"
            except:
                pass
            return True
        return False

    def getName(self):

        return self.name

    def setState(self, state):

        self.state = state
        try:
            self.image = self.allImages[self.state]
        except:
            pass

    def getState(self):

        return self.state

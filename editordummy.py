import pygame

class Dummy(pygame.sprite.Sprite):

    def __init__(self, line):

        super(Dummy, self).__init__(self.containers)

        self.type = line[0]

        if self.type == "platform":

            w, h = int(line[3]), int(line[4])
            
            # Create the Surface for the platform image
            self.image = pygame.Surface((w, h))
            self.image.fill((247, 145, 35))

            # Draw an outline
            pygame.draw.line(self.image, (0, 0, 0), (0, 0), (w, 0), 2)
            pygame.draw.line(self.image, (0, 0, 0), (0, 0), (0, h), 2)
            pygame.draw.line(self.image, (0, 0, 0), (0, h - 2), (w, h - 2), 2)
            pygame.draw.line(self.image, (0, 0, 0), (w - 2, 0), (w - 2, h), 2)

        elif self.type == "enemy":
            self.image = pygame.image.load("./rsc/shrek_32px.png")
        elif self.type == "player":
            self.image = pygame.image.load("./rsc/jing.png")

        self.rect = self.image.get_rect()
        self.rect.left = int(line[1])
        self.rect.top = int(line[2])

    def getType(self):

        return self.type

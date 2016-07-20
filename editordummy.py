import pygame

class Dummy(pygame.sprite.Sprite):

    def __init__(self, line):

        super(Dummy, self).__init__(self.containers)

        self.offset = (0, 0)

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

            self.rect = self.image.get_rect()
            self.rect.left = int(line[1])
            self.rect.top = int(line[2])

        elif self.type == "enemy":
            self.image = pygame.image.load("./rsc/shrek_32px.png")
            self.rect = pygame.Rect(int(line[1]), int(line[2]), 32, 32)
            self.offset = (0, 0)
        elif self.type == "player":
            self.image = pygame.image.load("./rsc/jing_32px.png")
            self.rect = pygame.Rect(int(line[1]), int(line[2]), 32, 32)
            self.offset = (0, 0)
        elif self.type == "datboi":
            self.image = pygame.image.load("./rsc/datboi_32px_0.png")
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = pygame.Rect(int(line[1]), int(line[2]), 32, 64)
            self.offset = (1, 13)

    def getType(self):

        return self.type

    def getDataString(self):

        if self.type == "platform":
            return self.type + " " + str(self.rect.left) + " " + str(self.rect.top) + " " + str(self.rect.width) + " " + str(self.rect.height) + "\n"
        elif self.type == "enemy":
            return self.type + " " + str(self.rect.left) + " " + str(self.rect.top) + "\n"
        elif self.type == "player":
            return self.type + " " + str(self.rect.left) + " " + str(self.rect.top) + "\n"
        elif self.type == "datboi":
            return self.type + " " + str(self.rect.left) + " " + str(self.rect.top) + "\n"

    def getOffset(self):

        return self.offset


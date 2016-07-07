import pygame

class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h):

        super(Platform, self).__init__(self.containers)

        # Create the Surface for the platform image
        self.image = pygame.Surface((w, h))
        self.image.fill((247, 145, 35))

        # Draw an outline
        pygame.draw.line(self.image, (0, 0, 0), (0, 0), (w, 0), 1)
        pygame.draw.line(self.image, (0, 0, 0), (0, 0), (0, h), 1)
        pygame.draw.line(self.image, (0, 0, 0), (0, h - 2), (w, h - 2), 2)
        pygame.draw.line(self.image, (0, 0, 0), (w - 2, 0), (w - 2, h), 2)

        # Get the bounding rect of the image
        self.rect = self.image.get_rect()

        # Set the platform's position
        self.rect.left = x
        self.rect.top = y

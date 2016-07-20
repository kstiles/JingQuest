import pygame

class FriendlyBullet(pygame.sprite.Sprite):

    def __init__(self, x, y, toRight, image):

        super(FriendlyBullet, self).__init__(self.containers)

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        if toRight:
            self.speed = 7
        else:
            self.speed = -7

        self.offset = (0, 0)

        self.time = 30
        self.damage = 1

    def move(self, enemies, platforms):

        # Check to see if the bullet should still be alive
        self.time -= 1
        if self.time >= 0:

            # Move the bullet
            self.rect.centerx += self.speed

            # Check for collisions with enemies
            hitEnemies = pygame.sprite.spritecollide(self, enemies, False)
            if len(hitEnemies) > 0:
                
                # When bullet is moving right, hit the leftmost enemy
                if self.speed > 0:
                    target = hitEnemies[0]
                    for i in range(len(hitEnemies)):
                        if hitEnemies[i].rect.left < target.rect.left:
                            target = hitEnemies[i]
                            
                # When bullet is moving left, hit the rightmost enemy
                elif self.speed < 0:
                    target = hitEnemies[0]
                    for i in range(len(hitEnemies)):
                        if hitEnemies[i].rect.right > target.rect.right:
                            target = hitEnemies[i]

                # Damage the enemy that was hit first and destroy the bullet
                target.takeDamage(self.damage)
                self.kill()

            # Check for collisions with platforms; prioritize hitting enemies
            # over platforms
            elif len(pygame.sprite.spritecollide(self, platforms, False)) > 0:
                self.kill()
        else:
            self.kill()

    def getOffset(self):

        return self.offset

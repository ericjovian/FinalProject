import pygame
from time import sleep
win = pygame.display.set_mode((1200, 700))


class Block(pygame.sprite.Sprite):
    """ This class represents the block. """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("Zombflip.png")
        self.image = pygame.transform.scale(self.image, (90, 120))

        self.rect = self.image.get_rect()

    def follow(self, x, y):
        if self.rect.x < x:
            self.rect.x += 1
        if self.rect.y < y:
            self.rect.y += 1
        if self.rect.x > x:
            self.rect.x -= 1
        if self.rect.y > y:
            self.rect.y -= 1

    def stop(self, x, y):
        green = (0, 220, 0)
        bright_green = (0, 225, 0)
        if self.rect.x == x and self.rect.y == y:
            sleep(0.5)
            die = pygame.image.load("gameover.jpg")
            die = pygame.transform.scale(die, (1200, 700))
            win.blit(die, [0, 0])


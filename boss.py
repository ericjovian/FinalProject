import pygame
from time import sleep


class Boss(pygame.sprite.Sprite):
    """ This class represents the block. """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("boss.png")
        self.image = pygame.transform.scale(self.image, (120, 150))

        self.rect = self.image.get_rect()

    def follow(self, x, y):
        if self.rect.x < x:
            self.rect.x += 5
        if self.rect.y < y:
            self.rect.y += 5
        if self.rect.x > x:
            self.rect.x -= 5
        if self.rect.y > y:
            self.rect.y -= 5

    def stop(self, x, y):
        if self.rect.x == x and self.rect.y == y:
            sleep(0.5)
            win = pygame.display.set_mode((1200, 700))
            die = pygame.image.load("gameover.jpg")
            die = pygame.transform.scale(die, (1200, 700))
            win.blit(die, [0, 0])

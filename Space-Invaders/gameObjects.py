import pygame

class playerShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("gfx\klingon.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 270
        self.speedx = 2
        self.speedy = 2
    height = 50
    width = 50
    
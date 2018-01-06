import pygame
import random
from main import windowWidth, windowHeight, explosionAnim1


class playerShip(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.exist = True
        self.image = pygame.image.load("gfx\klingon.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 270

    def move(self):
        pass

    speedx = 2
    speedy = 2


class enemyShipDumb(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.exist = True
        self.image = pygame.image.load("gfx\enemyShipDumb.png")
        self.rect = self.image.get_rect()
        self.rect.x = windowWidth - self.rect.width
        self.rect.y = random.randint(1, (windowHeight - self.rect.height))
        self.posx = self.rect.x
        self.posy = self.rect.y
        self.speedy = 0.3
        self.speedy *= random.randint(-2, 2)

    def move(self):
        if (self.posx + self.speedx) < 0 or (self.posx + self.speedx) > (windowWidth - self.rect.width):
            self.exist = False
        else:
            self.posx += self.speedx
        if (self.posy + self.speedy) < 0 or (self.posy + self.speedy) > (windowHeight - self.rect.height):
            self.speedy *= -1
        else:
            self.posy += self.speedy
        self.rect.x = int(self.posx)
        self.rect.y = int(self.posy)

    speedx = -2


class playerShotSimple(pygame.sprite.Sprite):

    def __init__(self, plShiprect):
        super().__init__()
        self.exist = True
        self.image = pygame.image.load("gfx\playerShotSimple.png")
        self.rect = self.image.get_rect()
        self.rect.x = plShiprect.x + plShiprect.width + 10
        self.rect.y = plShiprect.y + (plShiprect.height / 2)
        self.posx = self.rect.x
        self.posy = self.rect.y
        self.speedx = 5

    def move(self):
        if (self.posx + self.speedx) < 0 or (self.posx + self.speedx) > (windowWidth - self.rect.width):
            self.exist = False
        else:
            self.posx += self.speedx
        self.rect.x = int(self.posx)


class explosion1(pygame.sprite.Sprite):

    def __init__(self, enemyShiprect):
        super().__init__()
        self.exist = True
        self.image = explosionAnim1[0]
        self.rect = self.image.get_rect()
        self.rect.x = (enemyShiprect.x + (enemyShiprect.width / 2)) - (self.rect.width / 2)
        self.rect.y = (enemyShiprect.y + (enemyShiprect.height / 2)) - (self.rect.height / 2)
        self.posx = self.rect.x
        self.posy = self.rect.y
        self.speedx = -1
        self.animSpeed = 0.5
        self.animFrame = -1

    def move(self):
        if (self.posx + self.speedx) < 0 or (self.posx + self.speedx) > (windowWidth - self.rect.width) or (self.animFrame > 11):
            self.exist = False
        else:
            self.posx += self.speedx
            self.animFrame += self.animSpeed
            self.image = explosionAnim1[int(self.animFrame)]
        self.rect.x = int(self.posx)

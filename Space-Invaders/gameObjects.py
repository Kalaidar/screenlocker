import pygame
from pygame.locals import *
import random
from math import fabs, floor

windowWidth = 1200
windowHeight = 600
explosionAnim1 = []
bonusAnim1 = []
black = (0, 0, 0)
grey = (240, 240, 240)
plShipSpriteGroup = pygame.sprite.Group()
enemyShotsSpriteGroup = pygame.sprite.Group()
plShotsSpriteGroup = pygame.sprite.Group()
explosionsSpriteGroup = pygame.sprite.Group()
enemyShipsSpritesGroup = pygame.sprite.Group()
bonusSpriteGroup = pygame.sprite.Group()
pygame.mixer.init()
plasmaSound = pygame.mixer.Sound('snd\plasmaShot1.ogg')
machineGunSound = pygame.mixer.Sound('snd\machineGun1.ogg')
missileSound = pygame.mixer.Sound('snd\missile1.ogg')


class playerShip(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.exist = True
        self.image = pygame.image.load("gfx\klingon.png")
        self.machinegunImage = pygame.image.load("gfx\machinegun.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 270
        self.invul = 0
        self.xMoveBorder = 600
        self.speedx = 2
        self.speedy = 2
        self.bonus = ''

    def activateBonus(self, bon):
        self.bonus = bon
        if bon == 'machinegun':
            plShipSpriteGroup.add(playerShipPart('gfx\machinegun.png', self.rect, 'top'))
            plShipSpriteGroup.add(playerShipPart('gfx\machinegun.png', self.rect, 'bottom'))

    def move(self, keys):
        if keys[K_UP]:
            if (self.rect.y - self.speedy) < 0:
                self.rect.y = 0
            else:
                self.rect.y -= self.speedy
        if keys[K_DOWN]:
            if (self.rect.y + self.speedy) > (windowHeight - self.rect.height):
                self.rect.y = windowHeight - self.rect.height
            else:
                self.rect.y += self.speedy
        if keys[K_RIGHT]:
            if (self.rect.x + self.speedx) > self.xMoveBorder:
                self.rect.x = self.xMoveBorder
            else:
                self.rect.x += self.speedx
        if keys[K_LEFT]:
            if (self.rect.x - self.speedx) < 0:
                self.rect.x = 0
            else:
                self.rect.x -= self.speedx
        if self.invul > 0:
            if self.invul & 4 != 0:
                self.image = pygame.Surface((self.rect.width, self.rect.height))
            else:
                self.image = pygame.image.load("gfx\klingon.png")
            self.invul -= 1

class playerShipPart(pygame.sprite.Sprite):

    def __init__(self, bitmap, plShipRect, side):
        super().__init__()
        self.image = pygame.image.load(bitmap)
        self.rect = self.image.get_rect()
        self.rect.x = plShipRect.x
        if side == 'top':
            self.rect.y = plShipRect.y - self.rect.height
        elif side == 'bottom':
            self.rect.y = plShipRect.y + plShipRect.height
        self.side = side
            
    def move(self, plShipRect):
        self.rect.x = plShipRect.x
        if self.side == 'top':
            self.rect.y = plShipRect.y - self.rect.height
        elif self.side == 'bottom':
            self.rect.y = plShipRect.y + plShipRect.height

class enemyShipDumb(pygame.sprite.Sprite):

    def __init__(self, sign):
        super().__init__()
        self.exist = True
        self.image = pygame.image.load("gfx\enemyShipDumb.png")
        self.rect = self.image.get_rect()
        self.rect.x = windowWidth - self.rect.width
        self.rect.y = random.randint(1, (windowHeight - self.rect.height))
        self.posx = self.rect.x
        self.posy = self.rect.y
        self.speedx = -2
        self.speedy = 0.3
        self.speedy *= sign * 2
        self.score = 200

    def move(self, *unused):
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


class enemyShipRocket(pygame.sprite.Sprite):

    def __init__(self, sign):
        super().__init__()
        self.exist = True
        self.image = pygame.image.load("gfx\enemyShipRocket.png")
        self.rect = self.image.get_rect()
        self.rect.x = windowWidth - self.rect.width
        self.rect.y = random.randint(1, (windowHeight - self.rect.height))
        self.posx = self.rect.x
        self.posy = self.rect.y
        self.speedx = 0
        self.speedy = 0
        self.score = 300
        self.moveTimer = 0
        self.sign = sign
        self.movePattern = [ 'speeds',  # type
           - 0.5,  # x axis speed
           1,  # y axis speed
           150,  # ticks timer
           'toPlayer',
           0
           ]

    def move(self, plShipRect):
        
        if self.moveTimer == 0 and self.movePattern != []:
            moveType = self.movePattern.pop(0)
            if moveType == 'speeds':
                self.speedx = self.movePattern.pop(0)
                self.speedy = self.movePattern.pop(0)
                self.speedy *= self.sign
                self.moveTimer = self.movePattern.pop(0)
            if moveType == 'toPlayer':
                missileSound.play()
                self.speedx = -7
                self.speedy = (self.rect.y - plShipRect.y) / ((self.rect.x - plShipRect.x) / self.speedx)
                self.moveTimer = self.movePattern.pop(0)
        else:
            self.moveTimer -= 1
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

    
class enemyShipShooter1(pygame.sprite.Sprite):

    def __init__(self, sign):
        super().__init__()
        self.exist = True
        self.image = pygame.image.load("gfx\enemyShipShooter1.png")
        self.rect = self.image.get_rect()
        self.rect.x = windowWidth - self.rect.width
        self.rect.y = random.randint(1, (windowHeight - self.rect.height))
        self.posx = self.rect.x
        self.posy = self.rect.y
        self.speedx = -2
        self.speedy = 2
        self.speedy *= sign
        self.score = 200
        self.shotInterval = 0

    def move(self, plShipRect):
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
        if self.shotInterval > 0:
            self.shotInterval -= 1
        if fabs((self.rect.y + self.rect.height * 2) - (plShipRect.y + plShipRect.height * 2)) < random.randint(1, 35) and self.shotInterval == 0:
            enemyShotsSpriteGroup.add(enemyShotSimple(self.rect, "gfx\enemyShot1.png", -5))
            plasmaSound.play()
            self.shotInterval = 200


class enemyShipShooter2(pygame.sprite.Sprite):

    def __init__(self, sign):
        super().__init__()
        self.exist = True
        self.image = pygame.image.load("gfx\enemyShipShooter2.png")
        self.rect = self.image.get_rect()
        self.rect.x = windowWidth - self.rect.width
        self.rect.y = random.randint(1, (windowHeight - self.rect.height))
        self.posx = self.rect.x
        self.posy = self.rect.y
        self.speedx = -2
        self.speedy = 2
        self.speedy *= sign
        self.score = 300
        self.shotInterval = 0
        self.moveTimer = 0
        self.sign = sign
        self.moveType = ''
        self.movePattern = [
            'speeds',
            -0.5,
            1,
            100,
            'targetPlayer',
            'speeds',  # type
           - 0.5,  # x axis speed
           1,  # y axis speed
           150,  # ticks timer
           'targetPlayer',
           'speeds',
           -3,
           0.5,
           500
           ]

    def move(self, plShipRect):
        
        if self.moveTimer == 0 and self.movePattern != []:
            self.moveType = self.movePattern.pop(0)
            if self.moveType == 'speeds':
                self.speedx = self.movePattern.pop(0)
                self.speedy = self.movePattern.pop(0)
                self.speedy *= self.sign
                self.moveTimer = self.movePattern.pop(0)
            if self.moveType == 'targetPlayer':
                self.speedx = -1
                if self.rect.y > plShipRect.y:
                    self.speedy = -3
                else:
                    self.speedy = 3
                self.moveTimer = floor(fabs(self.rect.y - plShipRect.y) / fabs(self.speedy))
        else:
            self.moveTimer -= 1
            if self.moveTimer < 10 and self.moveTimer & 3 == 0 and self.moveType == 'targetPlayer':
                enemyShotsSpriteGroup.add(enemyShotSimple(self.rect, 'gfx\enemyShot2.png', -15))
            if self.moveTimer == 10 and self.moveType == 'targetPlayer':
                machineGunSound.play()

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


class enemyShipFireball(pygame.sprite.Sprite):

    def __init__(self, sign):
        super().__init__()
        self.exist = True
        self.image = pygame.image.load("gfx\enemyFireball.png")
        self.rect = self.image.get_rect()
        self.rect.x = windowWidth - self.rect.width
        self.rect.y = random.randint(1, (windowHeight - self.rect.height))
        self.posx = self.rect.x
        self.posy = self.rect.y
        self.speedx = 0
        self.speedy = 0
        self.score = 300
        self.sign = sign
        self.moveTimer = 0
        self.homingTimer = 0
        self.moveType = ''
        self.movePattern = [ 'speeds',  # type
           - 0.5,  # x axis speed
           1,  # y axis speed
           150,  # ticks timer
           'speeds',
           -5,
           1,
           210,
           'homing'
           ]

    def move(self, plShipRect):
        
        if self.moveTimer == 0 and self.movePattern != []:
            self.moveType = self.movePattern.pop(0)
            if self.moveType == 'speeds':
                self.speedx = self.movePattern.pop(0)
                self.speedy = self.movePattern.pop(0)
                self.speedy *= self.sign
                self.moveTimer = self.movePattern.pop(0)
        else:
            self.moveTimer -= 1
        if self.moveType == 'homing':
            if self.homingTimer == 0:
                if (self.rect.centerx - plShipRect.centerx) > 20:
                    self.speedx = -2
                elif (self.rect.centerx - plShipRect.centerx) < -20:
                    self.speedx = 2
                else:
                    self.speedx = 0
                if (self.rect.centery - plShipRect.centery) > 20:
                    self.speedy = -2
                elif (self.rect.centery - plShipRect.centery) < -20:
                    self.speedy = 2
                else:
                    self.speedy = 0
                self.homingTimer = 30
            else:
                self.homingTimer -= 1

        if (self.posx + self.speedx) < -200 or (self.posx + self.speedx) > (windowWidth - self.rect.width):
            self.exist = False
        else:
            self.posx += self.speedx
        if (self.posy + self.speedy) < -20 or (self.posy + self.speedy) > (windowHeight - self.rect.height):
            self.speedy *= -1
        else:
            self.posy += self.speedy
        self.rect.x = int(self.posx)
        self.rect.y = int(self.posy)

class playerShotSimple(pygame.sprite.Sprite):

    def __init__(self, plShipRect, spritePath):
        super().__init__()
        self.exist = True
        self.image = pygame.image.load(spritePath)
        self.rect = self.image.get_rect()
        self.rect.x = plShipRect.x + plShipRect.width + 10
        self.rect.y = plShipRect.y + (plShipRect.height / 2)
        self.posx = self.rect.x
        self.posy = self.rect.y
        self.speedx = 5

    def move(self):
        if (self.posx + self.speedx) < 0 or (self.posx + self.speedx) > (windowWidth - self.rect.width):
            self.exist = False
        else:
            self.posx += self.speedx
        self.rect.x = int(self.posx)


class enemyShotSimple(pygame.sprite.Sprite):

    def __init__(self, shipRect, spritePath, speedx):
        super().__init__()
        self.exist = True
        self.image = pygame.image.load(spritePath)
        self.rect = self.image.get_rect()
        self.rect.x = shipRect.x - shipRect.width - 10
        self.rect.y = shipRect.y + (shipRect.height / 2)
        self.posx = self.rect.x
        self.posy = self.rect.y
        self.speedx = speedx

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
        if self.animFrame > 11:
            self.exist = False
        else:
            self.posx += self.speedx
            self.animFrame += self.animSpeed
            self.image = explosionAnim1[int(self.animFrame)]
            self.rect.x = int(self.posx)

class bonus1(pygame.sprite.Sprite):

    def __init__(self, wreckRect, bonus):
        super().__init__()
        self.exist = True
        self.image = bonusAnim1[0]
        self.rect = self.image.get_rect()
        self.rect.x = wreckRect.x
        self.rect.y = wreckRect.y
        self.posx = self.rect.x
        self.posy = self.rect.y
        self.speedx = -2
        self.animSpeed = 0.2
        self.animFrame = 0
        self.bonus = bonus

    def move(self):
        if self.animFrame > 6 or self.animFrame < 0:
            self.animSpeed *= -1
        if (self.posx + self.speedx) < 0 or (self.posx + self.speedx) > (windowWidth - self.rect.width):
            self.exist = False
        else:
            self.posx += self.speedx
            self.animFrame += self.animSpeed
            self.image = bonusAnim1[int(self.animFrame)]
            self.rect.x = int(self.posx)

level1 = [
#         enemyShipDumb,  # ships type
#         5,  # ships number
#         1,  # random seed of ships number
#         10,  # random seed of appear time
         enemyShipShooter1, 2, 0, 1, 'bonus', 'machineguns', 'next',
         enemyShipRocket, 2, 0, 1,
         enemyShipShooter2, 1, 0, 1,
         enemyShipDumb, 5, 1, 20, 'next',
         enemyShipFireball, 2, 0, 1
         ]

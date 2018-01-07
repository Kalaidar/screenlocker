# -*- coding: cp1251 -*-

from pip._vendor.pyparsing import empty
global windowWidth
global windowHeight
windowWidth = 1200
windowHeight = 600
explosionAnim1 = []

import pygame
from pygame.locals import *
import tkinter as tk
from time import clock
from gameObjects import *
import spacelib
import os


def makeRoot():
    global root
    root = tk.Tk()
    root.title('SPACE INVADERS')
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(windowWidth, windowHeight))
    
def mainMenu():

    def startGame(event):
        rootFrame.pack_forget()
        rootFrame.destroy()
        root.update()
        os.environ['SDL_WINDOWID'] = str(root.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.init()
        global gameScreen
        gameScreen = pygame.display.set_mode((1200, 600))
        gameScreen.fill(black)
        playGame()
        root.quit()

    def highScores(event):
        exit()

    def quitGame(event):
        exit()

    def onHover(event):
        event.widget.config(bg="saddle brown")

    def offHover(event):
        event.widget.config(bg="black")

    rootFrame = tk.Frame(root)
    rootFrame.tk_setPalette(background="black", foreground="ghost white")
    header = tk.Label(rootFrame, text="SPACE INVADERS", anchor="w", fg="seashell2", font=("invasion2000", 80))
    startGameButton = tk.Button(rootFrame, text="START GAME", bd=0)
    highScoresButton = tk.Button(rootFrame, text="HIGH SCORES", bd=0)
    quitButton = tk.Button(rootFrame, text="QUIT GAME", bd=0)
    startGameButton.bind("<Enter>", onHover)
    startGameButton.bind("<Leave>", offHover)
    startGameButton.bind("<Button-1>", startGame)
    highScoresButton.bind("<Enter>", onHover)
    highScoresButton.bind("<Leave>", offHover)
    quitButton.bind("<Enter>", onHover)
    quitButton.bind("<Leave>", offHover)
    quitButton.bind("<Button-1>", quitGame)
    rootFrame.pack(expand=1, fill="both")
    header.pack(side="top")
    startGameButton.pack(pady=(100, 0))
    highScoresButton.pack()
    quitButton.pack()

def gameOver():
    pygame.quit()
    mainMenu()

def starSkyInit():

    def makeNewStar():
        star = {}
        star['x'] = random.randint(1, (windowWidth - 1))
        star['y'] = random.randint(1, (windowHeight - 1))
        star['speed'] = random.randint(1, 5)
        return star
    
    global stars   
    stars = []
    for _ in range(50):
        stars.append(makeNewStar())


def starSky():
    for s in stars:
        s['x'] -= s['speed']
        if s['x'] < 1:
            s['x'] = windowWidth - 1
            s['y'] = random.randint(1, (windowHeight - 1))
            s['speed'] = random.randint(1, 3)
        gameScreen.set_at((s['x'], s['y']), grey)

def playGame():

    plShipSpriteGroup = pygame.sprite.Group()
    plShip = playerShip()
    plShipSpriteGroup.add(plShip)
    plShotInterval = 50
    plShotTimeout = 0
    plShotsSpriteGroup = pygame.sprite.Group()
    explosionsSpriteGroup = pygame.sprite.Group()
    
    life = pygame.image.load('gfx\heart.png')
    score = 0
    lives = 3
    gameOverTimer = 0
    
    enemyDumbShipsCount = 5
    enemyShipsSpritesGroup = pygame.sprite.Group()

    for i in range(1, 14):
        filename = 'gfx\expl1\expl1{}.png'.format(i)
        img = pygame.image.load(filename)
        explosionAnim1.append(img)

    laserSound1 = pygame.mixer.Sound('snd\laser1.ogg')
    metalSound1 = pygame.mixer.Sound('snd\metal-bang.ogg')
    explosionSounds = []
    explosionSoundsNum = -1
    for i in range(1, 5):
        filename = 'snd\explosion{}.ogg'.format(i)
        snd = pygame.mixer.Sound(filename)
        explosionSounds.append(snd)
        explosionSoundsNum += 1
    pygame.mixer.music.load('snd\cavalry.mp3')
    pygame.mixer.music.play()
    
    carryOn = True
    
    '''
    поехал основной цикл экшна
    '''
    while carryOn:
    
# проверяем закрытие окна
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False

# проверяем нажатия клавиш и шевелим кораблем игрока
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            carryOn = False
# вся последующая часть - если корабль игрока существует   
        if plShip.exist == True:         
            plShip.move(keys)

# считаем таймаут выстрела
            if plShotTimeout > 0:
                plShotTimeout -= 1

# стреляем
            if keys[K_SPACE]:
                if plShotTimeout == 0:
                    laserSound1.play()
                    plShotsSpriteGroup.add(playerShotSimple(plShip.rect))
                    plShotTimeout = plShotInterval

# добавляем вражеские корабли
            if len(enemyShipsSpritesGroup) < enemyDumbShipsCount:
                if random.randint(1, 50) == 1:
                    enemyShipsSpritesGroup.add(enemyShipDumb())

# проверяем столкновения
            for ship in enemyShipsSpritesGroup:
                if plShip.invul == 0:
                    if ship.rect.colliderect(plShip.rect):
                        ship.exist = False
                        lives -= 1
                        plShip.invul = 250
                        ship.exist = False
                        metalSound1.play()
                        explosionsSpriteGroup.add(explosion1(ship.rect))
                        if lives == 0:
                            plShip.exist = 0
                            explosionsSpriteGroup.add(explosion1(plShip.rect))
                            plShipSpriteGroup.remove(plShip)
        
            for shot in plShotsSpriteGroup:
                for ship in enemyShipsSpritesGroup:
                    if shot.rect.colliderect(ship.rect):
                        shot.exist = False
                        ship.exist = False
                        explosionSounds[random.randint(0,explosionSoundsNum)].play()
                        explosionsSpriteGroup.add(explosion1(ship.rect))
                        score += 100

# двигаем все спрайты и удаляем отработавшие
        for sprite in enemyShipsSpritesGroup:
            if sprite.exist == True:
                sprite.move()
            else:
                enemyShipsSpritesGroup.remove(sprite)
        for sprite in plShotsSpriteGroup:
            if sprite.exist == True:
                sprite.move()
            else:
                plShotsSpriteGroup.remove(sprite)
        for sprite in explosionsSpriteGroup:
            if sprite.exist == True:
                sprite.move()
            else:
                explosionsSpriteGroup.remove(sprite)


# рисуем всё
        gameScreen.fill(black)
        starSky()
        plShipSpriteGroup.draw(gameScreen)
        enemyShipsSpritesGroup.draw(gameScreen)
        plShotsSpriteGroup.draw(gameScreen)
        explosionsSpriteGroup.draw(gameScreen)
        
        scoreText = regularFont.render(str(score), 1, grey)
        gameScreen.blit(scoreText, (1000, 6))
        
        for x in range(lives):
            gameScreen.blit(life, ((x*10+800), 3))
        
        if plShip.exist == False:
            gameOverTimer += 1
            if gameOverTimer > 100:
                gameOverText = largeFont.render("GAME OVER", 1, grey)
                gameScreen.blit(gameOverText, (windowWidth / 2 - gameOverText.get_width() / 2, windowHeight / 2 - gameOverText.get_height() / 2))
            if gameOverTimer == 100:
                pygame.mixer.music.load('snd\gamover.mp3')
                pygame.mixer.music.play()
            if gameOverTimer > 500:
                pygame.quit()
                mainMenu()
                
        pygame.display.update()
        clock.tick(100)

    
if __name__ == "__main__":

    black = (0, 0, 0)
    grey = (240, 240, 240)
    starSkyInit()
    clock = pygame.time.Clock()
    pygame.font.init()
    regularFont = pygame.font.Font('gfx\invasion2000.ttf', 24)
    largeFont = pygame.font.Font('gfx\invasion2000.ttf', 100)
    spacelib.loadfont(bytes('gfx\invasion2000.ttf', encoding='utf-8'))
    makeRoot()
    root.option_add("*font", "invasion2000 24")
    mainMenu()
    root.mainloop()
    

# -*- coding: cp1251 -*-

# imported variables


import pygame
from pygame.locals import *
import tkinter as tk
from spacelib import *
import os
from gameObjects import *

testMode = 1

    
def mainMenu():

    def startGame(event):
        rootFrame.pack_forget()
        rootFrame.destroy()
        root.update()
        os.environ['SDL_WINDOWID'] = str(root.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
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


def playGame():
    
    lives = 3
    plShotInterval = 50
    invulTime = 250
    enemyShipGroupInterval = 200
    signRandomizerTemplate = [1, -1]
    signRandomizer = list(signRandomizerTemplate)
    level = list(level1)

    enemyShipGroupTimer = enemyShipGroupInterval
    enemyShipCount = 0
    pygame.init()
    gameScreen = pygame.display.set_mode((1200, 600))
    gameScreen.fill(black)
    
    plShip = playerShip()
    plShipSpriteGroup.add(plShip)
    plShotTimeout = 0
    
    life = pygame.image.load('gfx\heart.png')
    score = 0
    gameOverTimer = 0
    bonus = ''

    for i in range(1, 14):
        filename = 'gfx\expl1\expl1{}.png'.format(i)
        img = pygame.image.load(filename)
        explosionAnim1.append(img)

    for i in range(1, 8):
        filename = 'gfx\\bonus1\\bonus1{}.png'.format(i)
        img = pygame.image.load(filename)
        bonusAnim1.append(img)


    laserSound1 = pygame.mixer.Sound('snd\laser1.ogg')
    metalSound1 = pygame.mixer.Sound('snd\metalBang1.ogg')
    metalSound2 = pygame.mixer.Sound('snd\metalBang2.ogg')
    dingSound1 = pygame.mixer.Sound('snd\ding.ogg')
    explosionSounds = []
    explosionSoundsNum = -1
    for i in range(1, 5):
        filename = 'snd\explosion{}.ogg'.format(i)
        snd = pygame.mixer.Sound(filename)
        explosionSounds.append(snd)
        explosionSoundsNum += 1
    pygame.mixer.music.load('snd\cavalry.mp3')
    pygame.mixer.music.play()
    
    if testMode == 1:
        lives = 3
        plShotInterval = 10
        invulTime = 50
        plShip.speedx = 5
        plShip.speedy = 5
        plShip.xMoveBorder = 1000

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
                    plShotsSpriteGroup.add(playerShotSimple(plShip.rect, 'gfx\playerShotSimple.png'))
                    plShotTimeout = plShotInterval

# добавляем вражеские корабли
            if enemyShipGroupTimer > 0:
                enemyShipGroupTimer -= 1
            if enemyShipGroupTimer == 0 and len(enemyShipsSpritesGroup) == 0 and enemyShipCount == 0 or \
                enemyShipCount == 0 and level[0] == 'next':
                if level[0] == 'next':
                    level.pop(0)
                else:
                    enemyShipGroupTimer = enemyShipGroupInterval
                enemyShipType = level.pop(0)
                enemyShipCount = level.pop(0)
                enemyShipRandomCount = random.randint(0, level.pop(0))
                enemyShipCount += enemyShipRandomCount
                enemyShipAppearTime = level.pop(0)
                if level == []:
                    level = list(level1)
                if level[0] == 'bonus': #смотрим, не надо ли нам добавить бонус после этой волны
                    bonus = level.pop(0)
                    bonus = level.pop(0)
            if enemyShipGroupTimer == 0 and enemyShipCount > 0:
                if signRandomizer == []:
                    signRandomizer = list(signRandomizerTemplate)
                if random.randint(1, enemyShipAppearTime) == 1:
                    enemyShipsSpritesGroup.add(enemyShipType(signRandomizer.pop()))
                    enemyShipCount -= 1

# проверяем столкновения
            for ship in enemyShipsSpritesGroup:
                if plShip.invul == 0:
                    if ship.rect.colliderect(plShip.rect):
                        ship.exist = False
                        lives -= 1
                        plShip.invul = invulTime
                        metalSound1.play()
                        explosionsSpriteGroup.add(explosion1(ship.rect))
                        if lives == 0:
                            plShip.exist = False
                            explosionsSpriteGroup.add(explosion1(plShip.rect))
                            plShipSpriteGroup.remove(plShip)

            for shot in enemyShotsSpriteGroup:
                if plShip.invul == 0:
                    if shot.rect.colliderect(plShip.rect):
                        lives -= 1
                        plShip.invul = invulTime
                        shot.exist = False
                        metalSound2.play()
                        if lives == 0:
                            plShip.exist = False
                            explosionsSpriteGroup.add(explosion1(plShip.rect))
                            plShipSpriteGroup.remove(plShip)
        
            for shot in plShotsSpriteGroup:
                for ship in enemyShipsSpritesGroup:
                    if shot.rect.colliderect(ship.rect):
                        shot.exist = False
                        ship.exist = False
                        explosionSounds[random.randint(0, explosionSoundsNum)].play()
                        explosionsSpriteGroup.add(explosion1(ship.rect))
                        score += ship.score

            for bon in bonusSpriteGroup:
                if bon.rect.colliderect(plShip.rect):
                    dingSound1.play()
                    bon.exist = False
                    plShip.activateBonus(bon)

# двигаем все спрайты и удаляем отработавшие
        for sprite in enemyShipsSpritesGroup:
            if sprite.exist == True:
                sprite.move(plShip.rect)
            else:
                enemyShipsSpritesGroup.remove(sprite)
        for sprite in plShotsSpriteGroup:
            if sprite.exist == True:
                sprite.move()
            else:
                plShotsSpriteGroup.remove(sprite)
        for sprite in enemyShotsSpriteGroup:
            if sprite.exist == True:
                sprite.move()
            else:
                enemyShotsSpriteGroup.remove(sprite)
        for sprite in explosionsSpriteGroup:
            if sprite.exist == True:
                sprite.move()
            else:
                # если это - последний оставшийся взрыв и нам надо добавить бонус, то самое время
                if len(explosionsSpriteGroup) == 1 and bonus != '':
                    bonusSpriteGroup.add(bonus1(sprite.rect, bonus))
                    bonus = ''
                explosionsSpriteGroup.remove(sprite)
        for sprite in bonusSpriteGroup:
            if sprite.exist == True:
                sprite.move()
            else:
                bonusSpriteGroup.remove(sprite)
 
# рисуем всё
        gameScreen.fill(black)
        starSky(gameScreen)
        plShipSpriteGroup.draw(gameScreen)
        bonusSpriteGroup.draw(gameScreen)
        enemyShipsSpritesGroup.draw(gameScreen)
        plShotsSpriteGroup.draw(gameScreen)
        enemyShotsSpriteGroup.draw(gameScreen)
        explosionsSpriteGroup.draw(gameScreen)
        
        scoreText = regularFont.render(str(score), 1, grey)
        gameScreen.blit(scoreText, (1000, 6))

        enemyShipGroupTimerText = regularFont.render(str(enemyShipGroupTimer), 1, grey)
        gameScreen.blit(enemyShipGroupTimerText, (200, 6))
        
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
            if gameOverTimer > 600:
                pygame.quit()
                mainMenu()
                
        pygame.display.update()
        clock.tick(100)

    
if __name__ == "__main__":

    starSkyInit()
    clock = pygame.time.Clock()
    pygame.font.init()
    regularFont = pygame.font.Font('gfx\invasion2000.ttf', 24)
    largeFont = pygame.font.Font('gfx\invasion2000.ttf', 100)
    loadfont(bytes('gfx\invasion2000.ttf', encoding='utf-8'))
    root = makeRoot()
    root.option_add("*font", "invasion2000 24")
    mainMenu()
    root.mainloop()
    

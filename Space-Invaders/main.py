import random
import pygame
from pygame.locals import *
import tkinter as tk
from time import sleep, clock
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
    allSprites = pygame.sprite.Group()
    plShip = playerShip()
    allSprites.add(plShip)
    carryOn = True
    while carryOn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            carryOn = False
        if keys[K_UP]:
            if (plShip.rect.y - plShip.speedy) < 0:
                plShip.rect.y = 0
            else:
                plShip.rect.y -= plShip.speedy
        if keys[K_DOWN]:
            if (plShip.rect.y + plShip.speedy) > (windowHeight - plShip.rect.height):
                plShip.rect.y = windowHeight - plShip.rect.height
            else:
                plShip.rect.y += plShip.speedy
        if keys[K_RIGHT]:
            if (plShip.rect.x + plShip.speedx) > 300:
                plShip.rect.x = 300
            else:
                plShip.rect.x += plShip.speedx
        if keys[K_LEFT]:
            if (plShip.rect.x - plShip.speedx) < 0:
                plShip.rect.x = 0
            else:
                plShip.rect.x -= plShip.speedx

        gameScreen.fill(black)
        starSky()
        allSprites.draw(gameScreen)
        pygame.display.update()
        clock.tick(100)
    
if __name__ == "__main__":
    global windowWidth
    global windowHeight
    windowWidth = 1200
    windowHeight = 600
    black = (0, 0, 0)
    grey = (240, 240, 240)
    starSkyInit()
    clock = pygame.time.Clock()
    pygame.font.init()
    regularFont = pygame.font.Font('gfx\invasion2000.ttf', 24)
    spacelib.loadfont(bytes('gfx\invasion2000.ttf', encoding='utf-8'))
    makeRoot()
    root.option_add("*font", "invasion2000 24")
    mainMenu()
    root.mainloop()
    

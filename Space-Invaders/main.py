import spaceLib
import tkinter as tk
import random
from threading import Thread
from time import sleep


def makeRoot():
    tkRootWidth = 1200
    tkRootHeight = 600
    global root
    root = tk.Tk()
    root.title('SPACE INVADERS')
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(tkRootWidth, tkRootHeight))
    
    
def _delete_window():
    try:
        root.destroy()
    except:
        pass

    
def mainMenu():

    def startGame(event):
        rootFrame.pack_forget()
        rootFrame.destroy()
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
        star['x'] = random.randint(10, 1199)
        star['y'] = random.randint(1, 599)
        star['speed'] = random.randint(1, 5)
        star['me'] = ""
        return star
    
    global stars   
    stars = []
    for _ in range(50):
        stars.append(makeNewStar())
        

def starFall():
    global starThread

    def moveStars():
        for i in stars:
            i['x'] -= i['speed']
            if i['x'] < 1:
                mainCanvas.delete(i['me'])
                i['x'] = 1199
                i['y'] = random.randint(1, 599)
                i['me'] = mainCanvas.create_line(i['x'], i['y'], i['x'] + 1, i['y'], fill="snow")
            mainCanvas.move(i['me'], -i['speed'], 0)
        mainCanvas.after(10, moveStars)

    for i in stars:
        i['me'] = mainCanvas.create_line(i['x'], i['y'], i['x'] + 1, i['y'], fill="snow")
    starThread = Thread(target=moveStars)
    starThread.start()


def playGame():
    
    def escape(event):
        starThread.join()
        mainCanvas.pack_forget()
        mainCanvas.destroy()
        mainMenu()
    
    global mainCanvas    
    mainCanvas = tk.Canvas(root, highlightthickness=0)
    mainCanvas.bind("<Escape>", escape)
    mainCanvas.pack(fill="both", expand=1)
    mainCanvas.focus_set()
    starFall()


if __name__ == "__main__":
    spaceLib.loadfont(bytes('gfx\invasion2000.ttf', encoding='utf-8'))
    makeRoot()    
    root.option_add("*font", "invasion2000 24")
    starSkyInit()
    mainMenu()
    while True:
        root.mainloop()
    

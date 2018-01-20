from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
import random
from main import windowWidth, windowHeight, grey, black
import tkinter as tk

FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20


def loadfont(fontpath, private=True, enumerable=False):
    '''
    Makes fonts located in file `fontpath` available to the font system.
    `private`     if True, other processes cannot see this font, and this 
                  font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts
    See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx
    '''
    # This function was taken from
    # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
    # This function is written for Python 2.x. For 3.x, you
    # have to convert the isinstance checks to bytes and str
    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, bytes):
        pathbuf = create_unicode_buffer(str)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or bytes')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)


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


def starSky(gameScreen):
    for s in stars:
        s['x'] -= s['speed']
        if s['x'] < 1:
            s['x'] = windowWidth - 1
            s['y'] = random.randint(1, (windowHeight - 1))
            s['speed'] = random.randint(1, 3)
        gameScreen.set_at((s['x'], s['y']), grey)

def makeRoot():
    root = tk.Tk()
    root.title('SPACE INVADERS')
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(windowWidth, windowHeight))
    return root

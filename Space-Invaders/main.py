import tkinter as tk
import spaceLib


class mainWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.header = tk.Label(self, text="SPACE INVADERS", anchor="w", font=("invasion2000",80))
        self.header.pack(side="top")
        
        
class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # create a prompt, an input box, an output label,
        # and a button to do the computation
        self.prompt = tk.Label(self, text="Enter a number:", anchor="w")
        self.entry = tk.Entry(self)
        self.submit = tk.Button(self, text="Submit", command = self.calculate)
        self.output = tk.Label(self, text="")

        # lay the widgets out on the screen. 
        self.prompt.pack(side="top", fill="x")
        self.entry.pack(side="top", fill="x", padx=20)
        self.output.pack(side="top", fill="x", expand=True)
        self.submit.pack(side="right")


if __name__ == "__main__":
    spaceLib.loadfont(bytes('gfx\invasion2000.ttf', encoding='utf-8'))
    tkRootWidth = 1200
    tkRootHeight = 600
    root = tk.Tk()
    root.title('SPACE INVADERS')
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(tkRootWidth, tkRootHeight))
    root.tk_setPalette(background="black", fg="lavender")
    mainWindow(root).pack(fill="both", expand=True)
    root.mainloop()
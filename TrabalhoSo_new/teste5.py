import psutil
import os
import time
import tkinter
from tkinter import *
list = [1491]


class JanelaDesktop:
    def __init__(self):
        self.window = tkinter.Tk()

        self.window.geometry("650x460")
        self.canvas = Canvas(self.window, width=650, height=460, bg="#404040")
        self.canvas.create_rectangle(199, 199, 301, 301, outline='white')
        self.red = self.canvas.create_rectangle(200, 250, 300, 300, fill='red')
        self.canvas.pack()

    def atualiza(self):
        p = psutil.Process(1409)
        x = int(p.cpu_percent(interval=3))
        print(x)
        self.canvas.coords(self.red, 200, int(f"{300 - x}"), 300, 300)
        #print(int(f"{int(p.cpu_percent(interval=3))}"))
        self.window.after(1000, self.atualiza)

    def run(self):
        self.window.after(0, self.atualiza)
        self.window.mainloop()


janela = JanelaDesktop()
janela.run()






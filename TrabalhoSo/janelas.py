import tkinter
import time
from tkinter import *
import platform
import psutil
from datetime import datetime


class JanelaCMD:
    def __init__(self):
        self.window = tkinter.Tk()

        ############# INFORMACOES DA JANELA ############
        self.window.title("CMD")
        self.window.resizable(False, False)
        #self.window.geometry(f"500x300")

        self.frame1 = Frame(self.window)
        self.frame1.grid(column=0, row=0)

        ############# VARIAVEIS #############
        self.row = 0

        ### MenuButton ###
        self.men1 = Menubutton(self.frame1, text="Comandos", relief=RAISED)
        self.men1.menu = Menu(self.men1)
        self.men1["menu"] = self.men1.menu
        self.men1.menu.add_command(label="clear")
        self.men1.menu.add_command(label="vasco")
        self.men1.menu.add_command(label="time")

        self.men1.grid(column=0, row=0)

        ### Text box ###
        self.txt1 = Text(self.frame1, bg="#404040", fg="white", insertbackground="white", font=("arial", 12, "bold"))
        self.txt1.insert(INSERT, "ronaldo:~$ ")
        self.txt1.tag_add("start", "1.0", "1.10")
        self.txt1.tag_configure("start", foreground="#6CF345")

        self.window.bind('<KeyPress-Return>', self.parse1)
        self.window.bind('<KeyRelease-Return>', self.parse2)
        self.window.bind('<BackSpace>', self.parse3)

        self.txt1.grid(column=0, row=1)

    ### Key Event Return ###
    def parse1(self, event):
        # Conta o numero de colunas no texto para pegar o texto de cada linha corretamente
        text = self.txt1.get('1.0', 'end-1c')
        self.row = text.count('\n')

        self.executar_comando(self.txt1.get(f"{self.row}.0", f"end -2 chars"))

    def parse2(self, event):
        self.txt1.insert(INSERT, "ronaldo:~$ ")
        self.txt1.tag_add("start", "end -1 lines", "end -2 chars")
        self.txt1.tag_configure("start", foreground="#6CF345")

    ### Key Event BackSpace ###
    def parse3(self, event):
        if self.txt1.get("current -1 chars") == '$':
            self.txt1.insert(INSERT, " ")

    def executar_comando(self, comando):
        comando = comando[11:len(comando)]

        dicio = {'clear': lambda: self.txt1.delete(1.0, END),
                 'vasco': lambda: self.txt1.insert(INSERT, "Muito Ruim\n"),
                 'time': lambda: self.txt1.insert(INSERT, f"{time.ctime()}\n")}

        try:
            dicio[comando]()
        except:
            self.txt1.insert(INSERT, "comando nao encontrado\n")

    def quit(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()


class JanelaSistema:
    def __init__(self):
        self.window = tkinter.Tk()

        self.window.geometry("800x300")

        self.frame = Frame(self.window)
        self.frame.pack()
        ### variaveis ###

        ### Informacoes do sistema ###
        self.txt = Text(self.window, bg="#404040", fg="white", insertbackground="white", font=("times", 14))
        self.txt.insert(INSERT, f"System: {platform.system()}\n")
        self.txt.insert(INSERT, f"Node Name: {platform.node()}\n")
        self.txt.insert(INSERT, f"Release: {platform.release()}\n")
        self.txt.insert(INSERT, f"Version: {platform.version()}\n")
        self.txt.insert(INSERT, f"Machine: {platform.machine()}\n")
        self.txt.insert(INSERT, f"Processor: {platform.processor()}\n")
        self.txt.pack()

    def get_size(self, bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def run(self):
        self.window.mainloop()


show = False


class JanelaDesktop:
    def __init__(self):
        self.window = tkinter.Tk()

        self.window.resizable(False, False)

        ### Desativa a caixa que fica em volta da janela ###
        #self.window.overrideredirect(1)

        ### Variaveis ###
        self.janela_cmd = NONE
        self.janela_menu_desktop = NONE
        self.janela_sistema = NONE

        ### Centralizar Janela ###

        self.window_width = 1280
        self.window_height = 720

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        self.x_cordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_cordinate = int((self.screen_height/2) - (self.window_height/2))

        self.window.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height,
                                                  self.x_cordinate, self.y_cordinate))

        ### Canvas ###
        self.canvas = Canvas(self.window, width=1280, height=720)

        self.imag1 = PhotoImage(file=r"Imagens/planodefundo.png")
        self.canvas.create_image(0, 0, image=self.imag1, anchor='nw')

        self.imag2 = PhotoImage(file=r"Imagens/cmd.png")
        self.imag2 = self.imag2.subsample(3, 3)
        self.btn2 = Button(self.canvas, image=self.imag2, command=lambda: self.window_cmd())
        self.canvas.create_window(10, 10, anchor='nw', window=self.btn2)

        self.btn3 = Button(self.canvas, bg="#404040", state="disabled", width=160, height=3)
        self.canvas.create_window(-3, 675, anchor='nw', window=self.btn3)

        self.imag3 = PhotoImage(file=r"Imagens/icone.png")
        self.btn1 = Button(self.canvas, image=self.imag3, bg="#404040", command=lambda: self.window_menu_desktop())
        self.canvas.create_window(-3, 675, anchor='nw', window=self.btn1)

        ### desktop widget ###
        self.imag4 = PhotoImage(file=r"Imagens/desktopMenu.png")
        self.btn4 = Button(self.canvas, image=self.imag4, bg="#404040", state="disabled")
        self.canvas.create_window(-3, 420, anchor='nw', window=self.btn4, state='hidden')

        self.imag5 = PhotoImage(file=r"Imagens/icone2.png")
        self.btn5 = Button(self.canvas, image=self.imag5, bg="#404040", command=lambda: self.quitAll())
        self.canvas.create_window(25, 615, anchor='nw', window=self.btn5, state="hidden")

        self.imag6 = PhotoImage(file=r"Imagens/icone3.png")
        self.btn6 = Button(self.canvas, image=self.imag6, bg="#404040", command=lambda: self.window_sistema())
        self.canvas.create_window(85, 450, anchor='nw', window=self.btn6, state="hidden")
        #self.canvas.create_rectangle(0, 500, 1280, 720, fill="#404040")

        self.imag7 = PhotoImage(file=r"Imagens/icone4.png")
        self.imag7 = self.imag7.subsample(3, 3)
        self.btn7 = Button(self.canvas, image=self.imag7, command=lambda: self.window_cmd(), bg="white")
        self.canvas.create_window(10, 100, anchor='nw', window=self.btn7)

        self.canvas.pack()

    def window_cmd(self):
        self.janela_cmd = JanelaCMD()
        self.janela_cmd.run()

    def window_sistema(self):
        self.janela_sistema = JanelaSistema()
        self.janela_sistema.run()

    def window_menu_desktop(self):
        global show

        if not show:
            self.canvas.itemconfig(5, state="normal")
            self.canvas.itemconfig(6, state="normal")
            self.canvas.itemconfig(7, state="normal")
            show = True
        else:
            self.canvas.itemconfig(5, state="hidden")
            self.canvas.itemconfig(6, state="hidden")
            self.canvas.itemconfig(7, state="hidden")
            show = False

    def quitAll(self):
        self.window.destroy()
        try:
            self.janela_cmd.quit()
        except:
            print()

    def run(self):
        self.window.mainloop()

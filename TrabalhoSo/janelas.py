import tkinter
import time
from tkinter import *


class JanelaCMD:
    def __init__(self):
        self.window = tkinter.Tk()

        ############# INFORMACOES DA JANELA #############
        self.window.title("CMD")
        self.window.resizable(False, False)
        #self.window.geometry(f"500x300")

        self.frame1 = Frame(self.window)
        #self.frame2 = Frame(self.window)

        self.frame1.grid(column=0, row=0)
        #self.frame2.grid(column=0, row=1)

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

        print(self.txt1.get("current -2 chars"))

    def executar_comando(self, comando):
        comando = comando[11:len(comando)]

        dicio = {'clear': lambda: self.txt1.delete(1.0, END),
                 'vasco': lambda: self.txt1.insert(INSERT, "Muito Ruim\n"),
                 'time': lambda: self.txt1.insert(INSERT, f"{time.ctime()}\n")}

        try:
            dicio[comando]()
        except:
            self.txt1.insert(INSERT, "comando nao encontrado\n")

    def run(self):
        self.window.mainloop()


class JanelaDesktop:
    def __init__(self):
        self.window = tkinter.Tk()

        self.window.resizable(False, False)
        self.window.geometry("600x450")

        self.janela_cmd = None

        self.frame1 = Frame(self.window)

        self.frame1.grid(column=0, row=0, sticky="N,S,E,W")

        self.imag1 = PhotoImage(file=r"Imagens/cmd.png")
        self.imag1 = self.imag1.subsample(3,3)
        self.btn1 = Button(self.frame1, image=self.imag1, command=lambda: self.window_cmd())
        self.btn1.grid()

    def window_cmd(self):
        self.janela_cmd = JanelaCMD()
        self.janela_cmd.run()

    def run(self):
        self.window.mainloop()

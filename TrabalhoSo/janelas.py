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

    def run(self):
        self.window.mainloop()


class JanelaDesktop2:
    def __init__(self):
        self.window = tkinter.Tk()

        self.window.resizable(False, False)
        self.window.geometry("1280x720")

        self.janela_cmd = None

        self.frame1 = Frame(self.window)
        self.frame2 = Frame(self.window)

        self.frame1.grid(column=0, row=0, sticky="N,S,E,W")
        self.frame2.grid(column=0, row=1)
        self.imag1 = PhotoImage(file=r"Imagens/cmd.png")
        self.imag1 = self.imag1.subsample(3, 3)
        self.btn1 = Button(self.frame1, image=self.imag1, command=lambda: self.window_cmd())
        self.btn1.grid()

        self.btn2 = Button(self.frame2, text="vasco")
        self.btn2.grid()

    def window_cmd(self):
        self.janela_cmd = JanelaCMD()
        self.janela_cmd.run()

    def run(self):
        self.window.mainloop()


class JanelaDesktop:
    def __init__(self):
        self.window = tkinter.Tk()

        #self.window.resizable(False, False)

        ### Desativa a caixa que fica em volta da janela ###
        #self.window.overrideredirect(1)

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

        self.plano_de_fundo = PhotoImage(file=r"Imagens/planodefundo.png")
        self.canvas.create_image(0, 0, image=self.plano_de_fundo, anchor='nw')

        self.canvas.create_rectangle(0, 680, 1280, 720, fill="#404040")

        self.imag1 = PhotoImage(file=r"Imagens/cmd.png")
        self.imag1 = self.imag1.subsample(3, 3)
        self.btn2 = Button(self.canvas, image=self.imag1, command=lambda: self.window_cmd())
        self.canvas.create_window(10, 10, anchor='nw', window=self.btn2)

        self.btn3 = Button(self.canvas, bg="#404040", state="disabled", width=160, height=3)
        self.canvas.create_window(-3, 675, anchor='nw', window=self.btn3)

        self.icone = PhotoImage(file=r"Imagens/icone6.png")
        self.btn1 = Button(self.canvas, text="VASCO", image=self.icone, bg="#404040")
        self.canvas.create_window(-3, 675, anchor='nw', window=self.btn1)

        self.canvas.pack()

    def window_cmd(self):
        self.janela_cmd = JanelaCMD()
        self.janela_cmd.run()

    def run(self):
        self.window.mainloop()
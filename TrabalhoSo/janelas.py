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

        self.window.geometry("800x500")

        ### variaveis ###
        self.boot_time_timestamp = psutil.boot_time()
        self.bt = datetime.fromtimestamp(self.boot_time_timestamp)

        self.cpufreq = psutil.cpu_freq()

        self.svmem = psutil.virtual_memory()
        self.swap = psutil.swap_memory()

        self.partitions = psutil.disk_partitions()
        self.partition_usage = NONE
        self.disk_io = psutil.disk_io_counters()

        self.if_addrs = psutil.net_if_addrs()
        self.net_io = psutil.net_io_counters()

        ### Informacoes do sistema ###
        self.txt = Text(self.window, bg="#404040", fg="white", font=("arial", 11), height=300, width=300)
        self.txt.insert(INSERT, f"========== System Information ==========\n"
                                f"System:  {platform.system()}\n"
                                f"Node Name:  {platform.node()}\n"
                                f"Release:  {platform.release()}\n"
                                f"Version:  {platform.version()}\n"
                                f"Machine:  {platform.machine()}\n"
                                f"Processor:  {platform.processor()}\n")

        self.txt.insert(INSERT, f"========== Boot Time: ==========\n"
                                f"Boot time:  {self.bt.year}/{self.bt.month}/{self.bt.day} "
                                f"{self.bt.hour}:{self.bt.minute}:{self.bt.second}\n")

        self.txt.insert(INSERT, f"========== CPU Information: ==========\n"
                                f"Physical Cores:  {psutil.cpu_count(logical=False)}\n"
                                f"Total Cores:  {psutil.cpu_count(logical=True)}\n"
                                f"Max Frequency:  {self.cpufreq.max:.2f}Mhz\n"
                                f"Min Frequency:  {self.cpufreq.min:.2f}Mhz\n"
                                f"Current Frequency:  {self.cpufreq.current:.2f}Mhz\n"
                                f"CPU Usage Per Core: \n")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
            self.txt.insert(INSERT, f"Core {i}:  {percentage}%\n")
        self.txt.insert(INSERT, f"Total CPU Usage:  {psutil.cpu_percent()}%\n")

        self.txt.insert(INSERT, f"========== Memory Usage: ==========\n"
                                f"Total:  {self.get_size(self.svmem.total)}\n"
                                f"Available:  {self.get_size(self.svmem.available)}\n"
                                f"Used:  {self.get_size(self.svmem.used)}\n"
                                f"Percentage:  {self.get_size(self.svmem.percent)}%\n"
                                f"===== Swap =====\n"
                                f"Total:  {self.get_size(self.swap.total)}\n"
                                f"Free:  {self.get_size(self.swap.free)}\n"
                                f"Used:  {self.get_size(self.swap.used)}\n"
                                f"Percentage:  {self.get_size(self.swap.percent)}%\n")

        self.txt.insert(INSERT, f"========== Disk Usage: ==========\n"
                                f"Partitions and Usage: \n")

        for partition in self.partitions:
            self.txt.insert(INSERT, f"=== Device: {partition.device} ===\n"
                                    f"  Mountpoint: {partition.mountpoint}\n"
                                    f"  File system type: {partition.fstype}\n")

            try:
                self.partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue

            self.txt.insert(INSERT, f"  Total Size: {self.get_size(self.partition_usage.total)}\n"
                                    f"  Used: {self.get_size(self.partition_usage.used)}\n"
                                    f"  Free: {self.get_size(self.partition_usage.free)}\n"
                                    f"  Percentage: {self.get_size(self.partition_usage.percent)}%\n")

        self.txt.insert(INSERT, f"Total read: {self.get_size(self.disk_io.read_bytes)}\n"
                                f"Total write: {self.get_size(self.disk_io.write_bytes)}\n")

        self.txt.insert(INSERT, f"========== Network Information: ==========\n")
        for interface_name, interface_addresses in self.if_addrs.items():
            for address in interface_addresses:
                self.txt.insert(INSERT, f"=== Interface: {interface_name} ===\n")
                if str(address.family) == 'AddressFamily.AF_INET':
                    self.txt.insert(INSERT, f"  IP Address: {address.address}\n"
                                            f"  Netmask: {address.netmask}\n"
                                            f"  Broadcast IP: {address.broadcast}\n")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    self.txt.insert(INSERT, f"  MAC Address: {address.address}\n"
                                            f"  Netmask: {address.netmask}\n"
                                            f"  Broadcast MAC: {address.broadcast}\n")
        self.txt.insert(INSERT, f"Total Bytes Sent: {self.get_size(self.net_io.bytes_sent)}\n"
                                f"Total Bytes Received: {self.get_size(self.net_io.bytes_recv)}\n")

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

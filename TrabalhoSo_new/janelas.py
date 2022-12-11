import tkinter
import time
from tkinter import *
import platform
import psutil
import os
from datetime import datetime
from datetime import time

from unidecode import unidecode


class JanelaArquivo:
    def __init__(self):
        self.window = tkinter.Toplevel()
        self.window.geometry("712x562")
        self.window.title("Arquivos")

        self.frame1= Frame(self.window)
        self.frame1.grid()

        self.img1 = PhotoImage(file=r"Imagens/pasta.png")

        self.listaBtn = []

        self.lista = os.listdir(path='/home/ronaldinho')
        self.lista = [l for l in self.lista if l[0] != '.']
        for i in range(len(self.lista)):
            self.lista[i] = unidecode(self.lista[i])
        self.lista = sorted(self.lista)

        y = 0
        x = 0
        for i in range(0, len(self.lista)):
            if i % 4 == 0 and i != 0:
                y += 1
                x = 0

            self.listaBtn.append(Button(self.frame1, text=self.lista[i], font=("arial", 12), image=self.img1,
                              compound="bottom"))
            self.listaBtn[i].grid(column=x, row=y)
            x += 1

    def atualizar(self):

        for item in self.listaBtn:
            item.destroy()

        self.listaBtn = []

        self.lista = os.listdir(path='/home/ronaldinho')
        self.lista = [l for l in self.lista if l[0] != '.']
        for i in range(len(self.lista)):
            self.lista[i] = unidecode(self.lista[i])
        self.lista = sorted(self.lista)

        y = 0
        x = 0
        for i in range(0, len(self.lista)):
            if i % 4 == 0 and i != 0:
                y += 1
                x = 0

            self.listaBtn.append(Button(self.frame1, text=self.lista[i], font=("arial", 12), image=self.img1,
                                        compound="bottom"))
            self.listaBtn[i].grid(column=x, row=y)
            x += 1

        self.window.after(3000, self.atualizar)

    def run(self):
        self.window.after(1000, self.atualizar)
        self.window.mainloop()


class JanelaMemoria:
    def __init__(self):
        self.window = tkinter.Toplevel()
        self.window.geometry("850x450")
        self.window.title("Memoria")

        ### Variaveis ###
        self.linhasRAM = []
        self.linhasDisco = []

        self.svmem = psutil.virtual_memory()

        self.partitions = psutil.disk_partitions()
        self.partition_usage = None
        self.disk_io = None

        try:
            self.partition_usage = psutil.disk_usage(self.partitions[0].mountpoint)
        except PermissionError:
            pass

        self.arcDisco = int((self.partition_usage.used * 360) / self.partition_usage.total)

        ### Canvas ###
        self.canvas = Canvas(self.window, width=850, height=450, bg="#404040")
        self.canvas.create_text(90, 315, text=f"% de utilizacao: {00}%", fill="white")      # ID 1
        self.canvas.create_text(510, 315, text=f"% de utilizacao: {00}%", fill="white")     # ID 2

        self.canvas.create_text(200, 20, text="MEMORIA", fill="white", font=("arial", 20))  # ID 3
        self.canvas.create_text(620, 20, text="DISCO", fill="white", font=("arial", 20))    # ID 4

        self.canvas.create_text(610, 60, text="Dispositivo: " + self.partitions[0].device,  # ID 5
                                fill="white", font=("arial", 15))

        self.canvas.create_text(200, 100, text="Total: " + self.get_size(self.svmem.total), fill="white")  # 6
        self.canvas.create_text(200, 275, text="Usado: 0GB", fill="white")   # 7
        self.canvas.create_text(620, 100, text="Total: " + self.get_size(self.partition_usage.total), fill="white")  # 8
        self.canvas.create_text(620, 275, text="Usado: " + self.get_size(self.partition_usage.used), fill="white")   # 9

        self.canvas.create_text(390, 315, text="100%", fill="white")  # ID 10
        self.canvas.create_text(400, 440, text="0%", fill="white")    # ID 11
        self.canvas.create_text(810, 315, text="100%", fill="white")  # ID 12
        self.canvas.create_text(820, 440, text="0%", fill="white")    # ID 13

        self.canvas.create_rectangle(9, 329, 411, 431, fill="#404040", outline="white")           # ID 14
        self.canvas.create_rectangle(429, 329, 831, 431, fill="#404040", outline="white")         # ID 15

        self.canvas.create_arc(100, 120, 300, 260, start=0, extent=180, fill="blue")              # ID 16
        self.canvas.create_arc(520, 120, 720, 260, start=0, extent=self.arcDisco, fill="blue")    # ID 17

        self.linhasRAM.append(self.canvas.create_line(10, 430, 90, 430, fill="green", width=2))
        self.linhasRAM.append(self.canvas.create_line(90, 430, 170, 430, fill="green", width=2))
        self.linhasRAM.append(self.canvas.create_line(170, 430, 250, 430, fill="green", width=2))
        self.linhasRAM.append(self.canvas.create_line(250, 430, 330, 430, fill="green", width=2))
        self.linhasRAM.append(self.canvas.create_line(330, 430, 410, 430, fill="green", width=2))

        self.linhasDisco.append(self.canvas.create_line(430, 430, 510, 430, fill="green", width=2))
        self.linhasDisco.append(self.canvas.create_line(510, 430, 590, 430, fill="green", width=2))
        self.linhasDisco.append(self.canvas.create_line(590, 430, 670, 430, fill="green", width=2))
        self.linhasDisco.append(self.canvas.create_line(670, 430, 750, 430, fill="green", width=2))
        self.linhasDisco.append(self.canvas.create_line(750, 430, 830, 430, fill="green", width=2))

        self.canvas.pack()

    def atualizar(self):
        ### uso da memoria ###
        self.svmem = psutil.virtual_memory()

        self.get_size(self.svmem.total)          # Total
        self.get_size(self.svmem.available)      # Available
        self.get_size(self.svmem.used)           # Used
        porcentagem = self.svmem.percent         # Percent

        self.canvas.coords(self.linhasRAM[0], 10, self.canvas.coords(self.linhasRAM[1])[1],
                           90, self.canvas.coords(self.linhasRAM[1])[1])
        self.canvas.coords(self.linhasRAM[1], 90, self.canvas.coords(self.linhasRAM[2])[1],
                           170, self.canvas.coords(self.linhasRAM[2])[1])
        self.canvas.coords(self.linhasRAM[2], 170, self.canvas.coords(self.linhasRAM[3])[1],
                           250, self.canvas.coords(self.linhasRAM[3])[1])
        self.canvas.coords(self.linhasRAM[3], 250, self.canvas.coords(self.linhasRAM[4])[1],
                           330, self.canvas.coords(self.linhasRAM[4])[1])
        self.canvas.coords(self.linhasRAM[4], 300, 430 - int(porcentagem),
                           410, 430 - int(porcentagem))

        self.canvas.itemconfig(1, text=f"% de utilizacao: {porcentagem}%")   # % Utilizacao RAM

        ### Uso do Disco ###
        self.partitions = psutil.disk_partitions()
        self.partition_usage = NONE
        self.disk_io = psutil.disk_io_counters()

        self.partition_usage = psutil.disk_usage(self.partitions[0].mountpoint)

        try:
            self.partition_usage = psutil.disk_usage(self.partitions[0].mountpoint)
        except PermissionError:
            pass

        self.get_size(self.partition_usage.used)
        self.get_size(self.partition_usage.free)
        porcentagem2 = self.partition_usage.percent

        self.canvas.coords(self.linhasDisco[0], 430, self.canvas.coords(self.linhasDisco[1])[1],
                           510, self.canvas.coords(self.linhasDisco[1])[1])
        self.canvas.coords(self.linhasDisco[1], 510, self.canvas.coords(self.linhasDisco[2])[1],
                           590, self.canvas.coords(self.linhasDisco[2])[1])
        self.canvas.coords(self.linhasDisco[2], 590, self.canvas.coords(self.linhasDisco[3])[1],
                           670, self.canvas.coords(self.linhasDisco[3])[1])
        self.canvas.coords(self.linhasDisco[3], 670, self.canvas.coords(self.linhasDisco[4])[1],
                           750, self.canvas.coords(self.linhasDisco[4])[1])
        self.canvas.coords(self.linhasDisco[4], 750, 430 - int(porcentagem2),
                           830, 430 - int(porcentagem2))

        self.canvas.itemconfig(2, text=f"% de utilizacao: {porcentagem2}%")  # % Utilizacao RAM
        self.canvas.itemconfig(7, text="Usado: " + self.get_size(self.svmem.used))
        self.canvas.itemconfig(16, extent=int((self.svmem.used * 360) / self.svmem.total))

        self.window.after(2000, self.atualizar)

    def get_size(self, bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def run(self):
        self.window.after(1000, self.atualizar)
        self.window.mainloop()


class JanelaProcessos:
    def __init__(self):
        self.window = tkinter.Toplevel()
        self.window.geometry("650x460")
        self.window.title("Processos")

        ### Variaveis ###
        self.objetos = None

        self.start_time = None
        self.end_time = None

        ### Frame ###
        self.canvas = Canvas(self.window, width=650, height=460, bg="#404040")
        self.canvas.pack()

        self.processSorted()

    def processSorted(self):
        self.canvas.delete("all")

        self.canvas.create_text(10, 10, anchor='nw', text='PID', fill='white')
        self.canvas.create_text(106, 10, anchor='nw', text='USUARIO', fill='white')
        self.canvas.create_text(252, 10, anchor='nw', text='%MEM', fill='white')
        self.canvas.create_text(368, 10, anchor='nw', text='TEMPO+', fill='white')
        self.canvas.create_text(484, 10, anchor='nw', text='COMANDO', fill='white')

        #Get list of running process sorted by Memory Usage
        listOfProcObjects = []
        # Iterate over the list
        for proc in psutil.process_iter():
            try:
                # Fetch process details as dict
                pinfo = proc.as_dict(attrs=['pid', 'status', 'name', 'username', 'memory_percent', 'create_time'])
                pinfo['rss'] = proc.memory_info().rss
                pinfo['status'] = proc.status()
                # Append dict to list
                listOfProcObjects.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        # Sort list of dict by key vms i.e. memory usage
        listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['memory_percent'], reverse=True)

        i = 50
        for elem in listOfProcObjects[:14]:
            self.canvas.create_text(10, i, anchor='nw', text=elem.get('pid'), fill='white')
            self.canvas.create_text(106, i, anchor='nw', text=elem.get('username'), fill='white')
            self.canvas.create_text(252, i, anchor='nw', text=("%.2f" % float(elem.get('memory_percent'))) + '%',
                                    fill='white')
            start_time = datetime.fromtimestamp(elem.get('create_time')).strftime("%H:%M:%S")
            end_time = datetime.now().strftime("%H:%M:%S")

            t1 = datetime.strptime(start_time, "%H:%M:%S")
            t2 = datetime.strptime(end_time, "%H:%M:%S")
            delta = t2 - t1

            self.canvas.create_text(368, i, anchor='nw', text=str(delta), fill='white')
            self.canvas.create_text(484, i, anchor='nw', text=elem.get('name'), fill='white')
            i += 30

        self.window.after(3000, self.processSorted)

    def run(self):
        self.window.mainloop()


class JanelaSistema:
    def __init__(self):
        self.window = tkinter.Toplevel()
        self.window.geometry("900x520")
        self.window.title("Sistema")

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
        self.txt.insert(1.0, datetime.now().strftime("%H:%M:%S\n"))
        self.txt.insert(INSERT, f"\n========== System Information ==========\n"
                                f"System:  {platform.system()}\n"
                                f"Node Name:  {platform.node()}\n"
                                f"Release:  {platform.release()}\n"
                                f"Version:  {platform.version()}\n"
                                f"Machine:  {platform.machine()}\n"
                                f"Processor:  {platform.processor()}\n")

        self.txt.insert(INSERT, f"\n\n========== Boot Time: ==========\n"
                                f"Boot time:  {self.bt.year}/{self.bt.month}/{self.bt.day} "
                                f"{self.bt.hour}:{self.bt.minute}:{self.bt.second}\n")

        self.txt.insert(INSERT, f"\n\n========== CPU Information: ==========\n"
                                f"Physical Cores:  {psutil.cpu_count(logical=False)}\n"
                                f"Total Cores:  {psutil.cpu_count(logical=True)}\n"
                                f"Current Frequency:  {self.cpufreq.current:.2f}Mhz\n"
                                f"CPU Usage Per Core: \n")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
            self.txt.insert(INSERT, f"Core {i}:  {percentage}%\n")
        self.txt.insert(INSERT, f"Total CPU Usage:  {psutil.cpu_percent()}%\n")

        self.txt.pack()

    def atu(self):
        self.txt.delete(1.0, END)

        self.txt.insert(1.0, datetime.now().strftime("%H:%M:%S\n"))
        self.txt.insert(INSERT, f"\n========== System Information ==========\n"
                                f"System:  {platform.system()}\n"
                                f"Node Name:  {platform.node()}\n"
                                f"Release:  {platform.release()}\n"
                                f"Version:  {platform.version()}\n"
                                f"Machine:  {platform.machine()}\n"
                                f"Processor:  {platform.processor()}\n")

        self.txt.insert(INSERT, f"\n\n========== Boot Time: ==========\n"
                                f"Boot time:  {self.bt.year}/{self.bt.month}/{self.bt.day} "
                                f"{self.bt.hour}:{self.bt.minute}:{self.bt.second}\n")

        self.txt.insert(INSERT, f"\n\n========== CPU Information: ==========\n"
                                f"Physical Cores:  {psutil.cpu_count(logical=False)}\n"
                                f"Total Cores:  {psutil.cpu_count(logical=True)}\n"
                                f"Current Frequency:  {self.cpufreq.current:.2f}Mhz\n"
                                f"CPU Usage Per Core: \n")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
            self.txt.insert(INSERT, f"Core {i}:  {percentage}%\n")
        self.txt.insert(INSERT, f"Total CPU Usage:  {psutil.cpu_percent()}%\n")

        self.txt.pack()

        self.window.after(1000, self.atu)

    def get_size(self, bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def run(self):
        self.window.after(1000, self.atu)
        self.window.mainloop()


class JanelaDesktop:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Desktop")

        self.window.resizable(False, False)

        ### Variaveis ###
        self.janela_cmd = None
        self.janela_menu_desktop = None
        self.janela_sistema = None
        self.janela_sistema2 = None
        self.janela_processos = None
        self.janela_memoria = None
        self.janela_arquivos = None

        ### Centralizar Janela ###

        self.window_width = 1024
        self.window_height = 560

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        self.x_cordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_cordinate = int((self.screen_height/2) - (self.window_height/2))

        self.window.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height,
                                                  self.x_cordinate, self.y_cordinate))

        ### Canvas ###
        self.canvas = Canvas(self.window, width=self.window_width, height=self.window_height, bg="#404040")

        self.canvas.create_rectangle(10, 10, 171, 550, fill="grey")

        self.img1 = PhotoImage(file=r"Imagens/monitor.png")
        self.img1 = self.img1.subsample(3, 3)
        self.canvas.create_image(53, 20, anchor=NW, image=self.img1)

        self.img2 = PhotoImage(file=r"Imagens/Sistema.png")
        self.btn1 = Button(self.canvas, image=self.img2, background="grey", command=lambda: self.window_sistema())
        self.canvas.create_window(13, 130, anchor='nw', window=self.btn1)

        self.img3 = PhotoImage(file=r"Imagens/arquivos.png")
        self.btn2 = Button(self.canvas, image=self.img3, background="grey", command=lambda: self.window_arquivos())
        self.canvas.create_window(13, 180, anchor='nw', window=self.btn2)

        self.img4 = PhotoImage(file=r"Imagens/processos.png")
        self.btn3 = Button(self.canvas, image=self.img4, background="grey", command=lambda: self.window_processos())
        self.canvas.create_window(13, 230, anchor='nw', window=self.btn3)

        self.img5 = PhotoImage(file=r"Imagens/memoria.png")
        self.btn4 = Button(self.canvas, image=self.img5, background="grey", command=lambda: self.window_memoria())
        self.canvas.create_window(13, 280, anchor='nw', window=self.btn4)

        self.img6 = PhotoImage(file=r"Imagens/Terminal.png")
        self.btn5 = Button(self.canvas, image=self.img6, background="grey", command=lambda: os.system("gnome-terminal"))
        self.canvas.create_window(13, 330, anchor='nw', window=self.btn5)

        self.canvas.create_text(65, 500, anchor='nw', text=datetime.now().strftime("%H:%M:%S"))
        self.canvas.pack()

    def atualizar(self):
        self.canvas.itemconfig(8, text=datetime.now().strftime("%H:%M:%S"))
        self.window.after(1000, self.atualizar)

    def window_sistema(self):
        self.janela_sistema = JanelaSistema()
        self.janela_sistema.run()

    def window_sistema2(self):
        self.janela_sistema2 = JanelaSistema2()
        self.janela_sistema2.run()

    def window_processos(self):
        self.janela_processos = JanelaProcessos()
        self.janela_processos.run()

    def window_memoria(self):
        self.janela_memoria = JanelaMemoria()
        self.janela_memoria.run()

    def window_arquivos(self):
        self.janela_arquivos = JanelaArquivo()
        self.janela_arquivos.run()

    def run(self):
        self.window.after(1000, self.atualizar)
        self.window.mainloop()

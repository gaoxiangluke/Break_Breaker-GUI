import tkinter as tk
import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image
import matplotlib.animation as animation
LARGE_FONT = ("Verdana", 12)
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from ArduinoUnoClass import Arduino
import threading
second = 0
AR1 = Arduino()
fig = Figure(figsize=(5,4), dpi=100)
ax1 = fig.add_subplot(111)
dataArray=[]
second = 0
start = time.time()
Quit = False
def animate(i):
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine) > 1:
            x = eachLine[0]
            y = eachLine[1]
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.plot(xar, yar)
class BBG(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageTwo):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    def task(self,second):
        Array = []
        Array = AR1.readData(0,False,True,True,False);
        if ( len(Array) > 0):
                dataArray.append([second,Array[0]])
        second=second+1;
        after(self,1000,self.task(second))
        #if time.time() - start > 1:
         #       start = time.time()
         #       second=second+1;


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # add baja image
        logo = tk.Label(self, width=300, height=300)
        img = ImageTk.PhotoImage(Image.open("logo.png"))
        logo.image = img
        logo.configure(image=img)
        logo.pack()
        # logo
        label = tk.Label(self, text="Break-Breaker GUI")
        label.pack(side="top", fill="both", expand=True)
        button = tk.Button(self, text="Start GUI",
                           command=lambda: controller.show_frame(PageTwo))
        button.pack(side="bottom", fill="both", expand=True)




class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        leftFrame = Frame(self, width=200, height=600)
        leftFrame.grid(row=0, column=0, padx=10, pady=2)
        tab_parent = ttk.Notebook(leftFrame)
        tab1 = ttk.Frame(tab_parent)
        tab2 = ttk.Frame(tab_parent)
        tab_parent.add(tab1, text="Speed")
        tab_parent.add(tab2, text="Temp")
        tab_parent.pack(expand=1, fill='both')
        last_inc = time.time()
        
       
       
        


        canvas = FigureCanvasTkAgg(fig, tab1)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, tab1)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect("key_press_event", on_key_press)

        def _quit():
            self.quit()  # stops mainloop
            self.destroy()  # this is necessary on Windows to prevent
            # Fatal Python Error: PyEval_RestoreThread: NULL tstate

        button = Button(tab1, text="Quit", command=_quit)

        # Right Frame and its contents
        rightFrame = Frame(self, width=200, height=600)
        rightFrame.grid(row=0, column=1, padx=10, pady=2)
        
        def MotorDisable():
            MotorBtn.configure(text="Turn on Motor", command=MotorEnable)
            AR1.sendInteger(2,True)
        def MotorEnable():
            MotorBtn.configure(text="Turn off Motor", command=MotorDisable)
            AR1.sendInteger(1,True)
        def SpeedLow():
            AR1.sendInteger(3,True)
        def Speedmed():
            AR1.sendInteger(3,True)
        def Speedhigh():
            AR1.sendInteger(3,True)
                
        btnFrame = Frame(rightFrame, width=200, height=200)
        btnFrame.grid(row=1, column=0, padx=10, pady=2)
        MotorBtn = Button(btnFrame, text="Turn on Motor", command=MotorEnable)
        MotorBtn.pack()
        StartBtn = Button(btnFrame, text="start system")
        StartBtn.pack()
        SpeedBtnFrame = Frame(btnFrame)
        HighSpeed = Button(btnFrame, text="High", command=Speedhigh)
        HighSpeed.pack(side=RIGHT)
        MedSpeed = Button(btnFrame, text="Medium", command=Speedmed)
        MedSpeed.pack(side=RIGHT)
        LowSpeed =  Button(btnFrame, text="Low", command=SpeedLow)
        LowSpeed.pack(side=RIGHT)
        SpeedBtnFrame.pack(side=TOP)
        LabelFrame = Frame(rightFrame)
        RPMIndicator = Label(LabelFrame,text = "RPM = 0")
        RPMIndicator.pack(side=TOP)
        TempIndicator = Label(LabelFrame,text = "temp = 0C")
        TempIndicator.pack(side=TOP)
        LoadIndicator = Label(LabelFrame,text = "Load = 0N")
        LoadIndicator.pack(side=TOP)
        LabelFrame.grid(row=2, column=0, padx=10, pady=2)
        
        
class myGui(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
                self.start()
        def callback(self):
                
                AR1.closeConn()
                self.app.quit()
                self.app.destroy()
                Quit = True
        def run(self):
                self.app = BBG()
                self.app.protocol("WM_DELETE_WINDOW",self.callback)
                ani = animation.FuncAnimation(fig,animate, interval=1000)
                self.app.mainloop()
appi = myGui()
while (Quit == False):
        Array = []
        Array = AR1.readData(0,False,True,True,False);
        if ( len(Array) > 0):
                dataArray.append([second,Array[0]])
        second=second+1;
        if time.time() - start > 0.25:
                start = time.time()
                second=second+1;
        

        
       

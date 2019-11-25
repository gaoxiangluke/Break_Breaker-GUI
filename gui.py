import tkinter as tk
import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image
from datetime import datetime
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
enableArduino = 1
testStrat = 1
if (enableArduino == 1):
    from ArduinoUnoClass import Arduino
import threading
second = 0
if (enableArduino == 1):
    AR1 = Arduino()
figTemp = Figure(figsize=(5,4), dpi=100)
ax1Temp = figTemp.add_subplot(111)
figPWM = Figure(figsize=(5,4), dpi=100)
ax1PWM = figPWM.add_subplot(111)
PWMArray=[]
TempArray=[]
LoadArray=[]
second = 0
start = time.time()
Quit = False
PwMNumber = ""
#PwMNumber.set("RPM = " + 0)
TempNumber = ""
#TempNumber.set("RPM = " + str(0) + "C")
LoadNumber = "load= " + str(0) + "N"
def animate(i):
   
    xar = []
    yar = []
    for eachLine in TempArray:
        if len(eachLine) > 1:
            if (enableArduino == 0):
                x,y = eachLine.split(',')
            else:
                x = eachLine[0]
                y = eachLine[1]
            xar.append(x)
            yar.append(y)
    ax1Temp.clear()
    ax1Temp.plot(xar, yar)  
    ax1Temp.set_ylim([0,100])                              
def animatePWM(i):
    xar = []
    yar = []
    for eachLine in PWMArray:
        if len(eachLine) > 1:
            if (enableArduino == 0):
                x,y = eachLine.split(',')
            else:
                x = eachLine[0]
                y = eachLine[1]
            xar.append(x)
            yar.append(y)
    ax1PWM.clear()
    ax1PWM.plot(xar, yar)
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





        
        canvas = FigureCanvasTkAgg(figTemp, tab2)  # A temp tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, tab2)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        canvas2 = FigureCanvasTkAgg(figPWM, tab1)  # A pwm tk.DrawingArea.
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        toolbar2 = NavigationToolbar2Tk(canvas2, tab1)
        toolbar2.update()
        canvas2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

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
            if (enableArduino == 1):
                AR1.sendInteger(2,True)
        def MotorEnable():
            MotorBtn.configure(text="Turn off Motor", command=MotorDisable)
            if (enableArduino == 1):
                AR1.sendInteger(1,True)
        def SpeedLow():
            if (enableArduino == 1):
                AR1.sendInteger(3,True)
        def Speedmed():
            if (enableArduino == 1):
                AR1.sendInteger(4,True)
        def Speedhigh():
            if (enableArduino == 1):
                AR1.sendInteger(5,True)
        def StoreData():
            now = datetime.now()
            dt_string = now.strftime("%dd_%mm_%YY_%HH_%MM_%SS")
            pushData =open(dt_string+"_temp.txt","w+")
            for i in TempArray:
                pushData.write(str(TempArray[0])+','+str(TempArray[1]))

        btnFrame = Frame(rightFrame, width=200, height=200)
        btnFrame.grid(row=1, column=0, padx=10, pady=2)
        MotorBtn = Button(btnFrame, text="Turn on Motor", command=MotorEnable)
        MotorBtn.pack()
        StartBtn = Button(btnFrame, text="start system")
        StartBtn.pack()
        SpeedBtnFrame = Frame(btnFrame)
        SpeedLabel=Label(btnFrame, text="Setting speed")
        SpeedLabel.pack()
        HighSpeed = Button(btnFrame, text="High", command=Speedhigh)
        HighSpeed.pack(side=RIGHT)
        MedSpeed = Button(btnFrame, text="Medium", command=Speedmed)
        MedSpeed.pack(side=RIGHT)
        LowSpeed =  Button(btnFrame, text="Low", command=SpeedLow)
        LowSpeed.pack(side=RIGHT)
        SpeedBtnFrame.pack(side=TOP)
        LabelFrame = Frame(rightFrame)
        RPMIndicator = Label(LabelFrame,text =   PwMNumber )
        RPMIndicator.pack(side=TOP)
        TempIndicator = Label(LabelFrame,text = TempNumber)
        TempIndicator.pack(side=TOP)
        LoadIndicator = Label(LabelFrame,text = LoadNumber)
        LoadIndicator.pack(side=TOP)
        LabelFrame.grid(row=2, column=0, padx=10, pady=2)

        DataButton = Button(rightFrame,text="StoreData",command=StoreData)
        DataButton.grid(row=3, column=0, padx=10, pady=2)
        extraButton = Button(rightFrame, text="Summon Danny")
        extraButton.grid(row=4, column=0, padx=10, pady=2)

class myGui(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.start()
        def callback(self):
            if (enableArduino == 1):
                AR1.closeConn()
            self.app.quit()
            self.app.destroy()
            Quit = True
        def run(self):
            self.app = BBG()
            self.app.protocol("WM_DELETE_WINDOW",self.callback)
            aniTemp = animation.FuncAnimation(figTemp,animate, interval=1000)
            aniPWM = animation.FuncAnimation(figPWM,animatePWM, interval=1000)
            self.app.mainloop()
appi = myGui()
i =0
while (Quit == False):
    Array = []
    if (enableArduino == 1):
        if (testStrat == 1):
            Array = AR1.readData(0,False,True,False,True)
            print(Array)
            if ( len(Array) > 0):
                if (Array[0]!="None"):
                    TempArray.append([second,Array[0]])
                second=second+1
            if time.time() - start > 0.25:
                start = time.time()
                second=second+1
       # PwMNumber.set("RPM = " + str(PWMArray[len(PWMArray)-1][1])
       # TempNumber.set("Temp = " + str(0) + "C")
       # LoadNumber = "load= " + y + "N"




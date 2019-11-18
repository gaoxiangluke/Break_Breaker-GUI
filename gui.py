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

fig = Figure(figsize=(5,4), dpi=100)
ax1 = fig.add_subplot(111)
def animate(i):
    pullData = open("sampleText.txt", "r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
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

        def MotorEnable():
            MotorBtn.configure(text="Turn off Motor", command=MotorDisable)

        btnFrame = Frame(rightFrame, width=200, height=200)
        btnFrame.grid(row=1, column=0, padx=10, pady=2)
        MotorBtn = Button(btnFrame, text="Turn on Motor", command=MotorEnable)
        MotorBtn.pack()
        StartBtn = Button(btnFrame, text="start system")
        StartBtn.pack()


app = BBG()
ani = animation.FuncAnimation(fig,animate, interval=1000)
app.mainloop()
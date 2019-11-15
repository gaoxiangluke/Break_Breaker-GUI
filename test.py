import tkinter 
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
master = Tk() 
leftFrame = Frame(master, width=200, height = 600)
leftFrame.grid(row=0, column=0, padx=10, pady=2)
tab_parent = ttk.Notebook(leftFrame)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="Speed")
tab_parent.add(tab2, text="Temp")
tab_parent.pack(expand=1, fill='both')
fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

canvas = FigureCanvasTkAgg(fig, tab1)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, tab1)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=tab1, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

#Right Frame and its contents
rightFrame = Frame(master, width=200, height = 600)
rightFrame.grid(row=0, column=1, padx=10, pady=2)
def MotorDisable():
    MotorBtn.configure(text="Turn on Motor",command = MotorEnable)    
def MotorEnable():
    MotorBtn.configure(text="Turn off Motor",command = MotorDisable)
btnFrame = Frame(rightFrame, width=200, height = 200)
btnFrame.grid(row=1, column=0, padx=10, pady=2)
MotorBtn = Button(btnFrame, text="Turn on Motor",command = MotorEnable)
MotorBtn.pack()
StartBtn = Button(btnFrame, text="start system")
StartBtn.pack()



tkinter.mainloop()



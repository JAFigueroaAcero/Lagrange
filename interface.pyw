import tkinter as tk

from tkinter import *
from tkinter import ttk

from os.path import isfile, isdir, dirname, join,realpath
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ad():
    def __init__(self,parent,title,text):
        self.root= tk.Toplevel(parent.root)
        self.root.resizable(0,0)
        self.root.geometry('240x100')
        self.root.title(title)
        self.root.iconbitmap(join(join(dirname(realpath(__file__)),'assets'), 'logo.ico'))
        
        self.a1 = Frame(self.root, width=200, height=100)
        self.a1l = Label(self.a1, text=text, anchor="center")
        self.a1l.grid(row=1,column=0, pady=10)
        self.b1 = Button(self.a1, width=3, height=1 ,text='Ok', command= self.root.destroy)
        self.b1.grid(row=3,column=0, sticky='nsew')
        self.a1.pack()
        self.root.transient(parent.root)
        self.root.mainloop()

class main():
    def __init__(self):
        matplotlib.use('TkAgg')
        self.root = tk.Tk()
        self.root.resizable(0,0)
        self.root.title('Gravity simulator')
        #self.root.iconbitmap(join(join(dirname(realpath(__file__)),'assets'), 'logo.ico'))
        
        self.a1 = Frame(self.root)
        self.a1.grid(row=0, column=0, sticky='nsew', pady=10)

        self.a2 = Frame(self.root)
        self.a2.grid(row=1, column=0, sticky='W')

        var = StringVar()
        var.trace("w", lambda name, index,mode, var=var: callback(var))

        Label(self.a1, text = 'Lagrangian:').grid(row=0,column=0)
        self.gen = Entry(self.a1,textvariable=var,  width=30)
        self.gen.grid(row=0, column=1)

        Label(self.a2, text = 'vars:').grid(row=0,column=0)

        self.entries = []   
        def clear():
            wx.clear()
            canvas.draw()
            self.gen.delete(0,"end")


        def callback(var):
            try:
                # Get the Entry Input
                tmptext = var.get()
                tmptext = "$"+tmptext+"$"
                # Clear any previous Syntax from the figure
                wx.clear()
                if tmptext != '$$':
                    wx.text(0.01, 0.5, tmptext, fontsize = 10)
                else:
                    wx.text(0.01, 0.5, '', fontsize = 10)
                canvas.draw()
            except:
                pass
        def create():
            if len(self.entries) < 19:
                self.entries.append(Entry(self.a2,width=2))
                self.entries[-1].grid(row=0, column = 2+len(self.entries))

        def remove():
            if len(self.entries) >= 1:
                self.entries.pop(-1).grid_remove()

        label = Label(self.a1,width=10,height=10)
        label.grid(row=0,column=2, pady=5)
        fig = matplotlib.figure.Figure(figsize=(5, 0.5), dpi=100)
        wx = fig.add_subplot(111)
        rgb = tuple(((c//256)/256 for c in self.root.winfo_rgb(self.root.cget('bg'))))
        fig.patch.set_facecolor(rgb)
        canvas = FigureCanvasTkAgg(fig, master=label)
        canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5)
        canvas._tkcanvas.grid(row=0, column=0, padx=5, pady=5)

        # Set the visibility of the Canvas figure
        wx.get_xaxis().set_visible(False)
        wx.get_yaxis().set_visible(False)

        self.b1 = Button(self.a1, text = 'Clear', width=6,padx=5,pady=0, command = lambda: clear())
        self.b1.grid(row=0, column = 3, sticky = 'E')

        self.b2 = Button(self.a2, text = 'Add', width=6,padx=5,pady=0, command = lambda: create())
        self.b2.grid(row = 0, column =1,sticky = 'E',padx=5, pady=5)

        self.b3 = Button(self.a2, text = 'Remove', width=6,padx=5,pady=0, command = lambda: remove())
        self.b3.grid(row = 0, column =2,sticky = 'E',padx=5, pady=5)

        self.root.mainloop()


if __name__ == "__main__":
    main()

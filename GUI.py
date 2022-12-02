# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:34:50 2022

@author: Andrew
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import *
from tkinter.messagebox import showinfo
import MACCOR_Process as pro
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk)


root = tk.Tk()
root.title('Echem Plotter')
root.geometry('300x200')

def browseandplot():
    
    selectfile = fd.askopenfilename(title='Open file', initialdir='/',\
                                    filetype=(('Excel files',('.*xlsx','*.xls')),\
                                              ('All files','*.')))
    label = Label(root,text=f'Currnet File: {selectfile}')
    label.pack(anchor=tk.N)
    
    actmass= tk.simpledialog.askfloat('ATTENTION','Enter active mass g: \t\t    ') #Do not delete spaces
    
    process = pro.main(selectfile,actmass)
    
    plot = pro.plot_echem(process)
    
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(plot,root)
    
    # placing the canvas on the Tkinter window
    
    #canvas.get_tk_widget().pack(side=tk.BOTTOM,expand=True)
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,root)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget(expand=True).pack()
    

browse_button = ttk.Button(root,text='Browse & Plot',command=browseandplot)
browse_button.pack(expand=True)



root.mainloop()
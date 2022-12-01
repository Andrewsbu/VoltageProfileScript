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


root = tk.Tk()
root.title('Echem Plotter')
root.geometry('800x600')

def browsefile():
    
    selectfile = fd.askopenfilename(title='Open file', initialdir='/',\
                                    filetype=(('Excel files',('.*xlsx','*.xls')),\
                                              ('All files','*.')))
    label = Label(root,text=f'Currnet File: {selectfile}')
    label.pack(anchor=tk.N)
    
browse_button = ttk.Button(root,text='Browser',command=browsefile)
browse_button.pack(expand=True)










root.mainloop()
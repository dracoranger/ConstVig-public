import tkinter as tk
from tkinter import ttk

import urllib
import json


def popup(msg):
    popup = tk.Tk()
    title_bar = tk.Frame(popup, bg="blue", relief="raised", bd=2)
    popup.wm_title("Attack Launch Count")
    popup.configure(background="blue")
    label = ttk.Label(popup, text=msg, font=("Verdana", 64), background="blue", foreground="white")
    label.pack(side="top", fill="x", padx=220, pady=220)
    B1 = ttk.Button(popup, text="Refresh", command=popup.destroy)
    B1.pack()
    popup.after(45000, lambda: popup.destroy())
    popup.mainloop()

run = True

while(run):
    f = open('mixed.log', 'r')
    counter = 0
    while f.readline() != '':
        counter +=1
    total = str(counter)+" attacks just launched!"
    popup(total)

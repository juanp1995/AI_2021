#!/usr/bin/env python3
from tkinter import *
from functools import partial
from itertools import product

# produce the set of coordinates of the buttons
positions = product(range(10), range(10))
buttonIds = []

def changeBtnColor(i):
    bname = (buttonIds[i])
    if bname.cget('bg') == 'black':
        bname.configure(bg='white')
    else:
        bname.configure(bg='black')

win = Tk()
frame = Frame(win)
frame.pack()

win.minsize(width=480, height=360)
win.title("Retina")

for i in range(10):
    # shape the grid
    setsize = Canvas(frame, width=30, height=0).grid(row=11, column=i)
    setsize = Canvas(frame, width=0, height=30).grid(row=i, column=11)

for i, item in enumerate(positions):
    button = Button(frame, bg='white', command=partial(changeBtnColor, i))
    button.grid(row=item[0], column=item[1], sticky="n,e,s,w")
    buttonIds.append(button)


win.mainloop()

from tkinter import *
import tkinter.scrolledtext as tkst

def writeInp():
    setBox(e.get())

def setBox(txt):
    box.config(state=NORMAL)
    box.delete(1.0,END)
    box.insert(INSERT, txt)
    box.config(state=DISABLED)
    
master = Tk()

Label(master,text="Enter kanji").grid(row=0,column=0)

e= Entry(master)
e.grid(row=0,column=1)

Button(master, text='go', command=writeInp).grid(row=0, column=2)
Button(master, text='quit',command=exit).grid(row=0,column=3)

box = tkst.ScrolledText(master,height=10,width=50,state=DISABLED)
box.grid(row=1,column=0,columnspan=4)

setBox('Loading dcitionatiy')

master.mainloop()

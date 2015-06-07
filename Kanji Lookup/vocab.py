import xml.etree.ElementTree as et
import codecs
import sys
import time
from tkinter import *
import tkinter.scrolledtext as tkst

initialized = False

def writeInp():
    s = e.get()
    if len(s)!=1: setBox('Please enter a single character')
    else:
        stop=True
        getKanjiWords(s)

def setBox(txt):
    box.config(state=NORMAL)
    box.delete(1.0,END)
    box.insert(INSERT, txt)
    box.config(state=DISABLED)
    master.update()

def insBox(txt):
    box.config(state=NORMAL)
    box.insert(END,txt)
    box.config(state=DISABLED)
    master.update()

def readDict(result):
    out=''
    out+=result.find(".k_ele/keb").text+'; '
    
    first=True
    for i in result.findall("./r_ele/reb"):
        if not first:
            out+=', '
        else:
            first= False
        out+=i.text
    out+='; '
    
    first=True    
    for i in result.findall("./sense/gloss"):
        if not first:
            out+=',　'
        else:
            first=False
        out+=i.text
    out+=';\n'
    return out

stop = False
def getKanjiWords(char):
    global stop
    stop = False
    setBox('')
    i=0
    for w in k:
        i+=1
        if stop: break 
        for c in w:
            if char == c:
                insBox(d.get(w))

def quit():
    stop=True
    exit()
    
master = Tk()
master.geometry("600x400")
master.wm_title("Example word finder")
master.protocol("WM_DELETE_WINDOW",exit)

frame = Frame(master)
frame.pack(side=TOP,anchor='nw')

Label(frame,text="Enter kanji").grid(row=0,column=0)

eText = StringVar()
e= Entry(frame,textvariable=eText)
e.grid(row=0,column=1)

Button(frame, text='go', command=writeInp).grid(row=0, column=2)
Button(frame, text='quit',command=quit).grid(row=0,column=3)

checkState = IntVar()
Checkbutton(frame, text='automatically copy from clipboard', variable=checkState).grid(row=0,column=4)

box = tkst.ScrolledText(master,height=1000,width=150,state=DISABLED)
box.pack(side=BOTTOM, fill=BOTH)

setBox('Loading dictionary')

tree = et.parse('JMdict_e.xml')

root = tree.getroot()

setBox('Indexing dictionary')

dictInit = []
for child in root:
    keb = child.find(".k_ele/keb")
    if keb != None:
        dictInit.append((keb.text,readDict(child)))
d = dict(dictInit)
k = d.keys()

setBox('Dictionary loaded. Please enter a kanji')

clipBoardVal = ""
def clipboardLoop():
    global clipBoardVal
    if checkState.get():
        try:
            s = master.clipboard_get()
            if len(s) == 1 and s!=clipBoardVal:
                eText.set(s)
                writeInp()
            clipBoardVal = s
        except Exception as err:
            print('Error in copying clipboard:',err)
    
    master.after(100,clipboardLoop)

clipboardLoop()

master.mainloop()

import xml.etree.ElementTree as et
import codecs
import sys
import time
from tkinter import *
import tkinter.scrolledtext as tkst

def writeInp():
    s = e.get()
    if len(s)!=1: setBox('Please enter a single character')
    else: getKanjiWords(s)

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
    
master = Tk()
master.geometry("600x400")

frame = Frame(master)
frame.pack(side=TOP,anchor='nw')

Label(frame,text="Enter kanji").grid(row=0,column=0)

e= Entry(frame)
e.grid(row=0,column=1)

Button(frame, text='go', command=writeInp).grid(row=0, column=2)
Button(frame, text='quit',command=exit).grid(row=0,column=3)

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
        dictInit.append((keb.text,child))

d = dict(dictInit)
k = d.keys()

setBox('Dictionary loaded. Please enter a kanji')

def getWord(word):
    result = d.get(word)
    insBox(word+'; ')
    
    first=True
    for i in result.findall("./r_ele/reb"):
        if not first:
            insBox(', ')
        else:
            first= False
        insBox(i.text)
    insBox('; ')
    
    first=True    
    for i in result.findall("./sense/gloss"):
        if not first:
            insBox(',　')
        else:
            first=False
        insBox(i.text)
    insBox(';\n')
    
def getKanjiWords(char):
    wordList=[]
    for w in k:
        for c in w:
            if char == c:
                wordList.append(w)

    l=len(wordList)
    if l == 0: setBox('No matching words found')
    else:
        setBox('')
        for word in wordList:
            getWord(word)

master.mainloop()
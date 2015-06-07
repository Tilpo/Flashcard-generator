import xml.etree.ElementTree as et
import codecs
import sys
import time
from tkinter import *
import tkinter.font as tkf

def writeInp():
    s = e.get()
    if len(s)!=1: setBox('Please enter a single character')
    else:
        stop=True
        getKanjiWords(s)

def setBox(txt):
    # box.config(state=NORMAL)
    box.delete(0,END)
    if txt!='':
        box.insert(END, txt)
    # box.config(state=DISABLED)

def insBox(txt):
    # box.config(state=NORMAL)
    box.insert(END,txt)
    # box.config(state=DISABLED)

def readDict(result):
    out=''
    out+=result.find(".k_ele/keb").text+';  '
    
    first=True
    for i in result.findall("./r_ele/reb"):
        if not first:
            out+=', '
        else:
            first= False
        out+=i.text
    out+=';  '
    
    first=True    
    for i in result.findall("./sense/gloss"):
        if not first:
            out+=',　'
        else:
            first=False
        out+=i.text
    return out

stop = False
def getKanjiWords(char):
    global stop
    stop = False
    setBox('')
    master.wm_title('Looking up words')
    i=0
    for w in k: #for all the words in the list of keys
        i+=1
        if stop: break 
        for c in w:
            if char == c:
                insBox(d.get(w))
    master.wm_title('Done!')

def quit():
    stop=True
    exit()
    
master = Tk()
master.geometry("1280x1024")
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
checkState.set(1)
Checkbutton(frame, text='automatically copy from clipboard', variable=checkState).grid(row=0,column=4)

listFrame = Frame(master)
listFrame.pack(side=BOTTOM, fill=BOTH)

boxFont = tkf.Font(family='TkDefaultFont',size='11')

yScroll=Scrollbar(listFrame, orient=VERTICAL)
yScroll.pack(side=RIGHT,fill=Y)
xScroll = Scrollbar(listFrame, orient=HORIZONTAL)
xScroll.pack(side=BOTTOM,fill=X)

box = Listbox(listFrame,width=10,height=1000,
              selectmode=EXTENDED,font=boxFont,activestyle='none',selectborderwidth=2,
              xscrollcommand=xScroll.set, yscrollcommand=yScroll.set
)
box.pack(side=TOP,fill=BOTH)
xScroll['command']=box.xview
yScroll['command']=box.yview



master.wm_title('Loading dictionary')

tree = et.parse('JMdict_e.xml')

root = tree.getroot()

master.wm_title('Indexing dictionary')

dictInit = []
for child in root:
    keb = child.find(".k_ele/keb")
    if keb != None:
        dictInit.append((keb.text,readDict(child)))
d = dict(dictInit)
k = d.keys()

master.wm_title('Dictionary loaded. Please enter a kanji')

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

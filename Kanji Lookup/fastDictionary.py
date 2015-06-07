import xml.etree.ElementTree as et
import codecs
import time as t

tree = et.parse('JMdict_e.xml')
root = tree.getroot()

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

dictInit = []
for child in root:
    keb = child.find(".k_ele/keb")
    if keb != None:
        dictInit.append((keb.text,readDict(child)))

d = dict(dictInit)
k = d.keys()

char='日'

t1=t.time()

wordList=[]
for w in k:
    for c in w:
        if char == c:
            wordList.append(w)

print(len(wordList))            
print(t.time()-t1)

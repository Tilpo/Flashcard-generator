import xml.etree.ElementTree as ET
import codecs
import sys
import time

print('Loading dictionary...')
tree = ET.parse('JMdict_e.xml')
root = tree.getroot()

print('Dictionary loaded. Loading word list...')

output = open('vocab_out.txt','w',encoding='utf-8')
err = open('errors.txt','w',encoding='utf-8')
errNum = 0

def getWord(word):
    global errNum

    result = None
    for child in root:
        keb = child.find('./k_ele/keb')
        if keb!=None and keb.text == word:
            result = child
            hasKanji=True
            break
            
    if result == None:
        for child in root:
            reb = child.find('./r_ele/reb')
            if reb!=None and reb.text == word:
                result = child
                hasKanji = False
                break
         
    if result == None:
        err.write('Could not find: '+word+'\n')
        errNum+=1
        return
    
    if hasKanji: output.write(result.find("./k_ele/keb").text+'; ')
    else: output.write(result.find("./r_ele/reb").text+'; ')
    
    j=0
    for i in result.findall("./r_ele/reb"):
        if j: output.write(', ')
        j+=1
        output.write(i.text)
    output.write('; ')
    j=0
        
    for i in result.findall("./sense/gloss"):
        if j: output.write(', ')
        j+=1
        output.write(i.text)
    output.write(';\n')
        
input = open('vocab.txt',encoding='utf-8')
wordList =[]
for line in input:
    if len(line)>1: wordList.append(line)
l=len(wordList)
print('Word list loaded. Parsing',l,'words.')
i=1
for word in wordList:
    getWord(word[:-1])
    print(str(i)+'/'+str(l),'words done.')
    i+=1
    
output.close()
err.close()
input.close()

if errNum == 0: print('Done! Process finished without errors')
else: print('Done! Encountered',errNum,'error(s).')

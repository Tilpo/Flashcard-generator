#this file looks up a entry in a kanji dictionary
import xml.etree.ElementTree as ET
import codecs
import sys
import time

tree = ET.parse('kanjidic2.xml')
root = tree.getroot() #get the entire tree going on

output = open('output.txt','w',encoding='utf-8')



allChars = root.findall("./character/literal") #find all the character elements in the XML file

cl = [] #make a list of strings of all these characters
for child in allChars:
	cl.append(child.text)

def find_char(char):
	for c in range(len(cl)):
		if cl[c] == char:
			return(c)
			break
	else:
		return(-1)

elem = root[find_char("盛")+1]
onyomi = elem.findall(".reading_meaning/rmgroup/reading[@r_type='ja_on']")
for child in onyomi:
	output.write(child.text+", ")
output.write("\n")

kunyomi = elem.findall(".reading_meaning/rmgroup/reading[@r_type='ja_kun']")
for child in kunyomi:
	output.write(child.text+", ")
	
output.write("\n All the words! \n")

#now we're going to load the vocabulary dictionary and for a given kanji, we will find all the words that only consist of allowed characters!
voc = ET.parse("JMdict_e.xml").getroot()
legalCharList = open('kanjiList.txt','r',encoding='utf-8')
legalChars = legalCharList.read()
legalCharList.close()

char = "制"
wordList = []
for child in voc: #find all the words that contain the character
	keb = child.find(".k_ele/keb")
	if keb != None:
		for c in keb.text:
			if c == char:
				wordList.append(child)
				break
def is_legal(char):
	for j in legalChars:
		if char == j:
			return True
	else:
		return False

wordList2=[]		
for child in wordList: #remove the words that have an unallowed character
	keb = child.find(".k_ele/keb").text
	legal = True
	for i in keb:
		if not is_legal(i):
			legal = False
	if legal:
		wordList2.append(child)
		output.write(keb+", ")

output.close()
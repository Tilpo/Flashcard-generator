#this file makes a list of all the kanji that are N2, let's say
import xml.etree.ElementTree as ET
import codecs
import sys
import time

tree = ET.parse('kanjidic2.xml')
root = tree.getroot() #get the entire tree going on

output = open('kanjiList.txt','w',encoding='utf-8')

for child in root: #iterate over all the children in the root
	grade = child.find("./misc/grade") #get the grade
	grd = 0
	if grade != None: #if the grade is not empty, save its value
		grd = int(grade.text) 
	if grd > 0 and grd <= 8:
		char = child.find("./literal") #if the grade is in the right range, obtain the string of the kanji and write it to file
		if char != None:
			output.write(char.text)

allowedChars= u'ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖ゙゚゜ァアィイゥウェエォオカガキギクグケゲコゴサザム々メモャヰヱヾヲゞンゝヴ〃仝ヵヶ・ーヽヾヤュユョヨラリルレロヮワシジスバパヒビピフブプヘベペホボポマミズセゼソゾタダチヂッツヅテデトドナニヌネノハ'
output.write(allowedChars)
output.close()
import time,sys,os,re
from docx import Document
from docx.shared import Inches

document = Document()
#fileQues = open("itemQues0.txt", "r")
fileQues = open("itemAnws0.txt", "r")

oneDayQues = ''
linesInfo = {}

i = 0
for line in fileQues:    
    if(line.startswith('full')):
        datimeInfo = re.search('(\d+.\d+)', oneDayQues)
        if(datimeInfo and datimeInfo.group(1)):
            linesInfo[datimeInfo.group(1)] = [oneDayQues, line]
        i += 1   
    elif(len(line) > 20):
        oneDayQues = line.decode('utf8')
        
index = 1
#for key in sorted(linesInfo.iterkeys()):
for i in range(1, 13):
    for j in range(1, 32):
        key = '%d.%d' % (i, j)
        if (key in linesInfo.keys()):
            txtLine = linesInfo[key][0]
            imgLine = linesInfo[key][1]
            document.add_heading(str(index) + " -- " + txtLine, level=4)  
            document.add_picture(imgLine[:-1],  width=Inches(6.0))    
            index += 1
      
document.save('ynjAoshuAnswer.docx')    

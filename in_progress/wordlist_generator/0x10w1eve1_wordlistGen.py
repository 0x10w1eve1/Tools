import sys


'''

TO DO: 

1) argparse integration
2) requitements.txt for packages
3) parse argparse infile to see filetype, if not filetype asssume its .txt. show this default in usage
4) depending on filetype from above, call prinpdfmeta.py or docx. maybe just put it all in this script. make it classY
5) for docx either use this:https://github.com/badbye/docxpy or modify your assessments logic to include headers and tables, make a test docx file to make sure you get all text from a table, header etc. 


import PyPDF2

import argparse


def printMeta(parser):
	docInfo = parser.getDocumentInfo()
	print('[*] PDF Metadata for: ' + str(parser))
	for metaItem in docInfo:
		print('[+] ' + metaItem + ':' + docInfo[metaItem])

def getWords(parser):
	pagenum=parser.numPages
	page=parser.getPage(1)
	for i in range(pagenum):
		try:
			text+=page.extractText()
		except:
			continue
	return text

	
def main():
	myparser = argparse.ArgumentParser(usage='python printmeta.py -F <filename>')
	myparser.add_argument('-F',dest='file',help='specify filename')
	myargs = myparser.parse_args()
	if myargs.file == None:
		print(myparser.usage)
	else:
		mypdf=open(myargs.file,'rb')
		parser = PyPDF2.PdfFileReader(mypdf)
		words=getWords(parser)




		
if __name__ == '__main__':
	main()




'''



Usage = " ### 0x10w1evee1 ### \nUsage: %s infile outfile "%sys.argv[0]
if len(sys.argv) !=3:
	print Usage
	sys.exit()
badchars = [',','.',':']
newwordlist = open(sys.argv[2],'w')
with open(sys.argv[1],'rb') as email:
	for line in email:
		for word in line.split():
			for ch in badchars:
				if ch in word:
					word = word.replace(ch,'')
			
			newwordlist.write(word+'\n')
			





### 0x10w1eve1 ###

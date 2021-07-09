#!/usr/bin/env python3
######
###
'''

TO DO: 

1) argparse integration
2) requitements.txt for packages
3) parse argparse infile to see filetype, if not filetype asssume its .txt. show this default in usage
4) depending on filetype from above, call prinpdfmeta.py or docx. maybe just put it all in this script. make it classY
<<<<<<< HEAD
5) for docx either use this:https://github.com/badbye/docxpy or modify your assessments logic to include headers and tables, make a test docx file to make sure you get all text from a table, header etc. 
=======
5) for docx either use this:https://github.com/badbye/docxpy or modify your word doc parser logic to include headers and tables, make a test docx file to make sure you get all text from a table, header etc. 
>>>>>>> fb2867c80b380f3895850ab896a55106bace510d
6) go through all scripts in git/wordlistedit and see if you can incorporate/use anything. 
######
####
'''

import PyPDF2
import sys
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

	




myparser = argparse.ArgumentParser()
myparser.add_argument('infile',help='file to parse')
myparser.add_argument('outfile', metavar="outfile", default="10w1eve1_wordlist.txt", help='new wordlist filename')
myparser.add_argument('-x', metavar="ext",choices=['pdf','txt','doc','html','xml'], help='extension of input file, if cannot detect, txt') 

myparser.parse_args()

if not myargs.infile:
	print(myparser.print_help())
	parser.exit()
else:
	pass


'''


		mypdf=open(myargs.file,'rb')
		parser = PyPDF2.PdfFileReader(mypdf)
		words=getWords(parser)


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
'''
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


### 0x10w1eve1 ###

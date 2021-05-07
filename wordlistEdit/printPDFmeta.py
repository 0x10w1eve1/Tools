import pyPdf
from pyPdf import PdfFileReader
import argparse


def printMeta(fileName):
	pdfile = PdfFileReader(file(fileName,'rb'))
	docInfo = pdfile.getDocumentInfo()
	print '[*] PDF Metadata for: ' + str(fileName)
	for metaItem in docInfo:
		print '[+] ' + metaItem + ':' + docInfo[metaItem]

def main():
	myparser = argparse.ArgumentParser(usage='python printmeta.py -F <filename>')
	myparser.add_argument('-F',dest='file',help='specify filename')
	myargs = myparser.parse_args()
	if myargs.file == None:
		print myparser.usage
	else:
		filename = myargs.file
		printMeta(filename)
if __name__ == '__main__':
	main()


### 0x10w1eve1 ###

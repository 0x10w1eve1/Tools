import zipfile
import argparse
import sys


def extractFile(filename,password):
	print 'Trying password: %s\n' %password
	try:		
		filename.extractall(pwd=password)
		print "Successfully Cracked=====> " +password+ '\n'		
		sys.exit()
	except Exception, e:
		return




def main():
	
	parser = argparse.ArgumentParser(usage='zipcrack.py -f <zipfile> -d <dictionary>')
	parser.add_argument('-f', dest='zname',help='specify zip file path')
	parser.add_argument('-d', dest='dname',help='specify dictionary file path')
	args = parser.parse_args()
	if (args.zname == None) | (args.dname == None):
		print parser.usage
		exit()
	else:
		zname = args.zname
		dname = args.dname

	zFile = zipfile.ZipFile(zname)
	dict = open(dname)

	print 'Cracking zip....'
	for line in dict.readlines():
		password = line.strip('\n')
		extractFile(zFile,password)

if __name__ == '__main__':
	main()

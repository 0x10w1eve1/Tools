import sys

if len(sys.argv) != 3:
	print 'Usage: python findword.py <file-to-search> <word-to-find>'
	sys.exit()


file = sys.argv[1]
word = sys.argv[2]
wc = 0

try:
	dik = open(file,'r')
except Exception,e:
	print e

for w in dik.readlines():
	wc +=1
	if w.rstrip('\n') == word:
		print 'Found Word. Word Count= %s'%wc



import hashlib
import sys

if len(sys.argv)!=3:
	print '[!] Usage: Python md5passcrack.py passhash wordlist\n\n'
	sys.exit()

tocrack = sys.argv[1]
wordlist = sys.argv[2]

with open(wordlist,'r') as f:
	for word in f.readlines():
		testhash = hashlib.md5(word.strip()).hexdigest()
		if tocrack==testhash:
			print '[+] Password ===> %s'%word
			sys.exit()

	print '[!] Password NOT FOUND...try different wordlist'




### 0x10w1eve1 ###

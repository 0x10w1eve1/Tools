#!/usr/bin/python3
import sys
# wrote this to remove duplciates after directory scanning.
if len(sys.argv) != 3:
	print(' [!] input file must be line separated.')
	print('\n\n\t\t\t0x10w1eve1\n\n\tUsage: %s <infile> <outfile>'%sys.argv[0])
	
	sys.exit()

nodups = []
infile = sys.argv[1]
outfile = sys.argv[2]
inwc = 0
outwc = 0

print('[*] Opening file to read....')
readfile = open(infile,'r')
print('[*] Sorting duplicates....')
for i in readfile.readlines():
	inwc +=1
	if i not in nodups:
		nodups.append(i)
		outwc +=1
print('[*] Writing new file....')
writefile = open(outfile,'w')
for i in nodups:
	writefile.write(i)
print('[!] Complete.')
print('[+] Original file size: ' + str(inwc) + '\n')
print('[+] New file size: ' + str(outwc))



### 0x10w1eve1 ###

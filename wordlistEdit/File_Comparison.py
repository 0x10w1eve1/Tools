import sys
#compare 2 files and write new file with no duplicates.
if len(sys.argv) != 4:
	print 'Usage: %s <infile1> <infile2> <outfile>' %sys.argv[0]
	sys.exit()

port80 = []
infile = sys.argv[1]
infile2 = sys.argv[2]
outfile = sys.argv[3]
notscanned = []


print '[*] Opening files to read....'
readfile = open(infile,'r')
readfile2 = open(infile2,'r')

#put all port 80's into a list
for i in readfile.readlines():
	port80.append(i)


print '[*] Comparing IPs ....'
for i in readfile2.readlines():
	if i not in port80:
		notscanned.append(i)


print '[*] Writing new file....'
writefile = open(outfile,'w')
for i in notscanned:
	writefile.write(i)
print '[!] Complete.'




### 0x10w1eve1 ###

import sys
#compare 2 files and write new file with no duplicates.
if len(sys.argv) != 4:
	print ' ### 0x10w1eve1 ### \n Usage: %s <infile1> <infile2> <outfile>' %sys.argv[0]
	sys.exit()

def Addnodups(nodupsarr,entry,count):
	nodupsarr.append(entry)
	return count+1


nodups = []
infile = sys.argv[1]
infile2 = sys.argv[2]
outfile = sys.argv[3]


infilewc = 0
infile2wc = 0
outwc = 0
print '[*] Opening files to read....'
readfile = open(infile,'r')
readfile2 = open(infile2,'r')

print '[*] Comparing Entries ....'
for i in readfile.readlines():
	outwc=Addnodups(nodups,i,outwc)
	infilewc+=1

for i in readfile2.readlines():
	infile2wc+=1
	if i not in nodups:
		outwc=Addnodups(nodups,i,outwc)


print '[*] Writing no duplicate file....'
writefile = open(outfile,'w')
for i in nodups:
	writefile.write(i)
print '[!] Complete.'

print '[+] Stats:\n File1 size: %s \n File2 size: %s \n NewFile size: %s'%(infilewc,infile2wc,outwc)




### 0x10w1eve1 ###

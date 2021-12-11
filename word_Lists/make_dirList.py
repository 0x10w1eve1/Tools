import sys


if len(sys.argv) != 3:
	print("### grep out https:// from  a file of urls, then use this script to parse/make a wordlist out of all the dirs in your url file")
	print('\n Usage: %s <targetfile> <outfile>\n'%sys.argv[0])
	sys.exit(1)

targetfile=sys.argv[1]
outfile=sys.argv[2]

## open target file and outfile
print("[+] Opening Files...")
try:
	dirfile=open(targetfile,'r')
	new_dirwordlist=open(outfile,'w')
except Exception as e:
	print("[!][!][!] ERROR [!][!][!]\n%s"%e)
	sys.exit(1)


dirList=[]
print("[+] Parsing Target File...")
#split links into array
for i in dirfile:
	tempdirList=i.split("/")
	for i in tempdirList:
		dirList.append(i.strip())
#remove all empty items
dirList = ' '.join(dirList).split()

#keep count of file write
nodups=[]
targetcount = len(dirList)
currcount = 0 
print("[+] Removing Duplicates...")
#remove duplicates
for i in dirList:
	if i not in nodups:
		nodups.append(i)
dirList=nodups

print("[+] Writing File...\n")
#write to file
for i in dirList:
	currcount+=1
	print("[*] Writing #%s/%s"%(currcount,targetcount))
	new_dirwordlist.write(i+"\n")

dirfile.close()
new_dirwordlist.close()


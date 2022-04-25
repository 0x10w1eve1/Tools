import sys
# wrote this to remove duplciates after directory scanning.
if len(sys.argv) != 3:
	print(" Usage: #scenario::  file1 is scanned ips, file2 is all target ips. get list of ips you still needa scan")
	print('\n %s <file1 -scanned file> <file2-all targets>'%sys.argv[0])
	sys.exit()


#check if ips in file 2, are in file 1, if they arent, print them out. 
#scenario::  file1 is scanned ips, file2 is all target ips. get list of ips you still needa scan
file1 = sys.argv[1]
file2 = sys.argv[2]


print('[*] Opening files to read....')
readfile1 = open(file1,'r')
readfile2 = open(file2,'r')

print("[*] parsing docs..")

for f2 in readfile2.readlines():

	if f2 not in readfile1.read():
		print(f2)


readfile1.close()
readfile2.close()
print("[*] Done...")




### 0x10w1eve1 ###

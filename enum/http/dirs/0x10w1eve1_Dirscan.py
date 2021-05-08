import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys


Usage = " ### 0x10w1evee1 ### \n Directory scanner for pages with a custom 404 page giving a http 200 \n\n Usage: %s <target> <wordlist>\n\ttarget = protocol://site \n"%sys.argv[0]
if len(sys.argv) !=3:
	print Usage
	sys.exit()

		
def write_results(foundDirs,notfound,checkme,falsepositive):
	logfile = open('Dirscan_results','w')
	logfile.write('[0x31 0x30 0x77 0x31 0x65 0x76 0x65 0x31]\n\n')
	logfile.write('~~~~~~~~~~~~~~ These Exist ~~~~~~~~~~~~~~\n\n')
	if foundDirs:
		for i in foundDirs:
			logfile.write(i)
	else:
		logfile.write('None\n')
	logfile.write(separator)
	'''
	logfile.write('~~~~~~~~~~~~~~ These Dont ~~~~~~~~~~~~~~\n\n')
	if notfound:
		for i in notfound:
			logfile.write(i)
	else:
		logfile.write('None\n')
	logfile.write(separator)
	'''
	logfile.write('~~~~~~~~~ Check These Manually ~~~~~~~~~\n\n')
	if checkme:
		for i in checkme:
			logfile.write(i)
	else:
		logfile.write('None\n')
	logfile.write(separator)
	logfile.write('~~~~~~~~~ Custom 404 Page ~~~~~~~~~\n\n')
	if falsepositive:
		for i in falsepositive:
			logfile.write(i)
	else:
		logfile.write('None\n')
	logfile.write(separator)
	logfile.write('\n[0x31 0x30 0x77 0x31 0x65 0x76 0x65 0x31]\n\n')	



### CHANGE these vars accordingly

failCase='404 Error'
proxy = {"https":"http://127.0.0.1:8080"}
OPTIONAL_HEADERS={
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}
### 

target=sys.argv[1]+"/"
dirlist=open(sys.argv[2],'r')
wc=0
wct=0
checkme=[]
foundDirs=[]
notfound=[]
falsepositive=[]
separator='~'*40+'\n\n\n'


#get total words in list
for i in dirlist:
	wct+=1
dirlist.seek(0)


for dirr in dirlist:
	print '[*] Trying dirs %s/%s'%(wc,wct) # display curr/total count
	resp=requests.get(target+dirr.strip(),headers=OPTIONAL_HEADERS,verify=False,proxies=proxy,allow_redirects=False)

	#response sorting logic
	if resp.status_code == 404 or resp.status_code == 302:
		notfound.append(dirr + '::: status:%s'%resp.status_code)
	elif resp.status_code == 200:
		if failCase in resp.content:
			falsepositive.append(dirr)
		else:
			foundDirs.append(dirr)
	else:
		checkme.append(dirr)


	wc+=1 #increment curr count

write_results(foundDirs,notfound,checkme,falsepositive)
print '[!] scan complete....writing files\n'
print '[~~~~~~~~~~~~~] Dirs Found [~~~~~~~~~~~~~]\n\n'
for i in foundDirs:
	print i.strip()
print '\n\n[~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~]'
print '\n[!!] Done: please see results in current dirr'



### 0x10w1eve1 ###


import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys


##### TO DO #######
# 1) add recursive scanning from found dirs, maybe do permuations of all found dirs
# 2) parse all wordlists to get files without default extension, and add own extension based on needs
# 3) MultiThread it all, if wordlists > 50k
# 4) send results to file after like 10k through wordlist, or 20 min, whichever comes first, so incase you have to cut it short you have something.
# 5) Add POST scanning (change request headers,body, and you need to do #2 on the list first) 

Usage = " ### 0x10w1evee1 ### \nUsage: %s <target> <wordlist> <outfile>\n\ttarget = protocol://site \n"%sys.argv[0]
if len(sys.argv) !=4:
	print Usage
	sys.exit()

target=sys.argv[1]+"/web/"
#all_targets=['Home','Content','']
dirlist=open(sys.argv[2],'r')
outfile=sys.argv[3]
wc=0
wct=0
checkme=[]
foundDirs=[]
notfound=[]
falsepositive=[]
separator='~'*40+'\n\n\n'

logfile=open(outfile,'w')
logfile.write('[0x31 0x30 0x77 0x31 0x65 0x76 0x65 0x31]\n\n')
logfile.write(' # 0x10w1evee1 # Showing results for the below options:\n')
logfile.write('Target: %s  |  Wordlist: %s  | Outfile: %s \n\n'%(target,sys.argv[2],outfile))
logfile.write(separator)
#logfile.seek(0)
logfile.close() #didnt want to keep the file open for loong scans. not sure if this is better than opening twice. maybe just seek it back and keep writing.


def write_results(foundDirs,notfound,checkme,falsepositive):
	logfile = open(outfile,'a')
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
	logfile.close()	



### CHANGE these vars accordingly

Cookie=''
failCase='404 Error'
proxy = {"https":"http://127.0.0.1:8080"}
OPTIONAL_HEADERS={
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
	'Cookie':'%s'%Cookie
}
### 


#get total words in list
for i in dirlist:
	wct+=1
dirlist.seek(0)

print '[**** Staring scan with GET ****'
for dirr in dirlist:
	print '[*] Trying dirs %s/%s'%(wc,wct) # display curr/total count
	resp=requests.get(target+dirr.strip(),headers=OPTIONAL_HEADERS,verify=False,proxies=proxy,allow_redirects=False)

	#response sorting logic

	if resp.status_code == 404 or resp.status_code == 302: # some IIS pages will give a 302 moved if you're not authed, not a good indicator, i usually play with these later
		notfound.append(dirr + '::: status:%s'%resp.status_code)
	elif resp.status_code == 200:
		if failCase in resp.content:
			falsepositive.append(dirr)
		else:
			foundDirs.append(dirr)
	else:
		checkme.append(dirr + " ::: status %s"%resp.status_code)


	wc+=1 #increment curr count

write_results(foundDirs,notfound,checkme,falsepositive)
print '[!] scan complete....writing files\n'
print '[~~~~~~~~~~~~~] Dirs Found [~~~~~~~~~~~~~]\n\n'
for i in foundDirs:
	print i.strip()
print '\n\n[~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~]'
print '\n[!!] Done: please see results in current dirr'



### 0x10w1eve1 ###


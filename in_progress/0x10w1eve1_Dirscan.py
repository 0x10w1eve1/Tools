import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys


##### TO DO #######
'''
 1) add recursive scanning from found dirs, maybe do permuations of all found dirs
 2) parse all wordlists to get files without default extension, and add own extension based on needs
 3) MultiThread it all, if wordlists > 50k
 4) send results to file after like 10k through wordlist, or 20 min, whichever comes first, so incase you have to cut it short you have something.
 5) Add POST scanning (change request headers,body, and you need to do #2 on the list first) 
 6) Add argparse to give user options
	- get/post or both
	-custom headers: cookie, data etc
	-custom fail cases : default is regular status code 404
		- Failcase customization :  -F[# of custom failcases] ["fail case string #1"] ["fail case string #2"]ex; -F2 "this is custom 404" "this is custom 403"
	-log verbosity: 
		-make functions for printing logs. each func one log type. 
		-make arparse option for levels 1-w.e
			not specified(default): write all found dirs with 200 (failcases counting as 200)
			1- found dirs, custom failcase dirs-->organize by  column=failcase 1, failcase 2 etc
			2- found dirs, custom failcase dirs, all status codes found --> organized by "other status codes (excluding 404, and failcase dirs::meaning dont count the status code from a failcase as a separate stat code)
			3- found dirs, custom failcase dirs, all status codes found, not found (404 and anything marked as 404 if *custom code argparse* option was given)
	-custom codes to be counted as found 
		- will group the specified codes as found dirs. 
	-custom codes to be counted as not found
7) add default configs to Usage:
	-found dirs: http 200
	-not found: 404 (auto includes all failcases)
	-log verbosity: default is just 200's (with failcases not counting as 200)

'''


Usage = " ### 0x10w1evee1 ### \nUsage: %s <target> <wordlist> <outfile>\n\ttarget = protocol://site \n"%sys.argv[0]
if len(sys.argv) !=4:
	print Usage
	sys.exit()

target=sys.argv[1]+"/"
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


### CHANGE these vars accordingly
failCase="was not found or does not implement IController." #not found
forbiddenCase="A public action method &#39;LogOn&#39; was not found on controller &#39;Indralok.LIS.UI.SharedController&#39;." #controller found
Cookie=''
proxy = {"https":"http://127.0.0.1:8080"}
OPTIONAL_HEADERS={
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}
### 


def write_results(foundDirs,notfound,checkme,falsepositive):
	logfile = open(outfile,'a')
	logfile.write('~~~~~~~~~~~~~~ These Exist ~~~~~~~~~~~~~~\n\n')
	if foundDirs:
		for i in foundDirs:
			logfile.write(i)
	else:
		logfile.write('None\n')
	logfile.write(separator)

	logfile.write('~~~~~~~~~~~~~~ These Dont ~~~~~~~~~~~~~~\n\n')
	if notfound:
		for i in notfound:
			logfile.write(i)
	else:
		logfile.write('None\n')
	logfile.write(separator)
	
	logfile.write('~~~~~~~~~ Check These Manually ~~~~~~~~~\n\n')
	if checkme:
		for i in checkme:
			logfile.write(i)
	else:
		logfile.write('None\n')
		'''
	logfile.write(separator)
	logfile.write('~~~~~~~~~ Custom 404 Page ~~~~~~~~~\n\n')
	if falsepositive:
		for i in falsepositive:
			logfile.write(i)
	else:
		logfile.write('None\n')
	
	logfile.write(separator)
	'''
	logfile.write('\n[0x31 0x30 0x77 0x31 0x65 0x76 0x65 0x31]\n\n')
	logfile.close()	




#get total words in list
for i in dirlist:
	wct+=1
dirlist.seek(0)

print '[**** Staring scan with GET ****'
for dirr in dirlist:
	print '[*] Trying dirs %s/%s'%(wc,wct) # display curr/total count
	resp=requests.get(target+dirr.strip(),headers=OPTIONAL_HEADERS,verify=False,proxies=proxy,allow_redirects=False)

	#response sorting logic

	if failCase in resp.content:
		notfound.append(dirr)
	elif forbiddenCase in resp.content:
		foundDirs.append("CONTROLLER FOUND::::" + dirr)
	else:
		checkme.append(dirr.strip() + '::: status:%s \n'%resp.status_code)
	'''

	elif resp.status_code == 404 or resp.status_code == 302: # some IIS pages will give a 302 moved if you're not authed, not a good indicator, i usually play with these later
		notfound.append(dirr + '::: status:%s'%resp.status_code)
	elif resp.status_code == 200:
		if failCase in resp.content:
			falsepositive.append(dirr)
		else:
			foundDirs.append(dirr)
	else:
		checkme.append(dirr.strip() + " ::: status %s \n"%resp.status_code)
	'''

	wc+=1 #increment curr count

write_results(foundDirs,notfound,checkme,falsepositive)
print '[!] scan complete....writing files\n'
print '[~~~~~~~~~~~~~] Dirs Found [~~~~~~~~~~~~~]\n\n'
for i in foundDirs:
	print i.strip()
print '\n\n[~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~]'
print '\n[!!] Done: please see results in current dirr'



### 0x10w1eve1 ###


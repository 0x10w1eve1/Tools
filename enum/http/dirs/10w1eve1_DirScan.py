import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys





Usage = "\nUsage: %s <target> <wordlist> <outfile> <y to check for customfaile cases> \n\n\ttarget = protocol://site \n"%sys.argv[0]


if len(sys.argv) == 5:
	if(sys.argv[4].lower() == 'y'):
		customfailcaseneeded=True
		
elif len(sys.argv) == 4:
	customfailcaseneeded=False

else:
	print("\n\n"+Usage+"\n\n")
	sys.exit()

target=sys.argv[1]+"/"
dirlist=open(sys.argv[2],'r')
outfile=sys.argv[3]

wc=0
wct=0

foundDirs=[]
notfound=[]
falsepositive=[]
checkme=[]





### CHANGE these vars accordingly
if(customfailcaseneeded):
	failCase="" 
	forbiddenCase="" 


#Cookie=''
proxy = {"https":"http://127.0.0.1:8080"}
OPTIONAL_HEADERS={
	'User-Agent':'Mozilla/5.0 (Google) Gecko/20100101 Firefox/78.0'
}
### 


def write_results(resultList,logfile):
	
	logfile.write('~'*40+'\n\n\n')
	
	if(resultList):
		for i in resultList:
			logfile.write(i)
		
	
	


#get total words in list
for i in dirlist:
	wct+=1
dirlist.seek(0)

print("[+] Starting Scan... ")
for dirr in dirlist:
	print('[*] Trying dirs %s/%s'%(wc,wct)) # display curr/total count
	resp=requests.get(target+dirr.strip(),headers=OPTIONAL_HEADERS,verify=False,proxies=proxy,allow_redirects=False)

	#response sorting logic



	if resp.status_code == 404 or resp.status_code == 302: # some IIS pages will give a 302 moved if you're not authed, not a good indicator, i usually play with these later
		notfound.append(dirr + '\t\t\t [ %s ] \n'%resp.status_code)
	elif resp.status_code == 200:
		if(customfailcaseneeded): # if testing for custom cases, check for custom 404 and add to false pos
			if failCase in resp.content:
				falsepositive.append(dirr.strip() + '\t\t\t [False Positive]\n')
		else: #if not checking for custom cases and its a 200, add to found dirs
			foundDirs.append(dirr.strip() + '\t\t\t [ 200 ]\n')

	else:
		checkme.append(dirr.strip() + '\t\t\t [ %s ] \n'%resp.status_code)


	wc+=1 #increment curr count




print('[+] scan complete....writing files\n')

scandata="\t\t[0x31 0x30 0x77 0x31 0x65 0x76 0x65 0x31]\n\n\t\tScan Info:\n\t\t\tTarget: %s\n\t\t\tWordlist: %s\n\t\t\tOutfile: %s\n\t\t\tProxy: %s\n"%(target,sys.argv[2],outfile,proxy)

with open(outfile,'w') as f: f.write(scandata+'\n\n\n'+'Directory\t\t\t Status Code\n')

with open(outfile,'a') as f:

	if(customfailcaseneeded):
		write_results(falsepositive,f)

	write_results(foundDirs,f)
	write_results(checkme,f)



print('[~~~~~~~~~~~~~] Dirs Found [~~~~~~~~~~~~~]\n\n')
for i in foundDirs:
	print(i.strip())
print('\n'+'~'*40+'\n\n\n')




### 0x10w1eve1 ###


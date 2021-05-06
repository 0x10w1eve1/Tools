import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys

proxy = {"https":"http://127.0.0.1:8080"}



Usage = "\nUsage: %s <wordlist>\n"%sys.argv[0]
if len(sys.argv) !=2:
	print Usage
	sys.exit()


dirlist=open(sys.argv[1],'r')

wc=0
wct=0
#get total words in list
for i in dirlist:
	wct+=1
dirlist.seek(0)

ok=[]
other=[]

for dir in dirlist:
	print '[*] Trying %s/%s dir(s)'%(wc,wct) # display curr/total count
	req=requests.get('https://ip:8000/welcome/%s/'%dir.strip(),verify=False,proxies=proxy)
	if req.status_code == '200':
		print '[*] %s/ ::: %s'%(dir.strip(),req.status_code)
		ok.append(dir)
	else:
		other.append(dir + 'status:%s'%req.status_code)

	wc+=1 #increment curr count

print '[+] 200 Response Dirs Found'
for i in ok:
	print i


#stream=urllib3.PoolManager()

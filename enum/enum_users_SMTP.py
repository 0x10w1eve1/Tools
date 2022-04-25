import socket
import sys

def vrfy(ip,port,userList):
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((ip,int(port)))
	banner = s.recv(1024)
	print banner
	s.send("EHLO 10w1eve1\r\n")
	result=s.recv(1024)
	if "VRFY" in result:
		print "yes"
	else:
		print "no"
	try:
		for i in userList:
			s.settimeout(15)
			s.send('VRFY ' + i + '\n')
			result = s.recv(1024)
			return result
	except socket.timeout:
			s.close()
			return "[!] Vrfy command disabled"


if len(sys.argv) <4:
	print """
	***********************************
	Usage: %s <target> <port> <username list>

	***********************************"""%sys.argv[0]

ip=sys.argv[1]
port = sys.argv[2]
userList=open(sys.argv[3],"r")

print vrfy(ip,port,userList)




### 0x10w1eve1 ###

import socket
import sys

ip=sys.argv[1]
port=int(sys.argv[2])
req="DESCRIBE rtsp://%s:%s RTSP/1.0\r\nCSeq: 2\r\n\r\n"%(ip,port)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((ip,port))
s.send(req)
data=s.recv(1024)
print data


### 0x10w1eve1 ###

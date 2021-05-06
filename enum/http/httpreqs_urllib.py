import urllib3
import sys

def getresp(stream):
	print stream.status
	#print stream.data
	#print stream.headers

def exploit(stream,method,url):
	r = stream.request(method,url,verify=False)
	getresp(r)

if len(sys.argv) !=3:
	print 'Usage: %s <http(s)://target> <method>'%sys.argv[0]
	sys.exit()

url = sys.argv[1]
method = (sys.argv[2]).upper()
#proxy = urllib3.ProxyManager("http://127.0.0.1:8080/")
stream = urllib3.PoolManager()
exploit(stream,method,url)

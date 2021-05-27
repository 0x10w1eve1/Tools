# Tools

These are some programs I wrote during OSCP training and engagements for work. I use most of these on a daily basis so perhaps they will help you too!

I am currently working on several scripts _(see Ongoing section below)_ and will be updating this repo with any changes. 


**Exploits:** *(I did not discover any of these exploits, I wrote them based off the cve writeups/tutorials) *
  * Buffer Overflow helper scripts
  * non-seh stack based buffer overflow poc's for crossfire, ability server, freefloat, minishare, and savant. 
  * webdav exploit poc

**crackoders:**: password cracking and decoding scripts

**enum:** Directory scanner, login bruteforce, webdav, rtsp, smtp..etc 

**wordlistEdit:** scripts for wordlist generation and file searches/manipulation
	

### **Ongoing Projects**: 

1) in_progress/0x10w1eve1_Dirscan.py   _Recently came across a site that had a custom 404 message giving 200's, couldn't figure out how to do it in dirbuster/gobuster so i wrote this. I plan to add functionality to it as well_
2) in_progress/wordlist_generator   _Extract all words in pdf/doc file and create a wordlist for bruteforcing/enumeration. 
3) Exploits/webdav/10w1eve1_webdav_poc.py   _tried to use this recently and couldnt get urllib3 to work with https. Im planning to change this to import requests instead of urllib3. Just not sure when i'll get to it but you can get the script to work by using a requests object instead: 
						Instead of: requests.Post()
						Use: requests.request("PROPFIND")_
						


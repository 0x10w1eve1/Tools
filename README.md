# Tools

Some of the programs I wrote during engagements. I will add new stuff here too.  

**Exploits:** *(I did not discover any of these exploits, i wrote them based off the cve writeups/tutorials) *
  * Buffer Overflow helper scripts
  * non-seh stack based buffer overflow poc's for crossfire, ability server, freefloat, minishare, and savant. 
  * webdav poc

**crackoders:**: password cracking and decoding scripts


**enum: scripts:** Directory scanner, login bruteforce, webdav, rtsp, smtp..etc 

**wordlistEdit:** scripts for wordlist generation and file searches/manipulation
	

### **New Stuff**: 

1) enum/http/dirs/0x10w1eve1_Dirscan.py   _Recently came across a site that had a custom 404 message giving 200's, couldn't figure out how to do it in dirbuster/gobuster so i wrote this. I plan to add functionality to it as well_
2) Exploits/webdav/10w1eve1_webdav_poc.py   _tried to use this recently and couldnt get urllib3 to work with https. So im planning to change this to import requests instead of urllib3. Just not sure when i'll get to it but you can acheive the same with a requests object by doing requests.request("PROPFIND")_

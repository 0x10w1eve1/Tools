# Tools

Hello, these are some of the "public-safe" programs I wrote during my OSCP training _(spoilers removed)_ and work-related engagements. There is nothing crazy here, mainly scripts to automate pen testing techniques. _If my non-existent comments are not clear enough, please fee free to reach out with any questions !_

**Exploit Writing (begginer):** _(cve's and original poc's can be found online)_
  * Buffer Overflow helper scripts
  * non-seh stack based buffer overflow poc's for crossfire, ability server, freefloat, minishare, and savant. 
  * webdav exploit poc

**crackoders:**: password cracking and decoding scripts

**enum:** Directory scanner, login bruteforce, webdav, rtsp, smtp..etc 

**wordlistEdit:** scripts for wordlist generation and file parsing	


### **In Progress**: 

1) **0x10w1eve1_Dirscan.py**
_Recently came across a site that had a custom 404 message giving 200's, couldn't figure out how to do it in dirbuster/gobuster so i wrote this. I plan to add functionality to it as well_
3) **wordlist_generator**
_Extract all words in pdf/doc file and create a wordlist for bruteforcing/enumeration. 

### **_Note_**

**_Exploits/webdav/10w1eve1_webdav_poc.py_** 
_tried to use this recently and couldnt get urllib3 to work with https. Im planning to change this to import requests instead of urllib3. Just not sure when i'll get to it but you can get the script to work by using a requests object (Instead of requests.Post() use requests.request("http_method"))_
						


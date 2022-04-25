from socket import *
from scapy.all import *
import netaddr


if len(sys.argv)!=2:
	print(f"[!] Usage: python {sys.argv[0]} <network in CIDR notation> ")
	sys.exit(0)


network = sys.argv[1]
print(f'[*] Performing ping sweep on {network}')
network = netaddr.IPNetwork(network)
for ip in network:

	iplayer = IP(dst=str(ip))
	ping = iplayer/ICMP()

	reply = sr1(ping, timeout=3,verbose=0)
	if not reply:
		continue
	if reply.getlayer(ICMP).type == 0 and reply.getlayer(ICMP).code == 0:
			seq=reply.getlayer(ICMP).seq
			ttl=reply.getlayer(IP).ttl
			print(f"[+] Host {ip} is responding to ICMP packets")


### 0x10w1eve1 ###

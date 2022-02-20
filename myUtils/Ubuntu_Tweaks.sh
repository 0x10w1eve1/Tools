#!/bin/bash
# automate ubuntu customization, r option is non-interactive.

#util vars
username=$(users)
dnsfile="/etc/systemd/resolved.conf"
netmanfile="/etc/NetworkManager/NetworkManager.conf"
##default dirs to remove from /home/$username
redundirs=("Desktop" "Pictures" "Public" "Templates" "Videos")
##temp for chrome download
tempfordl="/tmp/"



# basic commands

proceed (){
	echo -e "\n Hit enter to continue"
	read continue
}


cleanin (){
	echo -e "\n[+] Cleaning..."
	apt autoremove -y
	apt autoclean
}

regUpdate (){
	echo -e "\n [+] Updating System"
	apt update && apt upgrade -y
	cleanin
}

rebootin (){
	echo "[+] Rebooting in 10seconds..."
	sleep 10
	reboot -f
}

usermodin (){
	# sudo no passwd
	echo -e "\n [!] Adding current user as sudo nopasswd: (y/n) "
	echo -e "\n${username} ALL=(ALL) NOPASSWD: ALL"|tee -a /etc/sudoers
	
	for i in ${redundirs[@]};do
		rm -rf /home/$username/$i
		rm -rf /root/$i
	done

}

chngusername (){
	echo -e "\n [!] Changing username, Enter current username: "
	read curruser
	usermod -l $username $curruser; usermod -d /home/$username -m $username
}


# remove snap,cups, updatenotifier
rmSnapnStuff (){
	echo -e "\n[+] Starting SnapD destruction...\n"
	
	echo -e "\n--> Removing snap-store"
	snap remove --purge snap-store

	## if new install, shouldnt be any packages so commented this out to keep non interactive #
	#echo -e "\n===> $(snap list) <===\n"
	#echo "<!> Enter name of Snap pkg to delete, or N to continue:   "
	#read todesnap;
	
	#while [[ $todesnap != "N" ]]
	
	#do
		#echo -e "\n--> Removing ${todesnap}"
		#snap remove --purge $todesnap
		
		#echo "<!> Enter name of pkg to delete, or N to continue:   "
		#read todesnap
	#done
	
	echo -e "\n--> Removing snapd cache"
	rm -rf /var/cache/snapd/
	echo -e "\n--> Removing snapd"
	apt autoremove --purge snapd -y
	apt autoremove --purge gnome-software-plugin-snap
	echo -e "\n--> removing snap directories"
	for i in $(ls /home/);do rm -rf /home/$i/snap;done
	rm -rf /root/snap
	apt-mark hold snapd

	echo -e "\n[+] Removing update notifier"
	apt autoremove --purge update-notifier -y
	echo "[+] Disabling Cups service\n"
	systemctl stop cups
	systemctl disable cups
	apt autoremove --purge cups -y
	cleanin

}


# free port 53
DNSedit (){
	echo "[+] Editing DNS to free port 53, enable dnssec and dnsovertls"


	cp $dnsfile $dnsfile".bak"
	dnsmods=("DNS=1.1.1.1" "FallbackDNS=1.0.0.1" "DNSStubListener=no" "DNSSEC=true" "DNSOverTLS=yes")

	for i in ${dnsmods[@]};do
	echo -e "\n${i}" | tee -a $dnsfile
	done
	
	echo "[+] Creating resolv symlink"
	ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
	
	echo -e "\n[+] Modifying NetworkManager.conf"
	netmanconf="""
[main]
plugins=ifupdown,keyfile
dns=systemd-resolved

[ifupdown]
managed=false

[device]
wifi.scan-rand-mac-address=no
"""
	echo -e "\n${netmanconf}" > $netmanfile
	echo "[+] Restarting systemd-resolved & NetworkManager"
	systemctl restart systemd-resolved
	systemctl restart NetworkManager
	
}


changesources (){

	echo -e "\n[+] changing apt sources list "

	sourcesList="""
#ubuntu
deb http://us.archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse
deb-src http://us.archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse

deb http://us.archive.ubuntu.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://us.archive.ubuntu.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://security.ubuntu.com/ubuntu focal-security main restricted universe multiverse
deb-src http://security.ubuntu.com/ubuntu focal-security main restricted universe multiverse
"""
	echo -e "\n${sourcesList}" > /etc/apt/sources.list
	apt update 
	
}

getTools (){
	#update system
	regUpdate

	#below is autoinstalled after upgrade
	#apt install ca-certificates

	echo "[+] Downloading Chrome"
	apt install wget
	wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O $tempfordl.googleChrome
	
	echo -e "[+] Installing chrome"
	dpkg -i $tempfordl.googleChrome

	echo -e "[+] Installing other Tools"
	rm $tempfordl.googleChrome

	echo -e "\n--> adding cherryTree repo"
	add-apt-repository ppa:giuspen/ppa -y

	echo -e "\n--> fetching sublime key"
	echo -e "\n\n#sublime\ndeb https://download.sublimetext.com/ apt/stable/" >> /etc/apt/sources.list
	wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -

	apt update

	echo "wireshark-common wireshark-common/install-setuid boolean false" | debconf-set-selections
	DEBIAN_FRONTEND=noninteractive apt -y install wireshark curl nmap sublime-text cherrytree gnome-tweaks gnome-tweak-tool ssh apache2 net-tools rhythmbox pulseaudio pulseeffects
	cleanin	

}


runchecks (){
	echo -e "\n[+] Printing sudoers"
	cat /etc/sudoers
	echo -e "\n[+] Printing resolv.conf"
	cat /etc/resolv.conf
	ls -l /etc/resolv.conf
	echo -e "\n[+] Printing NetworkManager.conf"
	cat netmanconf
}


dnsmasq (){
	apt install dnsmasq
	systemctl stop systemd-resolved
	systemctl disable systemd-resolved
	

	echo -e "\nport=5353" >> /etc/dnsmasq.conf
	echo -e """
	[main]
	plugins=ifupdown,keyfile
	dns=dnsmasq          

	[ifupdown]
	managed=false

	[device]
	wifi.scan-rand-mac-address=no
""" > /etc/NetworkManager/NetworkManager.conf 

	systemct restart dnsmasq
	systemctl restart NetworkManager

}

forvpn (){
	apt install resolvconf
	deps=("systemd-resolved NetworkManager resolvconf")
	systemctl stop resolvconf
	systemctl enable resolvconf
	for i in ${deps[@]};do
		systemctl restart $i 

	done

}

install (){
	# Main program
	echo -e "\n[+] Starting Install..."

	rmSnapnStuff
	DNSedit
	changesources
	getTools
	rebootin
}

# Main Program 

echo -e "\n [?] Regular install or custom?: r/c"
read installtype


if [[ $installtype == "r" ]]
then
	install

elif [[ $installtype == "c" ]]
	then
	echo -e "\n [+++] Available Functions [+++] \n"
	AllFuncs=$(declare -F | awk '{print $NF}' | sort | egrep -v "^_")
	for i in $AllFuncs;do echo -e "+${i}";done
	echo -e "\n [?] Enter desired functions separated by a space"
	read userFunctions	
	functionsToExec=($(echo $userFunctions | sed 's/ /\n/g'))
	for func in ${functionsToExec[@]};do
		if [[ $(echo ${AllFuncs} | grep -w -q ${func};echo $?) == 1 ]]
		then
			invalid+=($func)
		else
			valid+=($func)
		fi
	done

	if (( ${#invalid[@]} ))
	then
		echo -e "\n [!] Invalid Functions [!] "
		for i in ${invalid[@]};do echo -e "+${i}";done
	fi
	if (( !${#valid[@]} ))
	then
		echo -e "\n [!!!] No valid functions entered...exiting"
		exit
	else
		echo -e "\n[?] Run valid functions? (y/n)"
		read continue
		if [[ $continue == 'y' ]]
		then
			echo -e "\n[+] Running functions...\n"
			for func in ${valid[@]};do 
				echo -e "--> ${func}"
				$func
			done
		else
			echo -e "\n[+] Not running.. Exiting..."
			exit
		fi
	fi
else
	echo -e "\n Invalid input, expecting r|c, exiting..."
fi

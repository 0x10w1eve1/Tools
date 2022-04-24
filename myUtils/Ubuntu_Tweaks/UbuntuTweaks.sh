#!/bin/bash

##############################################################################
######									######
######	Automate some basic ubuntu customizations 			######
######	For non-interactive run see comments in rmSnapnStuff function	######
###### 									######
##############################################################################


if [[ $(id -u) -ne 0 ]]
then
        echo -e "\n\n\t\t\t [!] You Might need Root, y to proceed anyway [!]\n\n"
        read pro
        if [[ "$pro"!="y" ]];then
                exit
        fi
fi


#util vars
username=$(users|cut -d " " -f1)
dnsfile="/etc/systemd/resolved.conf"
netmanfile="/etc/NetworkManager/NetworkManager.conf"
##default dirs to remove from /home/$username
redundirs=("Desktop" "Pictures" "Public" "Templates" "Videos")
##temp for deb pkgs download
tempfordl="/tmp/"

##Ubuntu Sources List
DISTRIB_CODENAME=$(cat /etc/lsb-release|grep "DISTRIB_CODENAME"|cut -d "=" -f2)
UbuntuSrcLst="""

deb http://us.archive.ubuntu.com/ubuntu/ ${DISTRIB_CODENAME} main restricted universe multiverse
deb-src http://us.archive.ubuntu.com/ubuntu/ ${DISTRIB_CODENAME} main restricted universe multiverse
deb http://us.archive.ubuntu.com/ubuntu/ ${DISTRIB_CODENAME}-updates main restricted universe multiverse
deb-src http://us.archive.ubuntu.com/ubuntu/ ${DISTRIB_CODENAME}-updates main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu ${DISTRIB_CODENAME}-security main restricted universe multiverse
deb-src http://security.ubuntu.com/ubuntu ${DISTRIB_CODENAME}-security main restricted universe multiverse

"""




# basic commands

proceed (){
	echo -e "\n\n\t\t\t Hit enter to continue"
	read continue
}


cleanin (){
	echo -e "\n\n\t\t\t[+] Cleaning..."
	apt autoremove -y
	apt autoclean
}

regUpdate (){
	echo -e "\n\n\t\t\t [+] Updating System"
	apt update && apt upgrade -y
	cleanin
}

rebootin (){
	echo "\n\t\t\t[+] Rebooting in 10seconds..."
	sleep 10
	reboot -f
}

usermodin (){
	# sudo no passwd
	echo -e "\n\n\t\t\t [!] Adding current user as sudo nopasswd: (y/n) "
	echo -e "\n${username} ALL=(ALL) NOPASSWD: ALL"|tee -a /etc/sudoers
	
	for i in ${redundirs[@]};do
		if [[ "$i" != "${username}" ]];then
			rm -rf /home/$username/$i
			rm -rf /root/$i
		fi
	done

}

chngusername (){
	echo -e "\n\n\t\t\t [!] Changing username, Enter current username: "
	read curruser
	usermod -l $username $curruser; usermod -d /home/$username -m $username
}


# remove snap,cups, updatenotifier
rmSnapnStuff (){
	echo -e "\n\n\t\t\t[+] Starting SnapD destruction...\n"
	
	echo -e "\n\n\t\t\t--> Removing snap-store"
	snap remove --purge snap-store
	snap remove --purge firefox
	# START COMMENT HERE__for non-interactive
	echo -e "\n\n\t\t\t===> $(snap list) <===\n"
	echo "<!> Enter name of Snap pkg to delete, or N to continue:   "
	read todesnap;
	
	while [[ $todesnap != "N" ]]
	
	do
		echo -e "\n--> Removing ${todesnap}"
		snap remove --purge $todesnap
		
		echo "<!> Enter name of pkg to delete, or N to continue:   "
		read todesnap
	done
	# END COMMENT HERE__for non-interactive
	echo -e "\n\n\t\t\t--> Removing snapd cache"
	rm -rf /var/cache/snapd/
	echo -e "\n\n\t\t\t--> Removing snapd"
	apt autoremove --purge snapd -y
	apt autoremove --purge gnome-software-plugin-snap
	echo -e "\n\n\t\t\t--> removing snap directories"
	for i in $(ls /home/);do rm -rf /home/$i/snap;done
	rm -rf /root/snap
	apt-mark hold snapd

	echo -e "\n\n\t\t\t[+] Removing update notifier"
	apt autoremove --purge update-notifier -y
	echo "\n\t\t\t[+] Disabling Cups service\n"
	
	#stopping&removing printing service, who needs open ports and save them trees ya fool
	systemctl stop cups
	systemctl disable cups
	apt autoremove --purge cups -y
	cleanin

}


# free port 53
DNSedit (){
	echo "\n\t\t\t[+] Editing DNS to free port 53, enable dnssec and dnsovertls"


	cp $dnsfile $dnsfile".bak"
	dnsmods=("DNS=1.1.1.1" "FallbackDNS=1.0.0.1" "DNSStubListener=no" "DNSSEC=true" "DNSOverTLS=yes")

	for i in ${dnsmods[@]};do
	echo -e "\n${i}" | tee -a $dnsfile
	done
	
	echo "[+] Creating resolv symlink"
	ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
	
	echo -e "\n\n\t\t\t[+] Modifying NetworkManager.conf"
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
	echo "\n\t\t\t[+] Restarting systemd-resolved & NetworkManager"
	systemctl restart systemd-resolved
	systemctl restart NetworkManager
	
}


changesources (){

	echo -e "\n\n\t\t\t [+] changing apt sources list "

	sourcesList=$UbuntuSrcLst
	
	cp /etc/apt/sources.list /etc/apt/sources.list.original
	echo -e "\n${sourcesList}" > /etc/apt/sources.list
	apt update 
	
}

getTools (){
	#update system
	regUpdate

	
	#apt install ca-certificates
	dlChrome="${tempfordl}googleChrome"
	dlBurp="${tempfordl}BurpPro.sh"
	echo "\n\n\t\t\t[+] Downloading Chrome \n\n"
	apt install wget
	wget "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" -O $dlChrome
	
	#chrome
	echo -e "[+] Installing chrome"
	dpkg -i $dlChrome
	rm $dlChrome

	#BurpSuite
	#burpsuite community
	wget "https://portswigger-cdn.net/burp/releases/download?type=Linux" -O $dlBurp
	chmod +x $dlBurp
	/bin/sh $dlBurp
	rm $dlBurp
	
	#burpsuite pro
	#wget "https://portswigger-cdn.net/burp/releases/download?&type=Linux" -O $dlBurp
	
	
	echo -e "[+] Installing other Tools"

	echo -e "\n--> adding cherryTree repo"
	add-apt-repository ppa:giuspen/ppa -y

	echo -e "\n--> fetching sublime key"
	echo -e "\n\n#sublime\ndeb https://download.sublimetext.com/ apt/stable/" >> /etc/apt/sources.list
	wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -

	#firefox (non snap repo)
	add-apt-repository ppa:mozillateam/ppa
	#auto upgrade
	echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox
	

	apt update

	echo "wireshark-common wireshark-common/install-setuid boolean false" | debconf-set-selections
	DEBIAN_FRONTEND=noninteractive apt -y install wireshark
	apt-get install -y curl nmap sublime-text cherrytree gnome-tweaks ssh apache2 net-tools git aircrack-ng firefox gnome-shell-extensions
	#music tools
	#clementine pulseaudio pulseeffects pavucontrol
	
	
	
	
	
	echo -e "\n\t [+] Done installing Tools [+]"
	
	
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
	echo -e "\n[+] Modifying NetworkManager.conf"
	netmanconf="""
[main]
plugins=ifupdown,keyfile
dns=resolvconf
[ifupdown]
managed=false
[device]
wifi.scan-rand-mac-address=no
"""
	echo -e "\n${netmanconf}" > $netmanfile
	systemctl stop resolvconf
	systemctl enable resolvconf
	for i in ${deps[@]};do
		systemctl restart $i 

	done

}

install (){
	# Main program
	echo -e "\n\n\t\t\t[+][+] Starting Install [+][+]\n\n "
	regUpdate
	#usermodin
	rmSnapnStuff
	getTools
	qqqqqqqqqrebootin
}

# Main Program 

echo -e "\n\n\t\t\t[?] Regular install or custom?: r/c"
read installtype


if [[ $installtype == "r" ]]
then
	install

elif [[ $installtype == "c" ]]
then
	echo -e "\n\n\t\t\t [+++] Available Functions [+++] \n"
	AllFuncs=$(declare -F | awk '{print $NF}' | sort | egrep -v "^_")
	for i in $AllFuncs;do echo -e "+${i}";done
	echo -e "\n\n\t\t\t [?] Enter desired functions separated by a space"
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
		echo -e "\n\n\t\t\t [!!!] No valid functions entered...exiting"
		exit
	else
		echo -e "\n\n\t\t\t [!] Chosen Functions [!] \n\n"
		for i in ${valid[@]};do echo -e "+${i}";done
		echo -e "\n\n\t\t\t[?] Run functions? (y/n)"
		
		read continue
		if [[ $continue == 'y' ]]
		then
			echo -e "\n\n\t\t\t[+] Running functions...\n"
			for func in ${valid[@]};do 
				echo -e "--> ${func}"
				$func
			done
		else
			echo -e "\n\n\t\t\t[+] Not running.. Exiting..."
			exit
		fi
	fi
else
	echo -e "\n\n\t\t\t [!] Invalid input, expecting r|c, exiting..."
fi

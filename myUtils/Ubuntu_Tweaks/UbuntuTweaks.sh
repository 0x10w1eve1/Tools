#!/bin/bash

Usage="""
#########0x10w1eve1###################################################
###### 								######
###### 		USAGE:	dot-slash-it, c will list functions	######
###### 								######
######	Customizations 'TO DO' after a fresh Ubuntu install	######
######								######
######		If needing a non-interactive run, comment out:	######
######		--> while loop in rmSnapnStuff			######
######		--> BurpSuite install (it needs a few clicks)	######
###### 								######
###### 		*Tested on*:	[ Ubuntu Focal 20.04.4 LTS ]	######
######				[ Ubuntu Jammy 22.04 LTS ]	######
###### 								######
########0x10w1eve1####################################################

*******************************************
*********** 14 Available Functions ********
*******************************************

+proceed --> too complicated to explain

+cleanin --> clean apt cache files

+regUpdate --> run update/upgrade

+rebootin --> reboot system

+usermodin --> let user sudo without passwd. 

+rmSnapnStuff --> oh snap we snapped the snap

+DNSedit --> free port 53, add cloudflare local dns route, enable secure dns

+changesources --> clean sources.list

+getTools -->	install chrome, wireshark, curl, wget, aircrack-ng, nmap,
				sublime-text, cherrytree, gnome-tweaks, ssh, apache2, 
				net-tools, make, BurpSuite

+chngusername --> change username

+runchecks --> print configs to check dns editions

+dnsmasq --> install dnsmasq

+forvpn --> install resolvconf for dns management if bridging

+install --> Run functions: regUpdate, usermoding, rmSnapnStuff, DNSedit, getTools

*******************************************
*******************************************

"""


if [[ $(id -u) -ne 0 ]]
then
        echo -e "\n\n\t\t\t [!] You Might need Root, y to proceed anyway [!]\n\n"
        read pro
        if [[ "$pro"!="y" ]];then
                exit
        fi
fi

if [[ "$1"=="-h" ]]
then
	echo -e "\n\n\t$Usage"
fi

############## GLOBALS ####################

#util vars
username=$(users|cut -d " " -f1)
dnsfile="/etc/systemd/resolved.conf"
netmanfile="/etc/NetworkManager/NetworkManager.conf"
##default dirs to remove from /home/$username
redundirs=("Desktop" "Pictures" "Public" "Templates" "Videos" "Documents")
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

##########################################

############### HELPERS ##################

proceed (){
	echo -e "\n\n\t\t\t Hit enter to continue"
	read continue
}


cleanin (){
	echo -e "\n\n\t\t\t[+] Cleaning apt files\n"
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

##########################################
############ Default Install #############


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




# remove snap,cups, updatenotifier
rmSnapnStuff (){
	echo -e "\n\n\t\t\t[+] Starting SnapD destruction...\n"
	snappaks=("snap-store" "firefox" "gtk-common-themes" "bare" "snapd-desktop-integration" "gnome-3-38-2004" "core20")
	echo -e "\n\n\t\t\t [*] Removing snap packages.. Make sure all snap owned windows are closed\n"
	for i in "${snappaks[@]}";do
		printf "\n\t\t\t ---> Removing $i\n"
		snap remove --purge $i
	done
	
	
	# START COMMENT HERE__for non-interactive
	printf "\n\n\t\t\t [!] All Snaps should be gone besides snapd, verify below \n\n"
	##todo; if -z snap list continue
	echo -e "\n\n\t\t\t===> $(snap list) <===\n"
	echo "<!> Enter name of Snap pkg to delete, or N to continue:   "
	read todesnap;
	
	while [[ $todesnap != "N" ]]
	
	do
		echo -e "\n\t\t\t---> Removing ${todesnap}"
		snap remove --purge $todesnap
		
		echo "<!> Enter name of pkg to delete, or N to continue:   "
		read todesnap
	done
	# END COMMENT HERE__for non-interactive
	printf "\n\n\t\t\t [*] Taking care of snapd files\n\n"
	echo -e "\n\n\t\t\t---> Removing snapd cache\n"
	rm -rf /var/cache/snapd/
	echo -e "\n\n\t\t\t---> Removing snapd package\n"
	apt autoremove --purge snapd -y
	apt autoremove --purge gnome-software-plugin-snap
	echo -e "\n\n\t\t\t---> Removing snap user directories\n"
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

	
	printf "\n\n\t\t\t[+] Starting DNS edits\n"


	cp $dnsfile $dnsfile".bak"
	#cloudflare dns
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
	printf "\n\t\t\t ---> Original backed up to /etc/apt/sources.list.original\n"
	apt update 
	
}

getTools (){
	#update system
	regUpdate

	printf "\n\n [+] Starting Tools Install\n"
	
	#apt install ca-certificates <-- was needed for earlier releases, now present on default image
	dlChrome="${tempfordl}googleChrome"
	dlBurp="${tempfordl}BurpPro.sh"
	
	apt install wget
	#chrome
	printf "\n\n\t\t\t---> Installing Chrome \n\n"
	wget "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" -O $dlChrome
	dpkg -i $dlChrome


	#BurpSuite
	## community
	wget "https://portswigger-cdn.net/burp/releases/download?type=Linux" -O $dlBurp
	chmod +x $dlBurp
	/bin/sh $dlBurp
	
	printf "\n\t\t\t[*] Cleaning temp files\n"
	rm $dlBurp
	rm $dlChrome
	
	echo -e "\n\t\t\t[*] Adding external repos"
	#cherrytree
	echo -e "\n\t\t\t--> adding cherryTree repo\n"
	add-apt-repository ppa:giuspen/ppa -y
	
	#sublime text
	echo -e "\n\t\t\t--> adding sublimetext repo\n"
	echo -e "\n\n#sublime\ndeb https://download.sublimetext.com/ apt/stable/" >> /etc/apt/sources.list
	wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -

	#firefox
	add-apt-repository ppa:mozillateam/ppa -y
	# --> https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04
	firefoxpriority="""
Package: *
Pin: release o=LP-PPA-mozillateam
Pin-Priority: 1001

Package: firefox*
Pin: release o=Ubuntu
Pin-Priority: -1
"""
	firefoxupgrade='Unattended-Upgrade::Allowed-Origins:: '"LP-PPA-mozillateam:${DISTRIB_CODENAME}"';'
	firefoxprefsfile="/etc/apt/preferences.d/mozilla-firefox"
	firefoxupgradesfile="/etc/apt/apt.conf.d/51unattended-upgrades-firefox"
	echo -e "\n${firefoxpriority}" > $firefoxprefsfile
	#testing $firefoxprefsfile
	echo -e "\n${firefoxupgrade}" > $firefoxupgradesfile
	#testing $firefoxupgradesfile
	
	#wireshark noninteractive install
	echo "wireshark-common wireshark-common/install-setuid boolean false" | debconf-set-selections
	
	apt update
	
	printf "\n\t\t\t [+] Starting Install of other tools...\n"
	
	printf "\n\t\t\t\t ---> WireShark\n\n\n"
	DEBIAN_FRONTEND=noninteractive apt -y install wireshark
	
	printf "\n\t\t\t\t ---> Others\n\n\n"
	apt-get install -y curl nmap sublime-text cherrytree ssh apache2 net-tools git aircrack-ng gnome-shell-extensions make clementine 
	
	printf "\n\t\t\t\t ---> FireFox\n\n\n"
	apt-get install firefox -y
	
	
	#disabling servers that are autostart by default
	printf "\n\n\t\t\t[+] Disabling default daemons\n"
	defaultrunners=("apache2" "ssh")
	for i in "${defaultrunners[@]}";do
		systemctl stop $i
		systemctl disable $i 
	done

	echo -e "\n\t [+] Done installing Tools [+]\n\n"
	cleanin	

}

##########################################
############ OPTIONAL Tasks ##############

chngusername (){
	echo -e "\n\n\t\t\t [!] Changing username, Enter current username: "
	read curruser
	usermod -l $username $curruser; usermod -d /home/$username -m $username
}

##########################################


######### For VPN configurations #########

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

##########################################



######### Main Function #########

testing (){
	
	printf "\n\t\t [!] All good? [!] \n"
	printf "\n\t\t ---> printing ${1} \n\n"
	cat $1
	proceed
}

install (){
	# Main program
	echo -e "\n\n\t\t\t[+][+] Starting Install [+][+]\n\n "
	
	rmSnapnStuff
	changesources
	regUpdate
	DNSedit
	getTools
	usermodin
	printf "\n\n\n\n\t\t\t\t [!!] Done [!!] \n\n"
	printf "\n Jammy was weird on me with a bare metal AMD install with lvm encr\n"
	printf "\n What helped me was a Full powerdown, on post go straight to bios, then saveNContinue and back to jammy\n"
	printf "\n\t exiting..\n"
	
	#rebootin
	
}

########## Main Program ##########

# regular runs install func
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

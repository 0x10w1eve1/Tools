
# quickndirty script to automate the creation of an HTTPS apache server with a signed cert from LetEncrypt
# tested on Ubuntu 20.04 LTS and 21.1

#must be ran as root
if [[ $(id -u) -ne 0 ]]
then
	echo -e "\n [!!] Must be run as ROOT"
	exit
fi



printf "%b\n[+] Please enter the below info \n"
read -p "Site Domain:  " siteDomain
read -p "Site Admin:  " siteAdmin
read -p "localwebroot:  " localwebroot
# /var/www/your_domain
localwebroot+="${siteDomain}"

printf "%b\n[?] Enter to confirm\n"

echo -e "\nSite Domain-->\t ${siteDomain}"
echo -e "\nSite Admin-->\t ${siteAdmin}"
echo -e "\nWeb Root-->\t ${localwebroot}"
read continue

username=$(users)
#apache cert file
certFile="/etc/ssl/certs/apache-LetsEncrypt.cert"
certKey="/etc/ssl/private/apache-LetsEncrypt.key"
touch certFile
touch certKey
#vhost path
vhostfilename="$(echo $siteDomain|tr -d ".").conf"
vhostsslfilename="$(echo $siteDomain|tr -d ".")-SSL.conf"
vhostpath="/etc/apache2/sites-available/${vhostfilename}"
vhostsslpath="/etc/apache2/sites-available/${vhostsslfilename}"


#http vhost config
vhostconf="""
<VirtualHost *:80>

	ServerAdmin ${siteAdmin}
	ServerName ${siteDomain}
	ServerAlias ${siteDomain}
	DocumentRoot ${localwebroot}

	RewriteEngine On
	RewriteCond %{HTTPS} off
	RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
	
	ErrorLog /var/log/apache2/error.log
	CustomLog /var/log/apache2/access.log combined

	#block some bots
	RewriteCond %{HTTP_USER_AGENT} (CriOS) [NC]
	RewriteRule .* - [F,L]

</VirtualHost>

"""

#https vhost config
vhostconfSSL="""
<VirtualHost *:443>
	ServerAdmin ${siteAdmin}
	ServerName ${siteDomain}
	ServerAlias ${siteDomain}
	DocumentRoot ${localwebroot}

	SSLEngine on
	SSLCertificateFile ${certFile}
	SSLCertificateKeyFile ${certKey}
</VirtualHost>
"""

#index.html
siteIndex='''
<!DOCTYPE html>
<html>
<title> 0x10w1eve1 </title>
<body onload="sayhi()"></body>
<script>
setInterval(function() {alert("0x10w1eve1");},1010)
</script>
</html>
'''

# helper functions

getapache() {
	printf "%b\n[+] Installing apache and enabling mods.\n\n"
	apt update
	apt -y install apache2
	systemctl enable apache2
	ufw allow "Apache 2"
	a2enmod ssl 
	a2enmod headers   
	a2enmod rewrite
	systemctl restart apache2
}

getCert() {
	
	print "[+] Installing certbot..."
	printf "%b\n[+][+] Getting Certificate, follow prompts below.\n\n"
	apt update
	apt -y install certbot python3-certbot-apache
	certbot --apache
}


webrootSetup (){
	printf "%b\n[+] webroot setup\n\n"
	if ! [[ -d "$localwebroot" ]]
	then
		mkdir $localwebroot
	fi
	chown -R $username $localwebroot
	chmod -R 755 $localwebroot
	echo $siteIndex > $localwebroot"/index.html"

}

vhostSetup() {
	printf "%b\n[+] Vhost setup\n\n"

	#suppress apachectl configtest warning
	cp /etc/apache2/apache2.conf /etc/apache2/apache2.conf.bak
	echo "ServerName 127.0.0.1" >> /etc/apache2/apache2.conf

	echo -e "$vhostconf" > $vhostpath
	echo -e "$vhostconfSSL" > $vhostsslpath
	a2ensite $vhostfilename
	a2ensite $vhostsslfilename
	a2dissite "000-default.conf"
	a2dissite "default-ssl.conf"
	#generate a self signed cert to pass configtest
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $certKey -out $certFile
	printf "%b\n [+] Running config test"
	apachectl configtest
	systemctl reload apache2

}


install() {
	printf "%b\n[+] Starting Install...\n"
	getapache
	webrootSetup
	vhostSetup
	getCert
	printf "%b\n[+] Done..press Enter to reboot...\n"
	read toreboot
	reboot
}

install

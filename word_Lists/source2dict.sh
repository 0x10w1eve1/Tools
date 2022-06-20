#!/bin/bash

if [[ -z "$1" ]];then
	printf "\n\n\t\t little script with 2 functions, find and extract all archives and generate wordlist with all dirs/files\n\n\n"
	printf "\n\n\t\t Issues if the filename has spaces..ends up adding it to the dict as separate entries. "

	printf "\n\n\t\t [-] Usage: $0 <path with source files>\n\n"
	printf "\n\n\t\t [-] Usage: $0 <path with source files> <anything here to find and extract all files in specifid dir>\n"

	printf "\n\t\t [-] Wordlist is generated with name 10w1eve1_Wordlist.txt in cd \n\n"
	exit
else
	#remove trailing slash and save sources dir name to later cut out full path for dict
	sourcesname=$(basename $1)
	sourceDir=$(realpath $1)
fi



FindExtract() {

	printf "\n\n\t [!] Staring archive search and extraction\n"
	#extracts all *.zip archives to subfolders with names of these archives.
	for archive in $(find "$sourceDir" -type f -exec file \{\} +| grep "archive data"|cut -d ":" -f1);do
		
		filename=$(basename $archive)
		printf "\n\n\t\t\t [+] Extracting $filename\n\n"

		#getting output directory for unzipping
		#dirname=$(echo $archive|sed "s/$filename$//") #sed out jar filename from path
		# or use the actual dirname..learned of it after. lol
		dirname=$(dirname $archive)


		#pipe no to unzip for no overwrite. 
		yes n|unzip "$archive" -d "$dirname"

	done

	printf "\n\n\t [+] Done Extracting....\n"


}



GenWordlist() {

	printf "\n\n\t [+] Starting Wordlist Gen\n"
	temp="temp10w1eve1_Wordlist.txt"
	touch $temp
	outfile="10w1eve1_Wordlist.txt"
	touch $outfile


	for dirr in $(ls -N -R "$sourceDir"|grep ":");do
		dname=$(echo -e "$dirr"|sed 's/://')
		echo -e "${dname}/"|tee -a $temp
		fname=$(ls -N -R -d $dname/*)
		echo "$fname"|tr ' ' '\n' |tee -a $temp		

	done

	
	#remove empty lines, images, and basepath
	cat $temp|grep -E -v '*.img|*.svg|*.jpg|*.jpeg|*.gif|*.png'|grep . |sed "s/^.*$sourcesname//" |tee -a $outfile
	rm "$temp"

	printf "\n\n\t\t\t [!] Done....New Wordlist generated: $outfile\n\n"

}


## main

if ! [[ -z "$2" ]];then
	FindExtract
fi

GenWordlist



#!/bin/bash

if [[ -z "$1" ]];then
	printf "\n\n\t\t\t little script with 2 functions, find and extract all archives and generate wordlist with all dirs/files\n\n\n"

	printf "\n\n\t\t\t [-] Usage: $0 <path with source files>\n\n"
	printf "\n\n\t\t\t [-] Usage: $0 <path with source files> <anything here to find and extract all files in specifid dir>\n"

	printf "\n\t\t\t [-] Wordlist is generated with name 10w1eve1_Wordlist.txt in cd \n\n"
	exit
else
	sourceDir=$1

fi


FindExtract() {

	#extracts all *.zip archives to subfolders with names of these archives.
	for archive in $(find "$sourceDir" -type f -exec file \{\} +| grep "archive data"|cut -d ":" -f1);do
		
		filename=$(basename $archive)
		printf "\n\n\t\t\t [+] Extracting $filename\n\n"

		#getting output directory for unzipping
		dirname=$(echo $archive|sed "s/$filename$//") #sed out jar filename from path
		unzip "$archive" -d "$dirname"


		#$(echo -e $archive|cut -d "/" -f12-) #basedirs removed

	done


}



GenWordlist() {

	temp="temp10w1eve1_Wordlist.txt"
	touch $temp
	outfile="10w1eve1_Wordlist.txt"
	touch $outfile


	for dirr in $(ls -N -R $sourceDir|grep ":");do
		dname=$(echo $dirr|sed 's/://')
		echo $dname|cut -d "/" -f13-|tee -a $temp
		
		fname=$(ls -N -R -d $dname/*)
		echo $fname|tr ' ' '\n'|cut -d "/" -f13- |tee -a $temp		

	done

	#remove empty lines and images
	cat $temp|grep -E -v '*.img|*.svg|*.jpg|*.jpeg|*.gif|*.png'|grep . > $outfile
	rm $temp

	printf "\n\n\t\t\t [!] Done....New Wordlist generated: $outfile\n\n"

}


## main

if ! [[ -z "$2" ]];then
	FindExtract
fi

GenWordlist



#!/bin/bash

############################################################################
####					                                ####
####	Convert cherryTree export into a dir structure			####
####	*note: work in progress, works but needs code cleaning		####									
####	in cherrytree menu->export->txt->don't check 'in one file'	####
####					                                ####
#####0x10w1eve1#############################################################

## Working dirs

#if [[ -z "$1" ]];then
#	printf "\n\t\t\t [!] Usage: ./ctd2Git.sh <path to cherrytree export directory>\n\n"
#fi

basedir=`pwd`
cherrydir=$1
#cherrydir="${basedir}cherryExport/"

# get tree title and make dir to hold repo
treetitle=($(ls $cherrydir|grep "README"|head -n 1|cut -d "-" -f1))
#dir for git repo
gitdir="${basedir}${treetitle}/"
#TreeTitle--README.md.txt
readme="${cherrydir}${treetitle}--README.md.txt"  #($(ls $cherrydir|sed "s/$treetitle--//"|grep "^README"))


printf "\n\t\t [+] Creating Dir for Git Repo [+] \n\n"
if ! [[ -d "$gitdir" ]];then
	mkdir $gitdir
else
	printf "\n\t [!] Git directory exists, Replace or create New ? (r/n)) [!]\n\n"
	read continue
	if [[ "$continue"=="r" ]];then
		rm -rf $gitdir
		mkdir $gitdir
	elif [[ "$continue"=="n" ]]; then
		concat=`date +%m_%d_%y`
		gitdir="${basedir}${treetitle}_${concat}/"
		mkdir $gitdir
	else
		prinf "\n\t\t [!] Input unrecongnized, exiting..."
		exit
	fi
fi

printf "\n\t\t [--->] Relocating Main Repo README file\n\n"
# get main readme for repo
mv $readme "${gitdir}README.md"	# removed to avoid dups, copy this back to source cherrydir when done

#get rid of empty file representing tree name
# note2self, you could just leave it and use it to create the treetile dir in gitdir
# try later, you'd have to get the treetile by other means or just not sed out the title from each node
# so it would be nodes=echo $file grep txt double slash to space
rm "${cherrydir}${treetitle}.txt"

for file in $(ls $cherrydir);do

	#make array to use as directory struct
	# assumed that each node was exported with tree title in name ex; MYTREE--parentnode-childnode
	# Note2self: sed the '-' into something else first to avoid spluting files with tools names like recon-ng
	NODES=($(echo $file |sed "s/^$treetitle--//"|sed 's/\.txt//'|tr '\-\-' ' '))
	
	cwd=$gitdir
	length=${#NODES[@]}
	endLoop=$(( $length - 1 ))
	#last index is the name of the final childnode 

	childNodeFileName=${NODES[$endLoop]}
	# contents of final childnode
	childNodeData=$cherrydir$file

	#sort parents and children
	for ((i = 0 ; i < $endLoop;i++));do
		if (( $i != 0 ));then
			prev=$(( $i - 1 ))
			prevcwd=$cwd
		fi
		#keep updating cwd as you move down the rabbit hole. 
		currnode=${NODES[$i]}
		cwd+=${NODES[$i]}
		
		# parent node with content gets written as a file becuase of how last node is detected
		# note2self; if cat node is empty, mkdir node else touch node
		# this way if birthed new children, just rm node instead of renaming and mving. 
		if ! [[ -d "$cwd" ]] && ! [[ -f "$cwd" ]];then
			cwd+="/"
			mkdir $cwd
		elif [[ -f "$cwd" ]]; then
			newname="${currnode}-info.txt"   #check if all these new info files are empty, if they are, just rename as readme maybe
			newfile="${cwd}-info.txt"

			mv $cwd $newfile
			cwd+="/"
			mkdir $cwd 
			mv $prevcwd$newname $cwd 
		elif [[ -d "$cwd" ]]; then
			cwd+="/"
		else
			:
		fi

	
	done
	cp $childNodeData $cwd$childNodeFileName
	
	
done


LOGS=Beforestats=$(cat <<-END
	childNodeFileName: ${childNodeFileName}
	childNodeData: ${childNodeData}
	i: ${i}
	lastelement: ${endLoop}
	cwd: ${cwd}\
	newname: ${newname} 
	END
	)
LOGS2=$(cat <<-END
		childNodeFileName: ${childNodeFileName}
		childNodeData: ${childNodeData}
		i: ${i}
		lastelement: ${endLoop}
		cwd: ${cwd}\
		newname: ${newname} 
		END
		)

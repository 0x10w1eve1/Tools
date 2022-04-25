target=$1
cat $1 |grep -v "#" |cut -d ":" -f2 |cut -d " " -f2 > newrob.txt
for i in $(cat newrob.txt);do echo "https://${target}${i}" >> to_scan.txt;done
rm newrob.txt
mv $target files_robots/

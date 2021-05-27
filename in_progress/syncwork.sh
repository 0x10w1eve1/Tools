basedir="/root/10wGit/in_progress/"
Arsenalbase="/media/root/Arsenal/"
inprog="${Arsenalbase}in_progress"
backup="/backfiles/"
mkdir $backup
cp -r $basedir $backup
echo "[+] syncing the below files..."
ls $basedir
echo "----------------------------------"
mv $inprog.7z $backup/old.7z
7z a -t7z -mx=9 $inprog.7z $basedir/*
echo "[!] all files synced, press ENTER to delete temp backup [!]"
read confirmation
rm -rf $backup

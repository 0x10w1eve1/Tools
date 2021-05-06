
badchars = [',','.',':']

newwordlist = open('s3cretwordlist','w')
with open('s3cret.txt') as email:
	for line in email:
		for word in line.split():
			for ch in badchars:
				if ch in word:
					word = word.replace(ch,'')
			
			newwordlist.write(word+'\n')
			




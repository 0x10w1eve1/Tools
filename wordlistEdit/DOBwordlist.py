from itertools import permutations
import sys
import itertools

newlist=[]

perms = [''.join(p) for p in permutations(['1988','12','9'])]
#print perms

perms2=[''.join(p) for p in permutations(['1988','12','09'])]
#print perms2

#generate mixed cases for the word december

pots = ['december']
combos=[]
for e in pots:
	combos += map(''.join, itertools.product(*((c.upper(), c.lower()) for c in e)))

#perms for each mixed case word with '09'
for i in combos:
	for x in ([''.join(p) for p in permutations(['1988',i,'09'])]):
		newlist.append(x)


#perms for each mixed case word with '9'
for i in combos:
	for x in ([''.join(p) for p in permutations(['1988',i,'9'])]):
		newlist.append(x)

for i in perms:
	newlist.append(i)

for i in perms2:
	newlist.append(i)

with open('sviridovdob','w') as f:
	for i in newlist:
		f.write(i+'\n')
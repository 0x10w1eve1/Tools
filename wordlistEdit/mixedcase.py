#creates a wordlist of all mixed case possibiliites for a word, and appends a domain. change as  u need.

import itertools

pots = ['members','old','registered','registeredmembers','oldsite']
combos=[]
for e in pots:
	combos += map(''.join, itertools.product(*((c.upper(), c.lower()) for c in e)))

with open('memcombos','w') as f:
	for i in combos:
		i += '.streetfighterclub.htb'+'\n'
		f.write(i)

from itertools import permutations
import sys
import itertools

password=''
keyword=''
numbers=''
simple=[]




#get all combos of mixed cases for the password
mixed_password=[]
mixed_password+=map(''.join,itertools.product(*((c.upper(),c.lower()) for c in password)))


#get all combos of mixed cases for the keyword
mixed_keyword=[]
mixed_keyword+=map(''.join,itertools.product(*((c.upper(),c.lower()) for c in keyword)))

#generate all possible permutations for the combination password,keyword,numbers
permss=[]
for p in mixed_password:
	for k in mixed_keyword:
		permss+=permutations([p,k,numbers])

for p in mixed_password:
	for k in mixed_keyword:
		permss+=permutations([p,k])

for p in mixed_password:
	permss+=permutations([p,numbers])

for k in mixed_keyword:
	permss+=permutations([k,numbers])


#results comes in the format [(a,b,c),(b,a,c)]
#so you join to make it ['abc','bac']
newlist=[]
newlist+=["".join(p) for p in permss]

for i in newlist:
	print i
'''
#[''.join(p) for p in permutations([p,k,'123'])]



#or i in mixed_password:
#     permss+=permutations([i,'123'])
#>>> newlist+=["".join(p) for p in permss]

#get all combos of mixed cases for the password
mixed_password=[]
mixed_password+=map(''.join,itertools.product(*((c.upper(),c.lower()) for c in password)))
for p in mixed_password:
	simple+=permutations([password,keyword,numbers])

for p in mixed_password:
	simple+=permutations([password,numbers])

for p in mixed_password:
	simple+=permutations([keyword,numbers])

for p in mixed_password:
	simple+=permutations([password,keyword])

simple_list=[]
simple_list+=["".join(p) for p in simple]
for i in simple_list:
	print i

	'''


### 0x10w1eve1 ###

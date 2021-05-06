#convert hex to decimal
import sys

if len(sys.argv) != 2:
        print "USAGE: python hex2char.py <hex numbers, ex: \x6C\x65\x6E\x67,\x6C\x65\x6E\x67,\x6C\x65\x6E\x67"
	sys.exit()

inputt = sys.argv[1].split('x')
inputt.remove('')

finalstring = ''.join(str(chr(int(l,16))) for l in inputt)
print finalstring

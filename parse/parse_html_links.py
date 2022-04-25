from bs4 import BeautifulSoup
import sys

html=open(sys.argv[1],'r')

soup = BeautifulSoup(html,"html.parser")

for a in soup.find_all('script'):
	print(a.get('src'))


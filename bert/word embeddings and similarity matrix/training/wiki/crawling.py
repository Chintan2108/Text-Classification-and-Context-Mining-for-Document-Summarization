from bs4 import BeautifulSoup

temp = open('withtags.txt', 'r')

data = ''

for line in temp:
    data += line

soup = BeautifulSoup(data)



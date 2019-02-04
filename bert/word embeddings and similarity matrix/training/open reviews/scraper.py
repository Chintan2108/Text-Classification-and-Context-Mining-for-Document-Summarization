import requests, time
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import PyPDF2

def web(page,WebUrl):
    if(page>0):
        url = WebUrl
        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        for link in s.findAll('a', {'class':'s-access-detail-page'}):
            tet = link.get('title')
            print(tet)
            tet_2 = link.get('href')
            print(tet_2)

def test():
    url = 'https://openreview.net/notes?invitation=ICLR.cc%2F2018%2FConference%2F-%2FBlind_Submission&offset=0&limit=1000'
    df = pd.DataFrame(requests.get(url).json()['notes']) # Each row in this data frame is a paper.
    df.to_csv('file_name', sep='\t', encoding='utf-8')
    #print(df)
    forum_content = []
    for i, forum_id in list(enumerate(df.forum)): # Each forum_id is a review, comment, or acceptance decision about a paper.
        forum_content.append(requests.get('https://openreview.net/notes?forum={}&trash=true'.format(forum_id)).json())
        time.sleep(.3)
        df['forumContent'] = pd.Series(forum_content)
    print(forum_content)

#test()

def new():
    url = 'https://openreview.net/notes?invitation=ICLR.cc%2F2018%2FConference%2F-%2FBlind_Submission&offset=0&limit=1000'
    df = pd.DataFrame(requests.get(url).json()['notes']) # Each row in this data frame is a paper.
    df.to_csv('file_name.csv', sep='\t', encoding='utf-8')
    #print(type(df))
    #print(df['invitation'])
    #for row in df['invitation']:
        #print(row)
    forum_content = []
    for i, forum_id in list(enumerate(df.forum)): # Each forum_id is a review, comment, or acceptance decision about a paper.
        print(forum_id)
        forum_content.append(requests.get('https://openreview.net/notes?forum={}&trash=true'.format(forum_id)).json())
        time.sleep(.3)
        df['forumContent'] = pd.Series(forum_content)
    print(df['forumContent'])
    print(forum_content)

new()

def downloadPDF():
    url = 'https://openreview.net/pdf/c49ec54d1c4c4909e73f88a0279bbec2c9e86d6d.pdf'  
    urllib.request.urlretrieve(url, './Papers_PDF/p1.pdf')  

def readPDF():
    pdfFileObject = open('./Papers_PDF/p1.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    count = pdfReader.numPages
    for i in range(count):
        page = pdfReader.getPage(i)
        print(page.extractText())

#readPDF()
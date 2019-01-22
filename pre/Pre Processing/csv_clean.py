# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 14:56:33 2018

@author: Chintan Maniyar
"""

import pandas as pd
from autocorrect import spell
import re
#from nltk.corpus import stopwords

def clean(sentence):
    if len(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', sentence)) > 0:
        return sentence.split('\n')[0]
    
    raw = []
    temp = sentence.split('\n')
    for s in temp:
        raw += s.split(':')
    sentence = ''

    for s in raw:
        if len(s) > 0:
            sentence += s
    
    raw = sentence.split('.')
    sentence = ''
    for s in raw:
        if len(s) > 1:
            sentence += s + '.'
    
    return sentence
'''    
def spellCheck(sentence):
    
    corrected = ''
    splits = sentence.split(' ')
    for s in splits:
        if(s == splits[len(splits)-1]):
            corrected += spell(s)
        else:
            corrected += spell(s) + ' '
    
    return corrected
'''
xls = pd.ExcelFile('Responses_All About the RMP2031.xlsx')
df = pd.read_excel(xls, 'Form responses 1', header=[0,1])

headers = df.keys()[1:]
headers = headers[:len(headers)-3]

for h in headers[1::2]:
    filename = str(h).split(',')[0].split('\'')[1] + '.txt'
    
    slist = []
    for sentence in df[h]:
        if type(sentence) == str:
            sentence = clean(sentence)
            if len(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', sentence)) > 0:
                slist.append(sentence)
                #print(sentence)
                #print()
            else:
                slist += sentence.split('.')
    
    file = open(filename, 'w', encoding='utf-8')
    index = 1
    print("Writing " + filename + '...')
    for sentence in slist:
        if len(sentence) > 2:
            file.write(str(index) + '- ' + sentence.lstrip() + '.\n')
            index += 1
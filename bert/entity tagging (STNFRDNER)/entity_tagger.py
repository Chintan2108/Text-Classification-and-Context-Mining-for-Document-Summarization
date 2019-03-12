from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import os

DIR_PATH = './../word embeddings and similarity matrix/data/comments'

st = StanfordNERTagger('E:/Me/IITB/Work/CIVIS/ML Approaches/entity tagging/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'E:/Me/IITB/Work/CIVIS/ML Approaches/entity tagging/stanford-ner-2018-10-16/stanford-ner-3.9.2.jar',
                        encoding='utf-8')

for domain in os.listdir(DIR_PATH):
    corpora = open(os.path.join(DIR_PATH,domain)).readlines()
    for response in corpora:
        print(response)
        response = word_tokenize(response)
        classified_response = st.tag(response)
        print(classified_response)
        print('*******************************************')
    break

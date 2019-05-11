from gensim.models import KeyedVectors
from nltk.corpus import stopwords
import numpy as np


wordmodelfile = 'E:/Me/IITB/Work/CIVIS/ML Approaches/word embeddings and similarity matrix/GoogleNews-vectors-negative300.bin'
wordmodel = KeyedVectors.load_word2vec_format(wordmodelfile, binary = True, limit=200000)

keywords = {
    'environment': ['pollution', 'plant trees', 'tree', 'open spaces', 'forests', 
                    'streams', 'lakes', 'water harvesting', 'recycled water',
                    'solar energy'],
    
    'housing': ['housing', 'affordable housing', 'economically weaker sections', 
                'floor area ratio', 'EWS housing'],
    
    'Traffic': ['traffic', 'Metro phase 1 and 2', 'Ring road', 'taxi', 'electric vehicle',
                'bike path', 'footpath', 'bus', 'outstation traffic', 'logistic hubs', 
                'heavy vehicles', 'trucks']
}

env_comments = open('Environment.txt', 'r', encoding='utf-8').readlines()
housing_comments = open('Housing.txt', 'r', encoding='utf-8').readlines()
traffic_comments = open('Traffic.txt', 'r', encoding='utf-8').readlines()

#####################Environment################################

distances = []

print('Initializing distances...')
for comment in env_comments:
    comments = list(filter(None, comment.lower().split('.')))
    for single_comment in comments:
        print(single_comment)
        wmd = []
        for keyword in keywords['environment']:

            cwords = single_comment.split()
            swords = keyword.split()

            cwords = set(cwords)    
            for word in cwords.copy():
                if word in stopwords.words('english'):
                    cwords.remove(word)
            
            swords = set(swords)
            for word in swords.copy():
                if word in stopwords.words('english'):
                    swords.remove(word)

            cwords = list(cwords)
            swords = list(swords)

            distance = wordmodel.wmdistance(cwords, swords)
            wmd.append(distance)
            # print(swords)
            # print(cwords)
            # print(distance)
            #print('==============')
        distances.append(wmd)
        minIndex = np.array(wmd).argmin()
        print(keywords['environment'][minIndex], wmd[minIndex]) 
        print('******************************\n\n')
print('Done.')

# print('\n\nPrinting Analysis...\n')
# for comment in env_comments:
#     comments = list(filter(None, comment.lower().split('.')))
#     for wmds,single_comment in zip(distances,comments):
#         print(single_comment)
#         print('-------------')
#         print(wmds)
#         wmds = np.array(wmds)
#         minIndex = wmds.argmin()
#         print(keywords['environment'][minIndex])
#         print(wmds[minIndex])
#         print('*************************************************')

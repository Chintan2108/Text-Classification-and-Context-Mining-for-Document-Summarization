from gensim.models import KeyedVectors
from nltk.corpus import stopwords
import numpy as np
# import pandas as pd

# df = pd.read_excel('HWest Responses_Venter.xlsx')
# feedbacks = df['Feedback']

# temp = open('./test_data.txt', 'w', encoding='utf-8')

# for feedback in feedbacks:
#     if type(feedback) == str:
#         print(feedback)
#         temp.writelines(feedback.split('\n')[0] + '\n')

# temp.close()


wordmodelfile = 'E:/Me/IITB/Work/CIVIS/ML Approaches/word embeddings and similarity matrix/GoogleNews-vectors-negative300.bin'
wordmodel = KeyedVectors.load_word2vec_format(wordmodelfile, binary = True, limit=200000)

keywords = {
    'hw': ['bedbugs', 'cctv', 'pipeline', 'Open spaces', 'gutter', 'garbage',
                    'rats', 'mice', 'robbery', 'theft', 'passage', 'galli', 'lane',
                    'light', 'bathrooms not clean', 'toilets not clean', 'play area', 'mosquito', 'fogging'],
}

hw_comments = open('test_data.txt', 'r', encoding='utf-8').readlines()


#####################hw test_data################################

distances = []

print('Initializing distances...')
for comment in hw_comments:
    comments = list(filter(None, comment.lower().split('.')))
    for single_comment in comments:
        if len(single_comment) == 1:
            continue
        print(single_comment)
        wmd = []
        for keyword in keywords['hw']:

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
        print(keywords['hw'][minIndex], wmd[minIndex]) 
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

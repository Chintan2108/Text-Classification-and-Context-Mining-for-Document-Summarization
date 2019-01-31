from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import wordnet as wn 
from nltk.corpus import stopwords
import sys
from gensim.models import KeyedVectors
import warnings
import numpy as np
import time

def similarityIndex(s1, s2, wordmodel):
    '''
    To compare the two sentences for their similarity using the gensim wordmodel 
    and return a similarity index
    '''
    if s1 == s2:
        return 1.0

    s1words = s1.split()
    s2words = s2.split()

    s1words = set(s1words)    
    for word in s1words.copy():
        if word in stopwords.words('english'):
            s1words.remove(word)
    
    s2words = set(s2words)
    for word in s2words.copy():
        if word in stopwords.words('english'):
            s2words.remove(word)

    s1words = list(s1words)
    s2words = list(s2words)    

    s1set = set(s1words)
    s2set = set(s2words)

    vocab = wordmodel.vocab
    
    if len(s1set & s2set) == 0:
        return 0.0
    for word in s1set.copy():
        if (word not in vocab):
            s1words.remove(word)
    for word in s2set.copy():
        if (word not in vocab):
            s2words.remove(word)
    
    return wordmodel.n_similarity(s1words, s2words)


def getCats(file):
    '''
    To read the category file of the domain and return a list of all
    the categories in the form of sentences
    '''  

    references = []
    for sentence in file:
        references.append(sentence.split('\n')[0])
    
    print('Mining categories...')
    return references

def vectorInit():
    '''
    Preparing a tfidf matrix of all the response sentences of one domain
    '''  
    environment = open('.\\data\\environment.txt','r')
    vect = TfidfVectorizer(min_df=1)
    sentences = []

    for sentence in environment:
        sentences.append(sentence.split('-')[1])

    tfidf = vect.fit_transform(sentences)

    tm = np.array((tfidf * tfidf.T).A)
    np.save('.\\tfidf vector\\tfidf_matrix.npy', tm)
    np.savetxt('.\\tfidf vector\\tfidf_matrix.txt', tm)
    print('tfidf vectors saved.')


if __name__ == "__main__":
    '''Main function/ driver function'''
    stats = open('stats.txt', 'w', encoding='utf-8')

    st = time.time()
    wordmodelfile = 'E:\\Me\\IITB\\Work\\CIVIS\\ML Approaches\\word embeddings and similarity matrix\\GoogleNews-vectors-negative300.bin.gz'
    wordmodel = KeyedVectors.load_word2vec_format(wordmodelfile, binary = True)
    et = time.time()
    s = 'Word embedding loaded in %f secs.' % (et-st)
    print(s)
    stats.write(s + '\n')

    #testing the tfidf
    st = time.time()
    vectorInit()
    et = time.time()
    s = 'Tfidf vector initilaized in %f secs. (with function overhead)' % (et-st)
    print(s)
    stats.write(s + '\n')

    #files
    environment = []
    fh = open('.\\data\\Environment.txt', 'r')
    environment = fh.readlines()
    rows = len(environment)

    categories = open('.\\data\\env_c.txt', 'r')
    categories = getCats(categories)
    columns = len(categories)

    #saving the scores in a similarity matrix
    #initializing the matrix with -1 to catch dump/false entries
    st = time.time()
    similarity_matrix = [[-1 for c in range(columns)] for r in range(rows)]
    et = time.time()
    s = 'Similarity matrix initialized in %f secs.' % (et-st)
    print(s)
    stats.write(s + '\n')

    row = 0
    st = time.time()
    for response in environment:
        column = 0
        for category in categories:
            similarity_matrix[row][column] = similarityIndex(response.split('-')[1].lstrip(), category, wordmodel)
            column += 1
        row += 1
    et = time.time()
    s = 'Similarity matrix saved in %f secs. ' % (et-st)
    print(s)
    stats.write(s + '\n')

    #saving the matrix
    save_matrix = np.array(similarity_matrix)
    np.save('.\\score matrix\\env_matrix.npy',save_matrix)
    np.savetxt('.\\score matrix\\env_matrix.txt',save_matrix)
    print('score matrix saved.')

    #categorizing the responses based on the scores
    fh1 = open('.\\results\\cat1.txt', 'w', encoding='utf-8')
    fh2 = open('.\\results\\cat2.txt', 'w', encoding='utf-8')
    fh3 = open('.\\results\\cat3.txt', 'w', encoding='utf-8')
    fh4 = open('.\\results\\cat4.txt', 'w', encoding='utf-8')
    fh5 = open('.\\results\\cat5.txt', 'w', encoding='utf-8')
    fh6 = open('.\\results\\cat6.txt', 'w', encoding='utf-8')
    fh7 = open('.\\results\\cat7.txt', 'w', encoding='utf-8')
    fh8 = open('.\\results\\cat8.txt', 'w', encoding='utf-8')
    fh9 = open('.\\results\\cat9.txt', 'w', encoding='utf-8')
    fh10 = open('.\\results\\cat10.txt', 'w', encoding='utf-8')
    fh11 = open('.\\results\\cat11.txt', 'w', encoding='utf-8')
    fh12 = open('.\\results\\cat12.txt', 'w', encoding='utf-8')
    fh13 = open('.\\results\\cat13.txt', 'w', encoding='utf-8')
    catFileHandles = [fh1, fh2, fh3, fh4, fh5, fh6, fh7, fh8, fh9, fh10, fh11, fh12, fh13]
        
    print('Writing category files...')
    for catName,fh in zip(categories, catFileHandles):
        fh.write(catName)
        fh.write('\n=====================================')
        fh.write('\n\n')

    print('Populating category files...')
    response_index = 0
    for score_row,response in zip(similarity_matrix,environment):
        max_sim_index = np.array(score_row).argmax()
        catFileHandles[max_sim_index].write(response)

    print('done.')
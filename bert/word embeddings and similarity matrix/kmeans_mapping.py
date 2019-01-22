from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import wordnet as wn 
from nltk.corpus import stopwords
import sys
from gensim.models import KeyedVectors
import warnings
import numpy as np

#globals
environment = open('Environment.txt', 'r')
categories = open('env_c.txt', 'r')

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
    global environment
    vect = TfidfVectorizer(min_df=1)
    sentences = []

    for sentence in environment:
        sentences.append(sentence)

    tfidf = vect.fit_transform(sentences)

    print((tfidf * tfidf.T).A)

if __name__ == "__main__":
    wordmodelfile = 'E:\Me\IITB\Work\CIVIS\ML Approaches\word embeddings and similarity matrix\GoogleNews-vectors-negative300.bin.gz'
    wordmodel = KeyedVectors.load_word2vec_format(wordmodelfile, binary = True)

    #files
    environment = open('Environment.txt', 'r')
    columns = len(environment.readlines())

    categories = open('env_c.txt', 'r')

    references = getCats(categories)
    rows = len(references)

    #saving the scores in a similarity matrix
    #initializing the matrix with -1 to catch dump/false entries
    similarity_matrix = [[-1 for c in range(columns)] for r in range(rows)]

    row = 0
    for category in references:
        column = 0
        environment = open('Environment.txt', 'r')
        for response in environment:
            similarity_matrix[row][column] = similarityIndex(response.split('-')[1].lstrip(), category, wordmodel)
            column += 1
        row += 1

    #saving the matrix
    save_matrix = np.array(similarity_matrix)
    np.save('env.npy',save_matrix)
    np.savetxt('env_txt.txt',save_matrix)

    print('score matrix saved.')
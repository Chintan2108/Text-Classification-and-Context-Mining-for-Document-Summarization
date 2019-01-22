from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import wordnet as wn 
from nltk.corpus import stopwords
import sys
from gensim.models import KeyedVectors
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

#globals
environment = open('Environment.txt', 'r')

def similarityIndex(s1, s2, wordmodel):
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




def vectorInit():  
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

    print('a' in wordmodel.vocab)

    reference = 'To improve Bengaluru environment, the municipality will plant trees on major roads, make tree planting mandatory for all new buildings and create more parks open spaces.'
    s = 'Their should small jungle in every part of Bangalore the technique of this jungle is used by HAL where a small 10*20 place will be filled with trees and managed in such a way that their is no place inside by setting up of small mini size to huge trees in a orderly way this will fight pollution and save greenery.'

    sim_score = []
    for sentence in environment:
        score = similarityIndex(reference, sentence.split('-')[1].lstrip(), wordmodel)
        sim_score.append(score)

    #print(similarityIndex(reference, s, wordmodel))
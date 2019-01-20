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
    
    stopset = set(stopwords.words('english'))
    
    for word in s1words:
        if word in stopset:
            s1words.remove(word)
    
    for word in s2words:
        if word in stopset:
            s2words.remove(word)
    

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
    wordmodelfile = 'GoogleNews-vectors-negative300.bin.gz'
    wordmodel = KeyedVectors.load_word2vec_format(wordmodelfile, binary = True)

    print('a' in wordmodel.vocab)

    reference = 'To improve Bengaluru environment, the municipality will plant trees on major roads, make tree planting mandatory for all new buildings and create more parks open spaces.'
    
    for sentence in environment:
        print(similarityIndex(reference, sentence.split('-')[1].lstrip(), wordmodel))
        print(sentence)
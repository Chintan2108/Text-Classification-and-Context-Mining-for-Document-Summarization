from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from gensim.models import KeyedVectors
from threading import Semaphore
from networkx.algorithms.components.connected import connected_components
import os
import json
import pickle
import warnings
import networkx
import time
import numpy as np

def toGraph(l):
    '''
    It takes in a list of lists and returns a graph object, 
    assigning nodes and edges from each sub-list object
    '''
    G = networkx.Graph()
    for part in l:
        G.add_nodes_from(part)
        G.add_edges_from(toEdges(part))
    return G

def toEdges(l):
    '''
    It treats args(1) 'l' as a graph and returns (implicitly) it's edges 
    '''
    it = iter(l)
    last = next(it)

    for current in it:
        yield last, current
        last = current 

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


def categorizer():
    '''
    driver function,
    returns model output mapped on the input corpora as a dict object
    '''
    stats = open('stats.txt', 'w', encoding='utf-8')

    st = time.time()
    wordmodelfile = 'E:/Me/IITB/Work/CIVIS/ML Approaches/word embeddings and similarity matrix/GoogleNews-vectors-negative300.bin'
    wordmodel = KeyedVectors.load_word2vec_format(wordmodelfile, binary = True)
    et = time.time()
    s = 'Word embedding loaded in %f secs.' % (et-st)
    print(s)
    stats.write(s + '\n')

    #filepaths
    responsePath = './data/comments/'
    categoryPath = './data/sentences/'
    responseDomains = os.listdir(responsePath)
    categoryDomains = os.listdir(categoryPath)
    
    #dictionary for populating the json output
    results = {}
    for responseDomain, categoryDomain in zip(responseDomains, categoryDomains):
        #instantiating the key for the domain
        domain = responseDomain[:-4]
        results[domain] = {}

        print('Categorizing %s domain...' % domain)

        temp = open(responsePath + responseDomain, 'r', encoding='utf-8-sig')
        responses = temp.readlines()
        rows = len(responses)

        temp = open(categoryPath + categoryDomain, 'r', encoding='utf-8-sig')
        categories = temp.readlines()
        columns = len(categories)
        categories.append('Novel')

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
        for response in responses:
            column = 0
            for category in categories[:-1]:
                similarity_matrix[row][column] = similarityIndex(response.split('-')[1].lstrip(), category, wordmodel)
                column += 1
            row += 1
        et = time.time()
        s = 'Similarity matrix populated in %f secs. ' % (et-st)
        print(s)
        stats.write(s + '\n')

        print('Initializing json output...')
        for catName in categories:
            results[domain][catName] = []

        print('Populating category files...')
        for score_row,response in zip(similarity_matrix,responses):
            max_sim_index = len(categories)-1
            if np.array(score_row).sum() > 0:
                max_sim_index = np.array(score_row).argmax()
            results[domain][categories[max_sim_index]].append(response)
        print('Completed.\n')
        
        #initializing the matrix with -1 to catch dump/false entries for subcategorization of the novel responses
        no_of_novel_responses = len(results[domain]['Novel'])
        st = time.time()
        similarity_matrix = [[-1 for c in range(no_of_novel_responses)] for r in range(no_of_novel_responses)]
        et = time.time()
        s = 'Similarity matrix for subcategorization of novel responses for %s domain initialized in %f secs.' % (domain, (et-st))
        print(s)
        stats.write(s + '\n')
        

        #populating the matrix
        row = 0
        for response1 in results[domain]['Novel']:
            column = 0
            for response2 in results[domain]['Novel']:
                if response1 == response2:
                    column += 1
                    continue
                similarity_matrix[row][column] = similarityIndex(response1.split('-')[1].lstrip(), response2.split('-')[1].lstrip(), wordmodel)
                column += 1
            row += 1
        
        setlist = []
        index = 0
        for score_row, response in zip(similarity_matrix, results[domain]['Novel']):
            max_sim_index = index
            if np.array(score_row).sum() > 0:
                max_sim_index = np.array(score_row).argmax()
            if set([response, results[domain]['Novel'][max_sim_index]]) not in setlist:
                setlist.append([response, results[domain]['Novel'][max_sim_index]])
            index += 1
        
        G = toGraph(setlist)
        setlist = list(connected_components(G))
        
        novel_sub_categories = {}
        index = 0
        for category in setlist:
            novel_sub_categories[index] = list(category)
            index += 1

        results[domain]['Novel'] = novel_sub_categories

        print('***********************************************************')
    with open('out_new.json', 'w') as temp:
        json.dump(results, temp)
    return results

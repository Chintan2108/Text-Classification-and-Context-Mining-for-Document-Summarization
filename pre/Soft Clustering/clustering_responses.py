#import numpy as np 
import pandas as pd 
import nltk
from nltk.stem.snowball import SnowballStemmer
import re
#import os
#import codecs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from matplotlib import pyplot as plt
from sklearn.manifold import MDS
#import mpld3 

def getSentences(filePath):
    print('Mining responses...')
    
    f = open(filePath, 'r')
    sentences = []
    for s in f:
        sentences.append(s.split('-')[1].split('\n')[0])
    
    print('Mining Responses done...')
    
    return sentences


def tokenizeAndStem(text):
    print('Tokenizing and stemming responses...')
    
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    
    for token in tokens:
        if(re.search('[a-zA-Z]', token)):
            filtered_tokens.append(token)
    
    stemmer = SnowballStemmer('english')
    stems = [stemmer.stem(t) for t in filtered_tokens]
    
    print('Done tokenizing and stemming responses...')
    
    return stems


def Tokenize(text):
    print('Tokenizing responses...')
    
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    
    for token in tokens:
        if(re.search('[a-zA-Z]', token)):
            filtered_tokens.append(token)
    
    print('Done tokenizing responses...')
    return filtered_tokens


def clusterResponses(numClusters, matrix, terms):
    print('Attempting clustering...')
    
    km = KMeans(n_clusters = numClusters)
    
    km.fit(matrix)

    clusters = km.labels_.tolist()
    
    #save the model as a pickle file
    joblib.dump(km, 'response_cluster.pkl')
    
    #uncomment this to load the pickle file when you run for the nth time (n>1)
    #km = joblib.load(km, 'response_cluster.pkl')
    
    clusters = km.labels_.tolist()
    
    #indexing
    diffs = {'response': responses, 'cluster': clusters }
    frame = pd.DataFrame(diffs, index = [clusters], columns = ['response', 'cluster'])
    
    for i in range(numClusters):
        
        print('Cluster %d responses' % i)
        for response in frame.loc[i]['response'].values.tolist():
            print('%s ' % response )
        print('===========================================================')
    return clusters


def visClusters(clusters, responses):
    MDS()
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

    xs, ys = pos[:, 0], pos[:, 1]
    
    cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e', 5: '#34ff22', 6: '#3eef34', 7: '#112fff', 8: '#999fff'}
                      
    cluster_names = {0: 'Cluster0', 
                     1: 'Cluster1',
                     2: 'Cluster2',
                     3: 'Cluster3',
                     4: 'Cluster4',
                     5: 'Cluster5',
                     6: 'Cluster6',
                     7: 'Cluster7'}
    
    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=responses))
    
    groups = df.groupby('label')
    
    fig, ax = plt.subplots()
    ax.margins(0.05)
    
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, label=cluster_names[name], color=cluster_colors[name], mec='none')
        ax.set_aspect('auto')
        ax.tick_params(\
            axis= 'x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off')
        ax.tick_params(\
            axis= 'y',         # changes apply to the y-axis
            which='both',      # both major and minor ticks are affected
            left='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelleft='off')
        
    ax.legend(numpoints=1)  #show legend with only 1 point
    
    #add label in x,y position with the label as the film title
    for i in range(len(df)):
        ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)  
    
        
        
    plt.show() #show the plot



if __name__ == "__main__":
    responses = getSentences('Traffic.txt')
    
    responses_stemmed = []
    responses_tokenized = []
    
    for r in responses:
        allwords_stemmed = tokenizeAndStem(r)
        responses_stemmed.extend(allwords_stemmed)
        
        allwords_tokenized = Tokenize(r)
        responses_tokenized.extend(allwords_tokenized)
    
    w2vecFrame = pd.DataFrame({'words': responses_tokenized}, index = responses_stemmed)
    #print stats
    print(str(w2vecFrame.shape[0]) + ' elements in the Frame')
    
    #initialize vecrotizer
    tfidf_v = TfidfVectorizer(max_df=0.8,
                              max_features=200000,
                              min_df=0.2,
                              stop_words='english',
                              use_idf=True,
                              tokenizer=tokenizeAndStem,
                              ngram_range=(1,3))
    
    #time matrix
    tfidf_matrix = tfidf_v.fit_transform(responses)
    print(tfidf_matrix.shape)
    
    terms = tfidf_v.get_feature_names()
    
    #evaluating the similarity of the responses
    dist = 1 - cosine_similarity(tfidf_matrix)
    
    #saving the clusters
    clusters = clusterResponses(8, tfidf_matrix, terms)
    
    #indexing
    diffs = {'response': responses, 'cluster': clusters }
    frame = pd.DataFrame(diffs, index = [clusters], columns = ['response', 'cluster'])
    
    #printing no of responses per cluster
    print(frame['cluster'].value_counts())
    
    #visClusters(clusters, responses)
    
    

    
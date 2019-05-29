import pandas as pd
import numpy as np

def trainSS(paper, tuples=40000):
    '''
    Samples sentence pair training data with labels 
    '''
    trainColumns = ['A', 'B', 'label', 'title']
    trainData = pd.DataFrame(columns=trainColumns)

    filename = './SSglobalTrainData_80.csv'

    titles = open('./wikiArticleNames.txt').readlines()

    for row in range(tuples):
        paperIndex = np.random.randint(0, len(papers))


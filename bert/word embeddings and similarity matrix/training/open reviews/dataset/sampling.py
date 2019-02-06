import pandas as pd
import pickle, random, sys
import numpy as np

columns = ['A', 'B', 'label']
sampledData = pd.DataFrame(columns=columns)
index = 0

def paperToList(compoundPaper, para=False):
    '''
    This function takes in a paper as a list of paragraphs as an argument
    and returns a the paper as a list of sentences
    arg para is to toggle between a paper(already segregated) and a paragraph(to be segregated) in the compoundPaper arg
    '''
    paper = []
    if para:
        for line in compoundPaper.split('. '):
            paper.append(line.lstrip())
    else:
        for para in compoundPaper:
            for line in para.split('. '):
                paper.append(line.lstrip())
    
    paper = list(filter(None, paper))

    return paper

def samplePaper(paper, epoch=100):
    '''
    This function takes in a list of sentences of a paper and 
    samples the dataframe with sentence pairs and the label
    arg epoch is the no of iterations for each paper
    '''
    global sampledData, index

    paperListed = paperToList(paper)
    
    for para in paper:
        paraListed = paperToList(para, para=True)
        CLS = paraListed[0]
        for x in range(epoch):
            if np.random.random_integers(0,1):
                sampledData.loc[index + x] = [random.choice(paraListed), CLS, 1]
            else:
                sampledData.loc[index + x] = [random.choice(paraListed), random.choice(paperListed), 0]
        index += epoch

    print('Data sampled successfully.\n')

if __name__ == "__main__":
    '''
    Main/ driver function
    sys args are - 1. sampling epoch for each paper
                   2. no of papers to sample data for
    eg: python sampling.py 100 1 -> samples 100 iterations for 1 paper
    '''
    papers = []
    with open('papers.pkl', 'rb') as temp:
        papers = pickle.load(temp)
    
    threshold = 1
    limit = int(sys.argv[2])
    for paper in papers:
        if threshold > limit:
            break
        print('Paper ' + str(threshold))
        samplePaper(paper, epoch=int(sys.argv[1]))
        threshold += 1
    sampledData.to_csv('SampledData.csv', encoding='utf-8')
    print('Sampled data saved as a csv successfully.')
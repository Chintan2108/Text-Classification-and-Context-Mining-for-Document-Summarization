import pandas as pd
import pickle, random, sys
import numpy as np


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


def trainingData(papers, tuples=10000):
    '''
    This function saves the train data as with features as ['A','B','label']
    A -> random sentence a random para from any paper
    B -> first sentence of that para; label = 1
    B -> random sentence from that paper; label = 0
    '''
    trainColumns = ['A','B','label']
    trainData = pd.DataFrame(columns=trainColumns)

    for row in range(tuples):
        paperIndex = np.random.randint(0,len(papers))
        paraIndex = np.random.randint(0, len(papers[paperIndex]))

        paperListed = paperToList(papers[paperIndex])
        paraListed = paperToList(papers[paperIndex][paraIndex], para=True)

        CLS = paraListed[0]

        if np.random.random_integers(0,1):
            trainData.loc[row] = [random.choice(paraListed), CLS, 1]
        else:
            trainData.loc[row] = [random.choice(paraListed), random.choice(paperListed), 0]

    trainData.to_csv('trainData.csv', encoding='utf-8')
    print('Training data saved successfully.')


def testingData(papers, reviews, tuples=10000):
    '''
    This function saves the train data as with features as ['A','B','label']
    A -> random sentence from any paper
    B -> random para of a random review for that paper
    '''
    testColumns = ['A', 'B']
    testData = pd.DataFrame(columns=testColumns)

    for row in range(tuples):
        paperIndex = np.random.randint(0,len(papers))
        paperListed = paperToList(papers[paperIndex])

        review = list(filter(None,random.choice(reviews[paperIndex])))

        testData.loc[row] = [random.choice(paperListed), random.choice(review)]

    testData.to_csv('testData.csv', encoding='utf-8')
    print('Testing data saved successfully.')


if __name__ == "__main__":
    '''
    Main/ driver function
    sys args are - 1. -train OR -test to toggle between train data and test data
                   2. -no_of_tuples to define the no of tuples for the train/test dataset
    eg: python sampling.py -train -100 ->  This will create 100 tuples train data 
    '''
    papers = []
    with open('papers.pkl', 'rb') as temp:
        papers = pickle.load(temp)
    
    reviews = []
    with open('reviews.pkl', 'rb') as temp:
        reviews = pickle.load(temp)
    
    if len(sys.argv) == 3:
        if sys.argv[1] == '-train':
            trainingData(papers, int(sys.argv[2]))
        elif sys.argv[1] == '-test':
            testingData(papers, reviews, int(sys.argv[2]))
        else:
            print('Invalid arguments\n\
            sys args are\n' +  
            '1. -train OR -test to toggle between train data and test data\n' + 
            '2. -no_of_tuples to define the no of tuples for the train/test dataset\n' +
            'eg: python sampling.py -train -100 ->  This will create 100 tuples train data')
    else:
        print('Invalid arguments\n\
            sys args are\n' +  
            '1. -train OR -test to toggle between train data and test data\n' + 
            '2. -no_of_tuples to define the no of tuples for the train/test dataset\n' +
            'eg: python sampling.py -train -100 ->  This will create 100 tuples train data')        

    print('Done.')
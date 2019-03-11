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
        for line in compoundPaper.split('.'):
            line = line.rstrip()
            line = line.lstrip()
            paper.append(line)
    else:
        for para in compoundPaper:
            for line in para.split('. '):
                paper.append(line.lstrip())
    
    paper = list(filter(None, paper))

    return paper


def trainingData(papers, tuples=10000, overall=False):
    '''
    This function saves the train data as with features as ['A','B','label']
    A -> random sentence a random para from any paper
    B -> first sentence of that para; label = 1
    B -> random sentence from that paper; label = 0;  for args overall=False
    B -> random sentence from any paper; label = 0;  for args overall=True
    '''
    trainColumns = ['A','B','label']
    trainData = pd.DataFrame(columns=trainColumns)
    if overall:
        filename = 'globalTrainData.csv'
    else:
        filename = 'localTrainData.csv'

    for row in range(tuples):
        paperIndex = np.random.randint(0,len(papers))
        paraIndex = np.random.randint(0, len(papers[paperIndex]))

        paperListed = paperToList(papers[paperIndex])
        paraListed = paperToList(papers[paperIndex][paraIndex], para=True)

        CLS = paraListed[0]
        A = random.choice(paraListed)
        label = 0
        
        if np.random.random_integers(0,1):
            paperListed = [CLS]
            label = 1
        else:
            if overall:
                paperIndex = np.random.randint(0,len(papers))
                paraIndex = np.random.randint(0, len(papers[paperIndex]))
                paperListed = paperToList(papers[paperIndex])
                
        B = random.choice(paperListed)
        trainData.loc[row] = [A, B, label]

    trainData.to_csv(filename, encoding='utf-8')
    print('Training data saved successfully.')


def testingData(papers, reviews, A='sentence', B='para'):
    '''
    This function saves the test data with features as ['A','B']
    A -> random sentence from any paper; B -> random sentence from all the reviews of that paper
    A -> random sentence from any paper; B -> random para from all the reviews of that paper
    A -> random para from any paper; B -> random sentence from all the reviews of that paper
    A -> random para from any paper; B -> random para from all the reviews of that paper
    No of tuples = (len(parent(A)) * len(parent(B)))*No_of_papers
    '''
    testColumns = ['A', 'B']
    testData = pd.DataFrame(columns=testColumns)
    
    paperIndex = 0
    rowIndex = 0
    paperListed = []
    filename = './dataset/'
    for paper in papers:
        if A == 'sentence':
            if paperIndex == 0:
                filename += 'S'
            paperListed = paperToList(paper)
        elif A == 'para':
            if paperIndex == 0:
                filename += 'P'
            paperListed = paper

        if paperIndex==0 and B=='para':
            filename += 'P'
        #getting a list of paragraphs for all reviews for paper papers[index]
        reviewListed = []
        for review in reviews[paperIndex]:
            for para in review:
                reviewListed.append(para)
        reviewListed = list(filter(None, reviewListed))

        if B == 'sentence':
            #getting sentences of all paras of the review in reviewListed
            if paperIndex == 0:
                filename += 'S'
            reviewSentences = []
            for para in reviewListed:
                reviewSentences.extend(paperToList(para, para=True))
            reviewListed = reviewSentences
        paperIndex += 1

        for A in paperListed:
                for B in reviewListed:
                    testData.loc[rowIndex] = [A, B]
                    rowIndex += 1
        print('Paper - %d, Row - %d' % (paperIndex, rowIndex))
    print('Populated the test data successfully.')

    testData.to_csv(filename+'testData.csv', encoding='utf-8')
    print('Testing data saved successfully as %s.' % filename)


if __name__ == "__main__":
    '''
    Main/ driver function
    sys args are -  For Trainig:
                    1. -train to prepare the train data
                    2. -no_of_tuples to define the no of tuples for the train dataset
                    eg: python sampling.py -train -100 ->  This will create 100 tuples train data

                    For Testing:
                    1. -test to prepare the test dataset (no of tuples are implicit based on the no of papers and the paper content)
                    2. -para -sentence OR -para -para OR -sentence -para OR -sentence -sentence 
                        The above args are to toggle between the selection of feature(A & B) characteristics for the test data
    '''
    papers = []
    with open('papers.pkl', 'rb') as temp:
        papers = pickle.load(temp)
    
    reviews = []
    with open('reviews.pkl', 'rb') as temp:
        reviews = pickle.load(temp)
    
    if (len(sys.argv)==4):
        if sys.argv[1]=='-train':
            if sys.argv[2]=='local':
                trainingData(papers, int(sys.argv[3]))
            elif sys.argv[2]=='global':
                trainingData(papers, int(sys.argv[3]), overall=True)
        elif sys.argv[1] == '-test':
            testingData(papers, reviews, sys.argv[2], sys.argv[3])
        else:
            print('Invalid arguments\n\
            sys args are\n' +  
            '1. -train OR -test to toggle between train data and test data\n' + 
            '2. no_of_tuples to define the no of tuples for the train dataset and -para AND -sentence flags for the test dataset\n' +
            'eg: python sampling.py -train global 100 ->  This will create 100 tuples train data with global sampling\n'+
            'eg: python sampling.py -test para sentence ->  This will create test data in the format [A, B] where\n' + 
            '\t A -> random para from any paper; B -> random sentence from all the reviews of that paper')
    else:
        print('Invalid arguments\n\
            sys args are\n' +  
            '1. -train OR -test to toggle between train data and test data\n' + 
            '2. -no_of_tuples to define the no of tuples for the train dataset and -para AND -sentence flags for the test dataset\n' +
            'eg: python sampling.py -train global 100 ->  This will create 100 tuples train data with global sampling\n'+
            'eg: python sampling.py -test para sentence ->  This will create test data in the format [A, B] where\n' + 
            '\t A -> random para from any paper; B -> random sentence from all the reviews of that paper')        

    print('Done.')
from process_pdf import PdfConverter
import pandas as pd
import random, sys
import numpy as np

FILEPATH = 'Civis_Bangalore Master Plan_Content.pdf'

def trainingData(proposal, tuples=10000):
    '''
    This function creates training data from the 2d list of proposal and 
    its domains and saves it with features [A, B, label]
    A --> random sentence from random domain of the proposal
    B --> first sentence of that domain (50/100); label = 1
    B --> random sentence from random domain of the proposal (50/100); label = 0
    '''
    trainColumns = ['A', 'B', 'label']
    df = pd.DataFrame(columns=trainColumns)

    for row in range(tuples):
        domain = random.choice(proposal)

        CLS = domain[0]
        A = random.choice(domain)
        label = 0

        if np.random.random_integers(0,1):
            B = CLS
            label = 1
        else:
            B = random.choice(random.choice(proposal))
        
        df.loc[row] = [A, B, label]
    
    df.to_csv('CIVIS_trainData.csv')
    print('Training data saved succesfully.')

if __name__ == "__main__":
    converter = PdfConverter(FILEPATH)

    # converter = PdfConverter(file_path=FILEPATH)``
    # converted_text_str = converter.PDFToText()
    # text = converter.splitByPara(converted_text_str, FILEPATH)

    proposal = []

    temp = open('Kitty.txt', 'r', encoding='utf-8')
    for lines in temp.readlines():
        domain = []
        for line in lines.split('. '):
            domain.append(line)
        proposal.append(domain)
    
    if (len(sys.argv)==3 or len(sys.argv)==2) and sys.argv[1] == '-train':
        if (len(sys.argv))==3: 
            trainingData(proposal, int(sys.argv[2]))
        elif (len(sys.argv)) == 2:
            trainingData(proposal)
        else:
            print('Invalid arguments\n\
            sys args are\n' +  
            '1. -train to save the train data\n' + 
            '2. no_of_tuples to define the no of tuples for the train dataset\n' +
            'eg: python sampling.py -train 100 ->  This will create 100 tuples train data\n')
    else:
        print('Invalid arguments\n\
        sys args are\n' +  
        '1. -train to save the train data\n' + 
        '2. no_of_tuples to define the no of tuples for the train dataset\n' +
        'eg: python sampling.py -train 100 ->  This will create 100 tuples train data\n')
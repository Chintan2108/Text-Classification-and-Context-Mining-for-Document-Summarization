import os, pickle
import process_pdf

def saveReviews():
    '''
    This function saves the reviews per paragraph, per review, per paper
    in the form of a 3d list pickled to a dataset
    '''
    path = './Review Params/Reviews/'
    papers = os.listdir(path)
    papers.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    print(papers)

    dataset = []
    for item in papers:
        paper = []
        with open(path + item, 'rb') as temp:
            reviews = pickle.load(temp)
            #'reviews list'
            for review_item in reviews:
                review = []
                #'single review'
                for para in review_item.split('\n\n'):
                    #p'single para'
                    if para is not None:
                        review.append(para.replace('\n',''))
                paper.append(review)
        dataset.append(paper)
    
    #pickling the dataset for reviews
    with open('./dataset/reviews.pkl', 'wb') as temp:
        pickle.dump(dataset, temp)
    print('Reviews dataset pickled successfully.')

def savePapers():
    '''
    This function pickles the 2d list returned by the processPDF function
    '''
    papers = process_pdf.processPDF('./Papers_PDF/')
    
    with open('./dataset/papers.pkl', 'wb') as temp:
        pickle.dump(papers, temp)
    print('Papers dataset pickled successfully.')
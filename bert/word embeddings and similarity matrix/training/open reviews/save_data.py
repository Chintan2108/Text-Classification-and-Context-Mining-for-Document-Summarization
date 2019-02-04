import os, pickle

def saveReviews():
    '''
    This function saves the reviews per paragraph, per review, per paper
    in the form of a 3d list pickled to a dataset
    '''
    path = './Review Params/Reviews/'
    papers = os.listdir(path)
    papers.sort()
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
                    review.append(para.replace('\n',''))
                paper.append(review)
        dataset.append(paper)
    
    #pickling the dataset for reviews
    with open('./dataset/reviews_dataset.pkl', 'wb') as temp:
        pickle.dump(dataset, temp)
    print('reviews dataset pickled successfully.')


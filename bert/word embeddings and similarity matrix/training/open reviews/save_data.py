import os, pickle

def saveReviews():
    path = './Review Params/Reviews'
    reviews = os.listdir(path)
    reviews.sort()
    print(reviews)

    dataset = []
    
saveReviews()
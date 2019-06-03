import wikipedia, pickle, sampling
import os
import pandas as pd


def getContent(titleList):
    '''
    This function takes in the article title as an argument, fetches article 
    content from the wikipedia website and saves the content in a text file
    Pickles it as a 2d list - list of articles as a list of paras
    '''
    articles = []

    index = 0
    for title in titleList:
        article = []
        content = wikipedia.page(title.split('\n')[0])
        for line in content.content.splitlines():
                if 'See also' in line:
                    break
                if (len(line)) > 40:
                    article.append(line)
        articles.append(article)
        print('%s saved successfully' % title.split('\n')[0])
        index += 1 

    with open('./big dataset/61-80articles.pkl', 'wb') as temp:
        pickle.dump(articles, temp)
    print('%d articles pickled successfully.' % index)

def saveData(para = False):
    '''
    This function saves the data as 2d and 3d pickles, if para is true then talk comments are sampled as a para otherwise as a sentence 
    '''
    pids = []
    responses = []
    TALK_COMMENTS_PATH = './dataset/test/talkComments'
    if para:
        pickleFileName = 'talkComments_S.pkl'
        pidsPickle = 'talkpids_S.pkl'
    else:
        pickleFileName = 'talkComments.pkl'
        pidsPickle = 'talkpids.pkl'
    replacements = ['.', '?',]
    for talk in os.listdir(TALK_COMMENTS_PATH):
        if talk[-3:] == 'csv':
            talkpid = []
            talkComments = []
            article = []
            temp = pd.read_csv(os.path.join(TALK_COMMENTS_PATH, talk))['text']
            parentid = pd.read_csv(os.path.join(TALK_COMMENTS_PATH, talk))['parent_id']
            for x,y in zip(temp, parentid):
                if str(x) != 'nan':
                    if para:
                        for r in replacements:
                            x = x.replace(r, '. ')
                        x = sampling.paperToList(x, para=para)
                        for xs in x:
                            talkComments.append(xs)
                            talkpid.append(y)
                    else:
                        talkComments.append(x)
                        talkpid.append(y)

            for talkComment in talkComments:
                temp = []
                temp.append(talkComment)
                article.append(temp)
            responses.append(article)
            pids.append(talkpid)
            print('%s pickled successfully.' % talk)

    with open(os.path.join('./dataset/test', pickleFileName), 'wb') as temp:
        pickle.dump(responses, temp)
    
    with open(os.path.join('./dataset/test',pidsPickle), 'wb') as temp:
        pickle.dump(pids, temp)

def testDataSP():
    '''
    '''
    articles = []
    with open('./dataset/test/articles.pkl', 'rb') as temp:
        articles = pickle.load(temp)

    talkComments = []
    with open('./dataset/test/talkComments.pkl', 'rb') as temp:
        talkComments = pickle.load(temp)
    
    talkpids = []
    with open('./dataset/test/talkpids.pkl', 'rb') as temp:
        talkpids = pickle.load(temp)

    sampling.testingData(articles, talkComments, talkpids)

def testDataSS():
    '''
    '''
    articles = []
    with open('./dataset/test/articles.pkl', 'rb') as temp:
        articles = pickle.load(temp)

    talkComments = []
    with open('./dataset/test/talkComments_S.pkl', 'rb') as temp:
        talkComments = pickle.load(temp)
    
    talkpids = []
    with open('./dataset/test/talkpids_S.pkl', 'rb') as temp:
        talkpids = pickle.load(temp)

    sampling.testingData(articles, talkComments, talkpids)

def trainPP():
    '''
    '''
    articles = []
    with open('./dataset/train/articles.pkl', 'rb') as temp:
        articles = pickle.load(temp)

    articlesP = []
    for article in articles:
        articleP = []
        articlelines = []
        for para in article:
            articlelines.extend(para.split('. '))
        new_para = ''
        length = 0
        for line in (articlelines):
            if int(length/10) > 10:
                articleP.append(new_para)
                new_para = ''
                length = 0
            
            new_para += line + '. '
            length += len(line.split())
                
        articlesP.append(articleP)
        

    with open('./dataset/train/articlesP.pkl', 'wb') as temp:
        pickle.dump(articlesP, temp)
    
    print('Creating Training data...')
    articles = []
    with open('./dataset/train/articlesP.pkl', 'rb') as temp:
        articles = pickle.load(temp)
    sampling.trainingData(articles, overall=True, para=False)
    
    return

def testDataPP():
    '''
    '''
    articles = []
    with open('./dataset/test/articles.pkl', 'rb') as temp:
        articles = pickle.load(temp)

    talkComments = []
    with open('./dataset/test/talkComments.pkl', 'rb') as temp:
        talkComments = pickle.load(temp)
    
    talkpids = []
    with open('./dataset/test/talkpids.pkl', 'rb') as temp:
        talkpids = pickle.load(temp)

    sampling.testingData(articles[:5], talkComments[:5], talkpids[:5], AA='para', BB='para', toggle=True)

if __name__ == "__main__":
    '''
    main/ driver function
    '''
    testDataSP()
    #articlesList = open('./big dataset/train/61-80wikiArticleNames.txt', 'r', encoding='utf-8').readlines()
    #getContent(articlesList)
    # saveData(para=True)
    
    # articles = []
    # with open('./dataset/articles.pkl', 'rb') as temp:
    #     articles = pickle.load(temp)
    
    # articles = []
    # temp_articles = []

    # with open('./big dataset/1-20articles.pkl', 'rb') as temp:
    #     temp_articles = pickle.load(temp)
    # articles.extend(temp_articles)

    # with open('./big dataset/21-40articles.pkl', 'rb') as temp:
    #     temp_articles = pickle.load(temp)
    # articles.extend(temp_articles)

    # with open('./big dataset/41-60articles.pkl', 'rb') as temp:
    #     temp_articles = pickle.load(temp)
    # articles.extend(temp_articles)

    # with open('./big dataset/61-80articles.pkl', 'rb') as temp:
    #     temp_articles = pickle.load(temp)
    # articles.extend(temp_articles)

    # sampling.trainingData(articles, tuples=80000, overall=True)
    
    # trainPP()
    # print('\n\n*********************\nSampling Test Data\n')
    # testDataPP()
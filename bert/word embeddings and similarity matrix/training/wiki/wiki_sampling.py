import wikipedia, pickle, sampling
import sampling, os
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

    with open('./dataset/articles.pkl', 'wb') as temp:
        pickle.dump(articles, temp)
    print('%d articles pickled successfully.' % index)

def saveData(para = False):
    '''
    This function saves the data as 2d and 3d pickles 
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

if __name__ == "__main__":
    '''
    main/ driver function
    '''
    testDataSP()
    # articlesList = open('./dataset/test/wikiTestArticles.txt', 'r', encoding='utf-8').readlines()
    # getContent(articlesList)
    # saveData(para=True)
    
    # articles = []
    # with open('./dataset/articles.pkl', 'rb') as temp:
    #     articles = pickle.load(temp)
    
    # sampling.trainingData(articles, tuples=10000, overall=True)
    
import pickle

def sampleTestSQUAD():
    '''
    This function samples a test dataset as a list for SQUAD-like pretraining
    Format of row per article, per para: [article_para, [all talk comments], article_name, row_id]
    Format of articles.pkl for a single article: [para1, para2, para3, ...]
    '''

    articles = []
    with open('./dataset/test/articles.pkl', 'rb') as temp:
        articles = pickle.load(temp)

    talkComments = []
    with open('./dataset/test/talkComments.pkl', 'rb') as temp:
        talkComments = pickle.load(temp)
    
    tempTalkComments = []
    for article in talkComments:
        temp = []
        for comment in article:
            temp.extend(comment)
        tempTalkComments.append(temp)
    
    talkComments = tempTalkComments

    titles = open('./dataset/test/wikiTestArticles.txt', 'r', encoding='utf-8').readlines()

    SQUAD = []
    tupleID = 0
    for article, article_name, comments in zip(articles, titles, talkComments):
        print('Processing %s...' % article_name.split('\n')[0])
        start_tuple = tupleID
        for para in article:
            SQUAD.append([para, comments, article_name.split('\n')[0], tupleID])
            tupleID += 1
        print('Successfully sampled %d tuples.\n' % (tupleID - start_tuple))
    
    with open('./big dataset/test/SQUAD_TEST_DATA.pkl', 'wb') as temp:
        pickle.dump(SQUAD, temp)
    print('\n********************\nSample stored as SQUAD.pkl.')

sampleTestSQUAD()
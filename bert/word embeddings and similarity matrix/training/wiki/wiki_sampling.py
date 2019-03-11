import wikipedia, pickle
import sampling


def getContent(titleList):
    '''
    This function takes in the article title as an argument, fetches article 
    content from the wikipedia website and saves the content in a text file
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



if __name__ == "__main__":
    '''
    main/ driver function
    '''
    # articlesList = open('wikiArticles.txt', 'r').readlines()
    # getContent(articlesList)
    
    articles = []
    with open('./dataset/articles.pkl', 'rb') as temp:
        articles = pickle.load(temp)
    
    sampling.trainingData(articles, tuples=10000, overall=True)
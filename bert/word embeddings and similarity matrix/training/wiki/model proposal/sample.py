import wikipedia, pickle, os
import pandas as pd

WHITELIST = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 01234567890')

def talkComments():
    '''
    Store talk comments
    '''
    comments = []
    articleName = []
    TALK_COMMENTS_PATH = './raw/tcnew'
    articles = os.listdir(TALK_COMMENTS_PATH)
    df = pd.DataFrame(columns=['Comments', 'Article'])
    globalRowCount = 0
    for article in articles:
        if article.endswith('csv'):
            tc = pd.read_csv(os.path.join(TALK_COMMENTS_PATH, article))
            comments.extend(tc['text'])
            for i in range(len(tc['text'])):
                articleName.append(article.split('.')[0].replace('_',' '))
                comments[i + globalRowCount] = ''.join(filter(WHITELIST.__contains__, str(comments[i + globalRowCount])))
                comments[i + globalRowCount] = article.split('.')[0].replace('_',' ') + '\t' + comments[i + globalRowCount] 
            globalRowCount += (i+1)
            print(comments[globalRowCount-1])
            print('Parsed %s successfully.' % article)
            print('*******************')
    df['Comments'] = comments
    df['Article'] = articleName
    df.to_csv('./processed/annotatedComments.csv')

    with open('./processed/articleComments.pkl', 'wb') as temp:
        pickle.dump(comments, temp)


def articles():
    '''
    Store article sentences
    '''
    articleSentences = []
    articleName = []
    titles = open('articleNames.txt', 'r', encoding='utf-8').readlines()
    # titles = open('./../dataset/train/wikiTrainArticles.txt', 'r', encoding='utf-8').readlines()
    df = pd.DataFrame(columns=['Sentence', 'Article'])
    globalRowCount = 0
    for title in titles:
        articleContent = wikipedia.page(title.split('\n')[0])
        for line in articleContent.content.splitlines():
            if 'See also' in line:
                    break
            if len(line) == 0:
                continue
            lines = line.split('. ')
            articleSentences.extend(lines)
            for i in range(len(lines)):
                articleSentences[i + globalRowCount] = title.split('\n')[0] + '\t' + articleSentences[i + globalRowCount]
                articleName.append(title.split('\n')[0])
            globalRowCount += (i + 1)
        print(articleSentences[globalRowCount-1])
        print('Parsed %s successfully.' % title.split('\n')[0])
        print('*******************')
    df['Sentences'] = articleSentences
    df['Article'] = articleName
    df.to_csv('./processed/annotatedSentences.csv')

    with open('./processed/articleSentences.pkl', 'wb') as temp:
        pickle.dump(articleSentences, temp)

talkComments()
articles()
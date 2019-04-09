import wikipedia, pickle, os
import pandas as pd

def talkComments():
    '''
    Store talk comments
    '''
    comments = []
    articleName = []
    TALK_COMMENTS_PATH = './raw/tc'
    articles = os.listdir(TALK_COMMENTS_PATH)
    df = pd.DataFrame(columns=['Comments', 'Article'])
    for article in articles:
        if article.endswith('csv'):
            tc = pd.read_csv(os.path.join(TALK_COMMENTS_PATH, article))
            comments.extend(tc['text'])
            for i in range(len(tc['text'])):
                articleName.append(article.split('.')[0].replace('_',' '))
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
    titles = open('./../dataset/train/wikiTrainArticles.txt', 'r', encoding='utf-8').readlines()
    df = pd.DataFrame(columns=['Sentence', 'Article'])
    for title in titles:
        articleContent = wikipedia.page(title.split('\n')[0])
        for line in articleContent.content.splitlines():
            if 'See also' in line:
                    break
            if len(line) == 0:
                continue
            lines = line.split('. ')
            for i in range(len(lines)):
                articleName.append(title.split('\n')[0])
            articleSentences.extend(lines)
        print('Parsed %s successfully.' % title.split('\n')[0])
        print('*******************')
    df['Sentences'] = articleSentences
    df['Article'] = articleName
    df.to_csv('./processed/annotatedSentences.csv')

    with open('./processed/articleSentences.pkl', 'wb') as temp:
        pickle.dump(articleSentences, temp)

talkComments()
    articles()
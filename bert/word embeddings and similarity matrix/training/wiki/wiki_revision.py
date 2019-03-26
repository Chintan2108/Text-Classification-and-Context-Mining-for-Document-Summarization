import xml.etree.ElementTree as ET
import requests
import pandas as pd

def getRevisions(pageTitle, limit=500):
    '''
    This function takes in two args - article title and limit 
    The title fetches the revision history and limit sets threshold on the no of previous revisions to fetch'
    and saves a csv file for that request with all the edit comments and other
    necessary details
    '''
    url = "https://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&rvlimit=%s&rvprop=ids|flags|timestamp|user|userid|size|sha1|contentmodel|comment|parsedcomment|content|tags|flagged&titles=%s" % (limit, pageTitle)
    
    print('Fetching api response...')
    response = requests.get(url)

    response = ET.fromstring(response.content)
    print('Parsing XML...')

    detailsColumns = ['revID','parentID','user','uid','timestamp','comment','content']
    revisions = pd.DataFrame(columns=detailsColumns)
    
    index = 0
    for revision in response[2][0][0][0].findall('rev'):
        revisions.loc[index] = [revision.get('revid'),
                                revision.get('parentid'),
                                revision.get('user'),
                                revision.get('userid'),
                                revision.get('timestamp'),
                                revision.get('comment'),
                                revision[1].text]
        index += 1
    
    filename = ''
    article = pageTitle.split()
    if len(article) > 1:
        for syllable in article:
            filename += syllable + '_'
        filename = filename[:-1]
    else:
        filename = pageTitle
    revisions.to_csv('./dataset/test/editComments/%s.edit_Comments.csv' % filename, encoding='utf-8')
    print('%s_editComments.csv saved successfully.\n' % pageTitle)

if __name__ == "__main__":
    '''
    Main/ driver function
    '''
    titles = open('./dataset/test/wikiTestArticles.txt', 'r', encoding='utf-8').readlines()

    for title in titles:
        getRevisions(title.split('\n')[0])
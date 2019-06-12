import requests, os, pickle
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

def getDiff(revID):
    '''
    This function compares the revID and the previous version of the article
    and returns two lists namely added lines and deleted lines
    '''
    url = 'https://en.wikipedia.org/wiki/?diff=%s' % str(revID)

    #open with GET method 
    resp=requests.get(url)

    #http_respone 200 means OK status 
    if resp.status_code==200: 
        print("Successfully opened the web page") 
      
        # we need a parser,Python built-in HTML parser is enough . 
        soup=BeautifulSoup(resp.text,'html.parser')     
        # l is the list which contains all the text i.e news  
        dl=soup.find_all("td", {"class":"diff-deletedline"})
        al=soup.find_all("td", {"class":"diff-addedline"}) 

        addedLines = []
        deletedLines = []

        for texttag in dl:
            text = texttag.find_all("div")
            for t in text:
                addedLines.append(t.text)
        
        for texttag in al:
            text = texttag.find_all("div")
            for t in text:
                deletedLines.append(t.text)

        return addedLines, deletedLines
    else: 
        print("Error")
        return False

def toDate(date):
    '''
    This function returns a datetime object, given a string date in the format 
    yyyy-mm-dd
    '''
    date = [int(i) for i in date.split('-')]

    return datetime(date[0], date[1], date[2])



def mapping(talkComment, editComment):
    '''
    This function creates a mapping between the two versions of a wiki article
    using the diff and returns a composite mapping in the form of a list
    '''
    print('mapping %s & %s . . .' % (talkComment, editComment))

    MARGIN = timedelta(15)
    
    talk_text = []
    m_diff = []
    p_diff = []

    tc = pd.read_csv(talkComment)
    ec = pd.read_csv(editComment)

    for text, user, date in zip(tc['text'], tc['user'], tc['date']):
        if user in list(ec['user']):
            ec_index = list(ec['user']).index(user)
            tc_date = toDate(date[:10])
            ec_date = toDate(ec['timestamp'][ec_index][:10])
            print(tc_date, ec_date)
            if (tc_date - MARGIN) <= ec_date and ec_date <= (tc_date + MARGIN):
                talk_text.append(text)
                temp_p_diff, temp_m_diff = getDiff(ec['revID'][ec_index])
                p_diff.append(temp_p_diff)
                m_diff.append(temp_m_diff)
    print('done')
    print('*********************************************\n')

    return [talk_text, m_diff, p_diff]


if __name__ == "__main__":
    '''
    main/ driver function
    '''

    TALK_COMMENTS_PATH = './test/talkComments'
    EDIT_COMMENTS_PATH = './test/editComments'

    MAPPING = []

    for batch in os.listdir(TALK_COMMENTS_PATH):
        for talkComment, editComment in zip(os.listdir(os.path.join(TALK_COMMENTS_PATH, batch))[0::2], os.listdir(os.path.join(EDIT_COMMENTS_PATH, batch))):
            if talkComment.endswith('csv') and editComment.endswith('csv'):
                MAPPING.append(mapping(os.path.join(TALK_COMMENTS_PATH, batch, talkComment), os.path.join(EDIT_COMMENTS_PATH, batch, editComment)))
    
    with open('./MAPPING.pkl', 'wb') as temp:
        pickle.dump(MAPPING, temp)
    
    print('\nMapping written successfully.')

# MAPPING = []

# MAPPING.append(mapping('./test/talkComments/1-20\Deloitte.comment_list.csv', './test/editComments/1-20\Deloitte.edit_Comments.csv'))

# with open('./MAPPING.pkl', 'wb') as temp:
#     pickle.dump(MAPPING, temp)

# print('\nMapping written successfully.')
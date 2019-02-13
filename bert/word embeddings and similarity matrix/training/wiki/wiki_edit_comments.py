import urllib.request
import re, xmltodict
import pandas as pd

def getRevisions(pageTitle):
    '''
    This function takes in the Wikipedia article title as an argument and 
    returns a list of all the revisions made on that article till date with a 
    threshold of 500 instances; wiki dum api is used
    '''

    url = "https://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&rvlimit=500&titles=" + pageTitle
    revisions = []     #list of all accumulated revisions
    next = ''    #information for the next request
    while True:
        response = urllib.request.urlopen(url + next).read()  #web request
        response = response.decode('utf-8')
        revisions += re.findall('<rev [^>]*>', response)  #adds all revisions from the current request to the list

        cont = re.search('<continue rvcontinue="([^"]+)"', response)
        if not cont:    #break the loop if 'continue' element missing
            break

        next = "&rvcontinue=" + cont.group(1)     #gets the revision Id from which to start the next request
    
    return revisions


if __name__ == "__main__":
    '''
    Main/ driver function
    '''

    titles = ['Coffee', 'Astrology', 'Football', 'Astronomy']
    columns = ['user', 'comment', 'timestamp']

    for title in titles:
        print('Parsing edit comments for article - %s...' % title)

        df = pd.DataFrame(columns=columns)

        index = 0
        revisions = getRevisions(title)

        for revision in revisions:
            try:
                row = xmltodict.parse(revision)
                df.loc[index] = [row['rev']['@user'], row['rev']['@comment'], row['rev']['@timestamp']]
            except KeyError:
                pass
            index += 1

        df.to_csv('./results/' + title + '.csv', encoding='utf-8')
        

    print('Done.')
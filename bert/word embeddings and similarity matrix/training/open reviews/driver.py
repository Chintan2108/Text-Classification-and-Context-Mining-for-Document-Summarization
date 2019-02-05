import crawler
import save_data

if __name__ == "__main__":
    '''
    driver function/ Main function
    '''

    #initializing the count var
    temp = open('count.txt', 'w')
    temp.write('0')
    temp.close()

    #crawling the notes section of openreviews.net/notes for paper submissions
    #and extracting the forum_ids to scrape papers and their reviews
    crawler.crawl(download=True)

    #saving the reviews as a pickled dataset
    #location: ./dataset/reviews.pkl
    save_data.saveReviews()

    #saving the papers as a pickled dataset
    #location: ./dataset/papers.pkl
    save_data.savePapers()

    print('Done.')
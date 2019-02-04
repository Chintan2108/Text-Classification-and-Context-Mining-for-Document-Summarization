import requests, time
import pandas as pd
import urllib.request
import pickle

def downloadPDF(url):
	'''
	This function downloads the pdf file of the research paper found in the args url 
	by a getcontent request
	'''
	directory = './Papers_PDF/'
	temp = open(directory + 'count.txt','r')
	pindex = temp.readline()
	temp = open(directory + 'count.txt', 'w')
	temp.write(str(int(pindex)+1))
	temp.close()
	
	#downloading the paper
	urllib.request.urlretrieve(url, './Papers_PDF/Paper_' + pindex + '.pdf')
	print('Paper-' + pindex + ' PDF downloaded succesfully.')

def pickleParams(textlist, numlist1, numlist2):
	'''
	This function pickles the review, rating and confidence lists for each paper 
	with relevant namesake
	'''
	directory = './Review Params/'
	temp = open(directory + 'count.txt','r')
	pindex = temp.readline()
	temp = open(directory + 'count.txt', 'w')
	temp.write(str(int(pindex)+1))
	temp.close()

	numlist1 = list(set(numlist1))
	numlist2 = list(set(numlist2))

	with open(directory + 'Reviews/Paper_' + pindex + 'review.pkl', 'wb') as temp:
		pickle.dump(textlist, temp)
	with open(directory + 'Ratings/Paper_' + pindex + 'rating.pkl', 'wb') as temp:
		pickle.dump(numlist1, temp)
	with open(directory + 'Confidence/Paper_' + pindex + 'confidence.pkl', 'wb') as temp:
		pickle.dump(numlist2, temp)

	print('Review params for Paper_' + pindex + ' pickled successfully.')

def crawl():
	'''
	This function crawls the base_url page and navigates accordingly,
	saving the data as json and does the necessary extractions,
	hence a web crawler
	'''
	url = 'https://openreview.net/notes?invitation=ICLR.cc%2F2018%2FConference%2F-%2FBlind_Submission&offset=0&limit=1000'
	df = pd.DataFrame(requests.get(url).json()['notes']) # Each row in this data frame is a paper.
    
    #df.to_csv('file_name.csv', sep='\t', encoding='utf-8')
    
	base_url = 'https://openreview.net'
	for i, forum_id in list(enumerate(df.forum)): # Each forum_id is a review, comment, or acceptance decision about a paper.
		print('Forum_id : ' + forum_id)
		target_url = base_url + '/notes?forum=' + forum_id
		pf = pd.DataFrame(requests.get(target_url).json()['notes']) # each row is details about the paper, first row contains paper pdf link, reviews from 3rd row onwards
		
		#placeholders for each paper for rating, reviews and comments
		rating = []
		review = []
		confidence = []
		index = 0
		for j, item in list(enumerate(pf.content)):
				if index == 0:
						downloadPDF(base_url + item['pdf'])

				if 'rating' in item.keys():
					review.append(item['review'])
					rating.append(item['rating'])
					confidence.append(item['confidence'])
				#print(item.keys())
				index += 1
		pickleParams(review, rating, confidence)
		print('************************************')

crawl()
    
# Text-Classification-and-Context-Mining-for-Document-Summarization

## Summary

Automnomously attempting a categorical summarization of a sparse, asymmetrical corpus in English language, by performing text classification - which is achieved by our intuitive sentence pair classification scenarios and usecases.

## Getting Started

Coming soon!

## Modules

### BERT for sentence pair classification

Fine-tuning a pretrained bert model on a custom dataset for sentence pair classification.

#### Built With

* PyTorch
* TorchVision
* CUDA >=7.0
* BERT

#### Datasets

The following datasets were sampled for groundtruth as well as for training and testing the model.
Validation data for model evaluation will be released soon.

* Openreviews papers and review comments
* Wikipedia talk and edit comments along with the articles

### Sentence Pair Similarity (Algorithm + Implementation)

This is an algorithm I penned for labelling a pair of sentences with a similarity score based on the cosine similarity of their word vectors, cross-referenced from the BOW (Bag of Words). The vectors are also validated using the tfidf matrix at the document level. Please cite when using this algorithm.

#### Built With

* Gensim wordmodel
* Gensim word vectors

#### Datasets

* Google Word Embeddings pretrained vectors for 1b words
* Train and test data to be released soon

### Web Crawlers

Two web crawlers have been developed for populating the train and test data, from openreviews as well as wikipedia as well. Feel free to use fork them and develop on top of them as well. Please cite a reference! 

#### OpenReviews Crawler

[This crawler](https://github.com/Chintan2108/Text-Classification-and-Context-Mining-for-Document-Summarization/tree/master/bert/word%20embeddings%20and%20similarity%20matrix/training/open%20reviews) uses the json source available at openreviews.net/notes and parses the same to segregate the papers and their review comments. 

#### Wikipedia Crawler

[This crawler]() uses the media wiki api and fetches the revisions pertiaining to that article. The xml response is then parsed and processed into a format to proceed with the data sampling. 

## Contribution

Please feel free to raise issues and fix any existing ones. Further details can be found in our [code of conduct]().

## References

* The parser for wikipedia talk comments was referenced from https://github.com/bencabrera/grawitas - Thank you for the source code and a detailed insight on how to use it.

```
Cabrera, B., Steinert, L., Ross, B. (2017). Grawitas: A Grammar-based Wikipedia Talk Page Parser. Proceedings of the Software Demonstrations of the 15th Conference of the European Chapter of the Association for Computational Linguistics, pp. 21-24.
```

* Also, a shoutout to [JasonKessler](https://gist.github.com/JasonKessler/5e147f3b604303ec6867a84b019b3957) for gisting up a nice kickstart to crawl openreviews.net! 

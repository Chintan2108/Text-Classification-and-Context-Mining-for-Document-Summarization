# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 20:47:28 2019

@author: Chintan Maniyar
"""
import warnings
warnings.filterwarnings('ignore')

import random
import numpy as np
import mxnet as mx
from mxnet import gluon 
import gluonnlp as nlp
#calling in pre-trained bert
import bert
from bert import *
from bert import 

#setting env
np.random.seed(100)
random.seed(100)
mx.random.seed(10000)
ctx = mx.cpu(0)

#vocab + model
bert_base, vocabulary = nlp.model.get_model('bert_12_768_12',
                                            dataset_name='book_corpus_wiki_en_uncased',
                                            pretrained=True,
                                            ctx=ctx,
                                            use_pooler=True,
                                            use_decoder=False,
                                            use_classifier=False)


#model definition for sentence pair classification
model = bert.BERTClassifier(bert_base, num_classes=2, dropout=0.1)

#init classifier layer
model.classifier.initialize(init=mx.init.Normal(0.02), ctx=ctx)
model.hybridize(static_alloc=True)

#softmax cross entropy loss
loss_function = gluon.loss.SoftmaxCELoss()
loss_function.hybridize(static_alloc=True)
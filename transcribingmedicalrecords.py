


import matplotlib.pyplot as plt
import itertools
import math
import pandas as pd
import os
import numpy as np
import re
import joblib

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer


model = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', OneVsRestClassifier(SGDClassifier(loss='log', penalty='l1', class_weight="balanced", verbose=1), n_jobs=-1))
                      ])
model = joblib.load('model2.pkl')

def summarizer(transcription):
    print('Input: '+ transcription)
    prediction_row = model.predict([transcription])
    print('Output: '+prediction_row[0])
    return prediction_row[0]



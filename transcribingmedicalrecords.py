# # -*- coding: utf-8 -*-
# """TranscribingMedicalRecords.ipynb

# Automatically generated by Colaboratory.

# Original file is located at
#     https://colab.research.google.com/drive/1q0qKMcmu7pkeDV584b70N-eiVpGQKMCt
# """

# # Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import matplotlib.pyplot as plt
import itertools
import math
import pandas as pd
import os
import numpy as np
import re
import joblib
# # # preprocessing
# # from keras.preprocessing.text import Tokenizer
# # from keras_preprocessing.sequence import pad_sequences
# # from keras.utils import to_categorical

# from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import recall_score
# from sklearn.metrics import f1_score
# from sklearn.metrics import precision_score
# from sklearn.metrics import classification_report
# from sklearn.metrics import hamming_loss

# import nltk
# nltk.download('stopwords')
# from nltk.tokenize import RegexpTokenizer
# from nltk.corpus import stopwords



# df = pd.read_csv('./datasets.csv', index_col=0)

# df.astype(str)
# print(df.head())

# df["keywords"].str.split(", ")

# def text_prepare(text):

#     REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@\-,.;#&]')
#     BAD_SYMBOLS_RE = re.compile('[0-9][0-9a-z ][#+_]{1,}')
#     STOPWORDS = set(stopwords.words('english'))
    
#     text = text.lower()
#     text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
#     text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
#     words = text.split()
#     i = 0
#     while i < len(words):
#         if words[i] in STOPWORDS:
#             words.pop(i)
#         else:
#             i += 1
#     text = ' '.join(map(str, words))# delete stopwords from text
    
#     return text
# def text_prepare_keywords(text):
#     REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@\-.,;#&]')
#     BAD_SYMBOLS_RE = re.compile('[0-9][0-9a-z #+%_]')
#     STOPWORDS = set(stopwords.words('english'))
    
#     text = text.lower()
#     text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
#     text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
#     words = text.split()
#     i = 0
#     while i < len(words):
#         if words[i] in STOPWORDS:
#             words.pop(i)
#         else:
#             i += 1
#     text = ' '.join(map(str, words))# delete stopwords from text
    
#     return text

# df['keywords'].replace('', np.nan, inplace=True)
# df = df.drop(df[df['transcription'].isna()].index)
# df = df.drop(df[df['keywords'].isna()].index)

# df['transcription'] = df['transcription'].str.replace(r'[0-9-A-Z\s]+:', '')
# df['keywords'] = df['keywords'].str.replace(r'[0-9-A-Z\s]+:', '')
# df['keywords'] = df['keywords'].str.replace(r'(, *)?$', '')
# df['keywords'] = df['keywords'].str.replace(r'^( *,)?', '')
# df['keywords'] = df['keywords'].str.replace(r'\s{2,}', '')
# df['keywords'] = df['keywords'].str.replace(r'%', '')
# df.loc[:, 'transcription'] = [text_prepare(x) for x in df['transcription'].values]
# df.loc[:, 'keywords'] = [text_prepare_keywords(x) for x in df['keywords'].values]

# tokenizer = RegexpTokenizer(r'[\w\'-]+')
# df["tokens_keywords"] = df["keywords"].apply(tokenizer.tokenize)
# df["tokens_keywords"].head()

# df["keyword_count"] = df['keywords'].apply(lambda text: len(text.split(" ")))
# df.head()

# df.keyword_count.value_counts()

# # using count vectorizer
# vectorizer = CountVectorizer(tokenizer = lambda x: x.split(' '))

# keywords_dtm = vectorizer.fit_transform(df['keywords'])

# print("Number of data points :", keywords_dtm.shape[0])
# print("Number of unique tags :", keywords_dtm.shape[1])

# # Storing the count of tag in each transcription in the list 'tag_count
# tag_quest_count = keywords_dtm.sum(axis=1).tolist()

# # converting list of lists into single list,we will get [[3], [4], [2], [2], [3]] and we are converting this to [3, 4, 2, 2, 3]
# tag_quest_count=[int(j) for i in tag_quest_count for j in i]
# print('We have total {} datapoints.'.format(len(tag_quest_count)))
# print(tag_quest_count[:5])

# print ("Maximum no of tag per transcription: %d"%max(tag_quest_count))
# print ("Minimum no of tags per transcription: %d"%min(tag_quest_count))
# print ("Avg number of tags per transcription: %f"% ((sum(tag_quest_count)*1.0)/len(tag_quest_count)))

# import seaborn as sns
# fig = plt.figure(figsize=(20,10))
# sns.countplot(tag_quest_count, palette='gist_rainbow')
# plt.title("Number of tags in the transcription")
# plt.xlabel("Number of Tags")
# plt.ylabel("Number of transcription")
# plt.show()

# tags = vectorizer.get_feature_names_out()
# print(len(tags))

# #Lets now store the document term matrix in a dictionary.
# freqs = keywords_dtm.sum(axis=0).A1
# result = dict(zip(tags, freqs))

# tag_df = pd.DataFrame({'Tags': tags, 'Counts': freqs})
# tag_df.head()

# tag_df_sorted = tag_df.sort_values(['Counts'], ascending=False)
# tag_counts = tag_df_sorted['Counts'].values

# plt.plot(tag_counts[:1000])
# plt.title("Distribution of number of times tag appeared")
# plt.grid()
# plt.xlabel("Tag number")
# plt.ylabel("Number of times tag appeared")
# plt.show()

# plt.plot(tag_counts, c='b')
# plt.scatter(x=list(range(0,100,5)), y=tag_counts[0:100:5], c='orange', label="quantiles with 0.05 intervals")
# # quantiles with 0.25 difference
# plt.scatter(x=list(range(0,100,25)), y=tag_counts[0:100:25], c='m', label = "quantiles with 0.25 intervals")

# for x,y in zip(list(range(0,100,25)), tag_counts[0:100:25]):
#     plt.annotate(s="({} , {})".format(x,y), xy=(x,y), xytext=(x-0.05, y+500))

# plt.title('first 100 tags: Distribution of number of times tag appeared transcription')
# plt.grid()
# plt.xlabel("Tag number")
# plt.ylabel("Number of times tag appeared")
# plt.legend()
# plt.show()
# print(len(tag_counts[0:100:5]), tag_counts[0:100:5])

# import datetime
# from wordcloud import WordCloud
# # Ploting word cloud
# start = datetime.datetime.now()

# # Lets first convert the 'result' dictionary to 'list of tuples'
# tup = dict(result.items())
# #Initializing WordCloud using frequencies of tags.
# wordcloud = WordCloud(    background_color='black',
#                           width=1600,
#                           height=800,
#                     ).generate_from_frequencies(tup)

# fig = plt.figure(figsize=(30,20))
# plt.imshow(wordcloud)
# plt.axis('off')
# plt.tight_layout(pad=0)
# fig.savefig("tag.png")
# plt.show()
# print("Time taken to run this cell :", datetime.datetime.now() - start)

# i=np.arange(30)
# fig = plt.figure(figsize=(20,10))
# tag_df_sorted.head(30).plot(kind='bar')
# plt.title('Frequency of top 20 tags')
# plt.xticks(i, tag_df_sorted['Tags'])
# plt.xlabel('Tags')
# plt.ylabel('Counts')
# plt.show()

# # Obsetving the quantiles using the violin plot and box .

# plt.figure(figsize=(10, 8))

# plt.subplot(1,2,1)
# sns.violinplot(data = tag_df_sorted.head(30) , )
# plt.xlabel("Number of Tags")
# plt.ylabel("Number of transcription")

# plt.subplot(1,2,2)
# sns.boxplot(tag_quest_count, palette='gist_rainbow')
# plt.xlabel("Number of Tags")
# plt.ylabel("Number of transcription")
# plt.show()

# df.drop(['description', 'medical_specialty', 'sample_name', 'tokens_keywords'], axis=1, inplace=True)

# df.head()

# x_train=df.sample(frac=0.5, replace=True, random_state=1)
# x_test=df.sample(frac=0.2, replace=True, random_state=1)

# import nltk
# import seaborn as sns
# all_genres = nltk.FreqDist(x_train["keywords"].apply(lambda x: x.split(' ')[0]))
# all_genres_df = pd.DataFrame({'Keywords': list(all_genres.keys()), 'Count': list(all_genres.values())})
# g = all_genres_df.nlargest(columns="Count", n = 100) 
# plt.figure(figsize=(12,15))
# ax = sns.barplot(data=g, x= "Count", y = "Keywords")
# ax.set(ylabel = 'Count')
# plt.show()
# list(all_genres.keys())

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer

# X_train = np.array(x_train['transcription'])
# Y_train = np.array(x_train['keywords'])
# X_test = np.array(x_test['transcription'])
# Y_test = np.array(x_test['keywords'])

model = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', OneVsRestClassifier(SGDClassifier(loss='log', penalty='l1', class_weight="balanced", verbose=1), n_jobs=-1))
                      ])
# model.fit(X_train, Y_train)
model = joblib.load('model2.pkl')
# joblib.dump(model, "pipeline1.pkl", compress=9)
# prediction = model.predict(X_test)

# print("Accuracy :",accuracy_score(Y_test, prediction))
# print("Hamming loss ",hamming_loss(Y_test,prediction))


# precision = precision_score(Y_test, prediction, average='micro')
# recall = recall_score(Y_test, prediction, average='micro')
# f1 = f1_score(Y_test, prediction, average='micro')
 
# print("Micro-average quality numbers")
# print("Precision: {:.4f}, Recall: {:.4f}, F1-measure: {:.4f}".format(precision, recall, f1))

# precision = precision_score(Y_test, prediction, average='macro')
# recall = recall_score(Y_test, prediction, average='macro')
# f1 = f1_score(Y_test, prediction, average='macro')
# predList = list()
# print("Macro-average quality numbers")
# print("Precision: {:.4f}, Recall: {:.4f}, F1-measure: {:.4f}".format(precision, recall, f1))
def summarizer(transcription):
    print('Input: '+ transcription)
    prediction_row = model.predict([transcription])
    print('Output: '+prediction_row[0])
    return prediction_row[0]



# -*- coding: utf-8 -*-
"""Deep Learning RNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M8J9CuVoGmZ0jcF0FQ9xnzQDyTYxOs8f
"""

import numpy as np
import pandas as pd
import re

from google.colab import drive
drive.mount('/content/drive')

path = "/content/drive/MyDrive/Project Dataset (1).csv"
disaster = pd.read_csv(path)

disaster.head()

# Loading required features
disaster = disaster[['text','target']]
disaster.head()

# Checking the Null Values
disaster.isna().sum()

# Checking the DF size
disaster.shape

# Lets see how Target Values labled
disaster['target'].value_counts()

disaster['text'] = [entry.lower() for entry in disaster['text']]
disaster['text'].head()

import nltk
from nltk.tokenize import word_tokenize

import nltk
nltk.download('punkt')

disaster['text'] = [word_tokenize(entry) for entry in disaster['text']]

disaster['text'].head()

disaster['text'].head()

from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet

import nltk
nltk.download('punkt')

nltk.download('averaged_perceptron_tagger')

import nltk
nltk.download('wordnet')

tag_map = defaultdict(lambda : wn.NOUN)
tag_map['j'] = wn.ADJ
tag_map['v'] = wn.VERB
tag_map['v'] = wn.ADV

import nltk
nltk.download('stopwords')

stop_words = set(stopwords.words("english"))
print(stop_words)

for index,entry in enumerate(disaster['text']):
    Final_words = []
    word_lemmstized = WordNetLemmatizer()
    for word,tag in pos_tag(entry):
        if word not in stopwords.words('english') and word.isalpha():
            word_final = word_lemmstized.lemmatize(word,tag_map[tag[0]])
            Final_words.append(word_final)
    disaster.loc[index,'text_final'] = str(Final_words)

disaster.head()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection,naive_bayes
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

Train_X,Test_X,Train_Y,Test_Y = model_selection.train_test_split(disaster['text_final'],disaster['target'],test_size = 0.3)
encoder = LabelEncoder()
Train_Y = encoder.fit_transform(Train_Y)
Test_Y = encoder.fit_transform(Test_Y)

y = Train_Y.tolist()

Tfidf_vect = TfidfVectorizer(max_features = 5000)
Tfidf_vect.fit(disaster['text_final'])
Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)

data = Train_X_Tfidf.toarray()

data

# Commented out IPython magic to ensure Python compatibility.
from keras.models import Model
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding
from tensorflow.keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from tensorflow.keras.utils import to_categorical
from keras.callbacks import EarlyStopping
# %matplotlib inline

Train_X,Test_X,Train_Y,Test_Y = model_selection.train_test_split(disaster['text_final'],disaster['target'],test_size = 0.3)
encoder = LabelEncoder()
Train_Y = encoder.fit_transform(Train_Y)
Test_Y = encoder.fit_transform(Test_Y)

Tfidf_vect = TfidfVectorizer(max_features = 5000)
Tfidf_vect.fit(disaster['text_final'])
Train_X_Tfidf = Tfidf_vect.transform(Train_X)
Test_X_Tfidf = Tfidf_vect.transform(Test_X)
max_words = 1000
max_len = 150
tok = Tokenizer(num_words=max_words)
tok.fit_on_texts(Train_X)
sequences = tok.texts_to_sequences(Train_X)
sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len)

def RNN():
    inputs = Input(name='inputs',shape=[max_len])
    layer = Embedding(max_words,50,input_length=max_len)(inputs)
    layer = LSTM(64)(layer)
    layer = Dense(256,name='FC1')(layer)
    layer = Activation('relu')(layer)
    layer = Dropout(0.5)(layer)
    layer = Dense(1,name='out_layer')(layer)
    layer = Activation('sigmoid')(layer)
    model = Model(inputs=inputs,outputs=layer)
    return model

model = RNN()
model.summary()
model.compile(loss='binary_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])

model.fit(sequences_matrix,Train_Y,batch_size=128,epochs=20,validation_split=0.2,callbacks=[EarlyStopping(monitor='val_loss',min_delta=0.0001)])

test_sequences = tok.texts_to_sequences(Test_X)
test_sequences_matrix = sequence.pad_sequences(test_sequences,maxlen=max_len)

accr = model.evaluate(test_sequences_matrix,Test_Y)

print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(accr[0],accr[1]))

def RNN():
    inputs = Input(name='inputs',shape=[max_len])
    layer = Embedding(max_words,50,input_length=max_len)(inputs)
    layer = LSTM(70)(layer)
    layer = Dense(406,name='FC1')(layer)
    layer = Activation('relu')(layer)
    layer = Dropout(0.2)(layer)
    layer = Dense(1,name='out_layer')(layer)
    layer = Activation('sigmoid')(layer)
    model = Model(inputs=inputs,outputs=layer)
    return model

model = RNN()
model.summary()
model.compile(loss='binary_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])

model.fit(sequences_matrix,Train_Y,batch_size=128,epochs=20,validation_split=0.2,callbacks=[EarlyStopping(monitor='val_loss',min_delta=0.0001)])

test_sequences = tok.texts_to_sequences(Test_X)
test_sequences_matrix = sequence.pad_sequences(test_sequences,maxlen=max_len)

accr = model.evaluate(test_sequences_matrix,Test_Y)

print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(accr[0],accr[1]))
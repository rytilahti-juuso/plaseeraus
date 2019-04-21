# -*- coding: utf-8 -*-
from keras.preprocessing.text import Tokenizer
import pandas as pd
import os
import re
os.chdir(r'C:\Users\The Risk Chief\Documents\GitHub\plaseeraus')
# DATA PREPROCESSING

column_names = ["name", "gender", "friends"]
train_data = pd.read_csv('plase.txt', delimiter= "\t", names = column_names)
friends_filled = train_data['friends'].fillna("Dummy_Value").values
names = train_data['name'].fillna("Dummy_Value").values

plase_score = []
for i in range(len(names)):
    friends_filled[i] = friends_filled[i].lower()
    friends_filled[i] = re.sub(r'[\,]+\s', ',', friends_filled[i])
    friends_filled[i] = re.sub(r'^\s','', friends_filled[i])

# Convert the names into integers
tokenizer = Tokenizer(split=",")
tokenizer.fit_on_texts(names)
sequences = tokenizer.texts_to_sequences(friends_filled)

# get word -> integer mapping
word2idx = tokenizer.word_index
print('Found %s unique tokens.' % len(word2idx))


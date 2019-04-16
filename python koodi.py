# -*- coding: utf-8 -*-

from keras.preprocessing.text import Tokenizer
from itertools import chain
import pandas as pd
import numpy as np
import re
import os
import random
os.chdir(r'C:\Users\The Risk Chief\Documents\GitHub\plaseeraus')



# Generate dummy table group
def generate_table_group(dummy_participant_count):
    table_group= []
    probability = random.randint(0,9)
    print(probability)
    if(probability >=4):
        table_group.append(random.randint(0,dummy_participant_count))
        if(probability >=6):
            table_group.append(random.randint(0,dummy_participant_count))
            if(probability>=9):
                table_group.append(random.randint(0,dummy_participant_count))
    return table_group


def generate_all_dummy_data():    
    all_data = []
    dummy_participant_count = 100
    for i in range(dummy_participant_count):
    #    data for single person stored in array
        person_data = []        
        person_data.append(i)
    #    people wanted in the same table group
        table_group = generate_table_group(dummy_participant_count)
        person_data.append(table_group)
    #    persons gender
        person_data.append(random.randint(0,1))
        all_data.append(person_data)
        print(i)
    return all_data

all_data = generate_all_dummy_data()

                    
# ACTUAL DATA PREPROCESSING

column_names = ["name", "gender", "friends"]
train_data = pd.read_csv('plase.txt', delimiter= "\t", names = column_names)
friends_filled = train_data['friends'].fillna("Dummy_Value").values
names = train_data['name'].fillna("Dummy_Value").values

plase_score = []
for i in range(len(names)):
    print(i)
    plase_score.append(100)
#    boy girl boy girls score affecting
    if(i%2 == 0):
        if(train_data["gender"][i]== 0):
            plase_score[i] = plase_score[i]-20
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



# Text preprocessing

#persons = ['Matti meikälainen, Kossu Koskenkorce, Eppu Normaali']
persons = [['Matti meikälainen, Kossu Koskenkorce, Eppu Normaali'], ["Ville Virtanen, Riski Asteriski,"], ["Riski Asteriski"]]


# Using numpy, if you use numpy, you can flatten numpy array with flatten() for tokenizer
#list_of_all_persons = persons.flatten()

# Using itertools.chain to flatten 2d list to 1d
list_of_all_persons = list(chain.from_iterable(persons))

# Text Cleaning
for i in range(len(list_of_all_persons)):
    print(i)
    list_of_all_persons[i] = list_of_all_persons[i].lower()
    list_of_all_persons[i] = re.sub(r'[\,]+\s', ',', list_of_all_persons[i])
    list_of_all_persons[i] = re.sub(r'^\s','', list_of_all_persons[i])
    print(list_of_all_persons[i])

# Convert the names into integers
tokenizer = Tokenizer(split= ',')
tokenizer.fit_on_texts(list_of_all_persons)
sequences = tokenizer.texts_to_sequences(list_of_all_persons)

# get word -> integer mapping
word2idx = tokenizer.word_index
print('Found %s unique tokens.' % len(word2idx))

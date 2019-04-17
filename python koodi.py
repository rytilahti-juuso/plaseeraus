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
#    print(probability)
    if(probability >=2):
        table_group.append(random.randint(0,dummy_participant_count))
        if(probability >=4):
            table_group.append(random.randint(0,dummy_participant_count))
            if(probability>=6):
                table_group.append(random.randint(0,dummy_participant_count))
    return table_group

# one element contains(name, table_group, gender, boolean isAlreadySorted)
def generate_all_dummy_data():    
    all_data = []
    dummy_participant_count = 20
    for i in range(dummy_participant_count):
    #    data for single person stored in array
        person_data = []        
        person_data.append(i)
    #    people wanted in the same table group
        table_group = generate_table_group(dummy_participant_count-1)
        person_data.append(table_group)
    #    persons gender
        person_data.append(random.randint(0,1))
        person_data.append(False)
        all_data.append(person_data)
        print(i)
    return all_data
    
# Needs size of wanted table company + man itself
def indexes_of_table_group(all_data, size_of_table_group):    
    items_indexes = []
    for i in range(0, len(all_data)):
        if(len(all_data[i][1])== size_of_table_group-1):
            
#            if(all_data[i][3] == False):       
            items_indexes.append(i)
#                all_data[i][3] = True
            
    return items_indexes 

def sort_data_by_table_company_size(all_data):
    all_data_sorted = []
    group_of_4 =  indexes_of_table_group(all_data, 4)
    group_of_3 = indexes_of_table_group(all_data, 3)
    group_of_2 = indexes_of_table_group(all_data, 2)
    group_of_1 = indexes_of_table_group(all_data, 1)
    for i in range(len(group_of_4)):
        all_data_sorted.append(all_data[group_of_4[i]])
    for i in range(len(group_of_3)):
        all_data_sorted.append(all_data[group_of_3[i]])
    for i in range(len(group_of_2)):
        all_data_sorted.append(all_data[group_of_2[i]])
    for i in range(len(group_of_1)):
        all_data_sorted.append(all_data[group_of_1[i]])
    return all_data_sorted

def create_final_order_table(all_data_sorted_by_size, list_to_find_index):
    final_order = []
    for i in range(0, len(all_data_sorted_by_size)):
        if(all_data_sorted_by_size[i][3] == False):
            final_order.append(all_data_sorted_by_size[i])
            print(all_data_sorted_by_size[i])
            all_data_sorted_by_size[i][3] = True
    #            Go through wanted table company
            final_order = loop_through_wanted_table_company(all_data_sorted_by_size[i][1], final_order)
    return final_order

#    Loops through wanted table company
#returns appended final_order
def loop_through_wanted_table_company(table_company, final_order):
    for a in range(0, len(table_company)):
                wanted_index = table_company[a]
#                print("this is wanted index", wanted_index, all_data_sorted_by_size[wanted_index][3])
                wanted_index = list_to_find_index.index(wanted_index)
                if(all_data_sorted_by_size[wanted_index][3] == False):    
                    all_data_sorted_by_size[wanted_index][3] = True
                    list_item = all_data_sorted_by_size[wanted_index]
                    print("this is list item", list_item)
                    final_order.append(list_item)
    return final_order
    
def create_list_to_find_correct_index(all_data_sorted_by_size):        
    find_correct_index_list = []
    for i in range(len(all_data_sorted_by_size)):
        find_correct_index_list.append(all_data_sorted_by_size[i][0])
    return find_correct_index_list    

# before going sorted by size
def validate_that_desire_to_table_group_is_mutual():
    pass

# check if sits on correct gender_spot
def check_gender_and_change_place(table):
    for i in range(3, (len(final_table)-3)):
#        TODO: special cases like index 0 and last index handling
#        if(i%2==0 and i!=0):
#        Checks if gender on the other side of table is same gender
        if(table[i][2] ==table [i+2][2]):
#            to left side of the table
            if(i%2==0):                
                if(table[i][2] != table[i-1][2]):
                    print("before change table[i] is:", table[i])
                    print("before change table[-1] is:", table[i-1])
                    temp = table[i-1]
                    table[i-1] = table[i]
                    table[i] = temp
                    print("after change table[i] is:", table[i])
                    print("after change table[-1] is:", table[i-1])
                if(table[i][2] != table[i+3][2]):
                    print("before change table[i] is:", table[i])
                    print("before change table[-1] is:", table[i+3])
                    temp = table[i+3]
                    table[i-3] = table[i]
                    table[i] = temp
                    print("after change table[i] is:", table[i])
                    print("after change table[-1] is:", table[i+3])
            if(i%2==1):
                if(table[i][2] != table[i-3][2]):
                    print("before change table[i] is:", table[i])
                    print("before change table[-1] is:", table[i-3])
                    temp = table[i-3]
                    table[i-3] = table[i]
                    table[i] = temp
                    print("after change table[i] is:", table[i])
                    print("after change table[-1] is:", table[i-3])
                if(table[i][2] != table[i+1][2]):
                    print("before change table[i] is:", table[i])
                    print("before change table[-1] is:", table[i+1])
                    temp = table[i+1]
                    table[i+1] = table[i]
                    table[i] = temp
                    print("after change table[i] is:", table[i])
                    print("after change table[-1] is:", table[i+1])
                
        
    
#def main():    
all_data = generate_all_dummy_data()
#indexes_of_table_group(all_data, 2)
all_data_sorted_by_size =  sort_data_by_table_company_size(all_data)
list_to_find_index = create_list_to_find_correct_index(all_data_sorted_by_size)
final_table = create_final_order_table(all_data_sorted_by_size, list_to_find_index)








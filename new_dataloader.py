#### this data loading is based on torch.utils.Dataloader

import os 
import re
import json
import numpy as np 
import pandas as pd

import torch 
from torch.utils.data import DataLoader, Dataset     # what is the Dataset here ??
import torch.nn as nn 
import torch.nn.functional as F 

# also I need to make the program deal with the 
add = '/Users/meiluyuan/Desktop/Theorem_Proving/data/premise_selection/human_1/'   # '/your-data-address/'
train_set = add + 'train.csv'
val_set = add + 'valid.csv'
test_set = add + 'test.csv'
tactic_id_json = add + 'tactic_id.json'
TRUNCATE_NUM = 1000 
BATCH_SIZE = 10

#### data preprocessing .... for each set ( train/validation/test... )
# 1. read each line and get all the pairs 
# 2. follow the some course videos and the DeepHOL repo to build the data pipeline ...
raw_data = pd.read_csv(add + val_set)
cat_num = 2
# we need to skip the 1st raw and then get all the data 
proofs = raw_data.iloc[cat_num, 0]
tactics = raw_data.iloc[cat_num, 1]   # all data have the string type ...

print ("Look at the proofs: \n {}".format(proofs) )
print ("Look at the tactics \n {}".format(tactics) )

# Here we need to form a tactic list with 41 tactic info from the training set ...
def tactic_id_list(train_csv):
    csv_contents = pd.read_csv(train_csv) 
    all_tactics = csv_contents.iloc[:, 1].tolist()   # get all the tactics 
    # write a file named as 'tactic_id.json.'
    tactic_set = set(all_tactics)
    count = 0
    tactic_list = []
    for tactic in tactic_set:
        tactic_list.append( (tactic, count))
        count = count + 1 
    tactic_dict = dict(tactic_list)
    tactic_count = { tactic: all_tactics.count(tactic) for tactic in tactic_set }
    print ( "This is the tactic dict: \n {}".format( tactic_dict ) )
    with open(add + 'tactic_id.json', 'w') as f:
        json.dump(tactic_dict, f)

# Here is a function definition which will split and truncate the goal statement to have fixed inout length ...
def goal_processing(goal):
    goal = goal.replace('(', ' ').replace(')', ' ')
    return ' '.join( goal.split()[1:TRUNCATE_NUM + 1] ) # remove the 1st word of the goal statement ...
     

# The most important part: the class to manipulate the goal-tactic pair dataset ...
class Goal_Tactic_Dataset(Dataset):    # why there is a Dataset input ....
    '''
    An abstract class representing a dataset. Your custom dataset should inherit Dataset and override the following methods 
    __len__ so that len(dataset) returns the size of the dataset.
    __getitem__ to support the indexing such that dataset[i] can be used to get ith sample 
    
    '''
    def __init__(self, csv_file, tactic_id_json):    # we only need a csv_file as input here ...
        self.goal_tactic_pairs = pd.read_csv(csv_file)
        self.TRUNCATE_NUM = TRUNCATE_NUM
        # read the tactic_id.json file as dict, so we can get the tactic_id_list ...
        self.tactic_id_list = json.load( open(tactic_id_json) )

    def __len__(self):
        return len(self.goal_tactic_pairs)

    def __getitem__(self, idx):       # what is the idx here used for ... ???
        if torch.is_tensor(idx):
            idx = idx.tolist()
        #### the following lines should be about get the data with the format we want ...
        # read the goal and tactic individually then get the tactic id and the splited truncated goal statement ...
        goal = self.goal_tactic_pairs.iloc[idx, 0]
        input_goal = goal_processing(goal)    
        tactic = self.goal_tactic_pairs.iloc[idx, 1]   # take care the tactic value format ... 
        tactic_id = self.tactic_id_list(tactic)
        return input_goal, tactic_id

goal_tacitc_train = Goal_Tactic_Dataset(train_set, tactic_id_json)
datalaoder = DataLoader(goal_tacitc_train, batch_size = BATCH_SIZE,  shuffle = True, num_workers = 4 )    # how to choose the batch_size

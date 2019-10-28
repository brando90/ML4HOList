"""
This is the neural nets (main) part of the premise selection ... 
For loading data, we'd like to apply the torchtext (docs here: https://torchtext.readthedocs.io/en/latest/ )
"""
import os  
import re
import math

import pandas as pd    # read the test 

# torchtext to help load and batch the data ...
import torch
import torchtext
from torchtext.data import Field 
from torchtext.data import TabularDataset 
from torchtext.data import Iterator, BucketIterator

import torch.nn as nn 
import torch.nn.functional as F 

"""
In this program, mainly two parts: data input && network architecture ... 
"""
##### Data input part ...

tokenize = lambda x : x.split()
text = Field( sequential = True, tokenize = tokenize, lower = True )
label = Field( sequential = False, use_vocab = True )     
# whether we are able to use another/standard vocab list to replace the generated label list ???

# read csv file with certain rule ...  
tv_datafields = [ ("goal", text), ("tactic", label) ]
train_set, validation_set = TabularDataset.splits(
        path="./premise_selection/human/", # the root directory where the data lies
        train='train.csv', validation="valid.csv",
        format='csv',
        skip_header=True, # if your csv header has a header, make sure to pass this to ensure it doesn't get proceesed as data!
        fields=tv_datafields)

test_datafields = [("goal", text)]
test_set = TabularDataset.splits(
    path = './premise_selection/human/test.csv',
    format = 'csv',
    skip_header = True,
    fields = test_datafields
)

text.build_vocab(train_set)    # build the vocab for goal and tactic ...
"""
to show or read any data use some codes like 
train_set[0]__dict__.keys()     # // 
train_set[0].a_key[:3] 
"""

train_iter, val_iter = BucketIterator.splits(
    (train_set, validation_set),
    batch_sizes = (64, 64), 
    device = -1,    # here, we use cpu to read the data ... (avoid spcifying GPU number)
    sort_key = lambda x:len(x.goal),  # what's wrong here ???
    sort_within_batch  = False,
    repeat = False
)

batch = next(train_iter.__iter__())    # training input data ...

"""
# To see the information e.g. contents / dict keys of batch data:
print (batch)
batch.__dict__.keys()
"""
test_iter = Iterator(test_set, batch_size = 64, device = -1, sort = -1, sort_within_batch = False, repeat = False)


class BatchWrapper:
    def __init__(self, dl, x_var, y_vars):
        self.dl, self.x_var, self.y_vars = dl, x_var, y_vars # we pass in the list of attributes for x and y
    
    def __iter__(self):
        for batch in self.dl:
            x = getattr(batch, self.x_var) # we assume only one input in this wrapper
            
            if self.y_vars is not None: # we will concatenate y into a single tensor
                y = torch.cat([getattr(batch, feat).unsqueeze(1) for feat in self.y_vars], dim=1).float()
            else:
                y = torch.zeros((1))

            yield (x, y)
    
    def __len__(self):
        return len(self.dl)

#### then make the data batch which is able to be input directly ...
train_batch = BatchWrapper(train_iter, "goal", ["tactic"])
valid_batch = BatchWrapper(val_iter, "goal", ["tactic"])
test_batch = BatchWrapper(test_iter, "goal", None)



# Here we create the network for prediction task ... 
# For complete replication, refer the code snippets here ( https://github.com/tensorflow/deepmath/blob/master/deepmath/deephol/train/architectures.py ) 
class Baseline_Model():
    def __init__():
        self.embedding = ,
        self.encoder = ,
        self.linear_layers = ,
        self.predictor = ,
    def forward():
        # ...
        output = self.predictor()
        return output 


def main():
        return 


if __name__ == '__main__':
        main()



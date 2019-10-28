"""
To prepare the data for basic classification of the project ...
Extract the goal-tactic pairs ...
# What files we should have: txt? csv? json ??? We'd better to have a json file ???
"""

import os 
import re
import csv
import glob
import numpy as np 

pm_add = '/Users/meiluyuan/Desktop/Theorem_Proving/data/premise_selection/'

# read the whole file by line (per line represents a theorem proof ...)
def rw_one_file(file):
    with open(file, 'r') as f:
        for line in f:
            print ("The first data in file {} is :\n".format(file))
            print (line) 


# read and write the data woith appropriate way ...
def try_extract():
    all_files = glob.glob('/Users/meiluyuan/deephol-data/deepmath/deephol/proofs/human/test/*.pbtxt')
    file = '/Users/meiluyuan/deephol-data/deepmath/deephol/proofs/human/test/prooflogs-00000-of-00537.pbtxt'
    count = 0
    count_other = 0     # this part is used to make the 
    with open(file, 'r') as f:
        
        # Here, we need to locate precisely ... Make sure we re the precise pattern ...
        all_lines = f.readlines()
        a_line = all_lines[0]
        print ("This is a_line: {}".format(a_line))
        print ("\n")
        all_nodes = re.findall(r'nodes {   (.*?) status: PROVED }', a_line)    # with two bracelets outside the two  
        print ("There are all_nodes: {}".format(all_nodes))
        print ("\n")
        # make a doc for dis-matched goal and proof number  
        for node in all_nodes:
            # how to get the matched result as expectecd ...
            print (node)
            all_goals = re.findall(r'goal {     conclusion: "(.*?)"     tag:', node)   # find all_goals or all_proofs ...
            print ("all_goals are: {}".format(all_goals))
            print ("\n")
            all_tactics = re.findall(r'proofs {     tactic: "(.*?)"     result', node)
            print ("all_proofs are: {}".format(all_tactics) )
            # until now, we are able to extract all the data for premise slection, what kind of method we need to use for data organization ...



# Try to make them more efficient with some mechanism ... 
# the difference between the goal and proofs ...   # perhaps 
def try_main():
    all_files = glob.glob('/Users/meiluyuan/deephol-data/deepmath/deephol/proofs/human/test/*.pbtxt')
    for file in all_files:    # here I use [0] to limit the data for test ...
        print (file)
        with open(file, 'r') as f:
            all_lines = f.readlines()
            """ Here, we write the all the goal-tactic paris into a pbtxt file ... (refer the pytorch framework ...) """
            pm_name = re.findall(r'/prooflogs(.*?).pbtxt', file)
            print ("Current pm_name is {}".format(pm_name) )
            pm = open(pm_add + 'goal_tactic' + pm_name[0] + '.pbtxt', 'w+')
            count_1 = 0
            for a_line in all_lines:   
                all_nodes = re.findall(r'nodes {   (.*?) status: PROVED }', a_line)
                count_2 = 0
                for node in all_nodes:
                    all_goals = re.findall(r'goal {(.*?)     tag:', node)
                    """
                    all_subgoals = re.findall(r'subgoals {(.*?)     tag:', node)
                    all_goals = all_goals + all_subgoals
                    """
                    all_tactics = re.findall(r'proofs {     tactic: "(.*?)"', node)
                    goal_num = len(all_goals)
                    tactic_num = len(all_tactics)
                    """
                    print ("Node is {}".format(node))
                    print (all_goals)
                    print (all_tactics)
                    print ("goal_num is {}".format(goal_num) )
                    print ("tactic_num is {}".format(tactic_num) )
                    """
                    # if the number of goals and tactics don't match each other, then we won't write it into our premise selection data ...
                    if goal_num == tactic_num:
                        for i in range(goal_num):
                            pm.write('goal:' + all_goals[i] + ';')
                            pm.write('tactic:' + all_tactics[i] + ';')
                            pm.write('\n')
                    elif goal_num - tactic_num == 1:
                        print ("File: {}, Line: {} Node Count: {} --- goal tactic don't match ...".format(file, count_1, count_2))
                        print ("Goal_num is {} and Tactic_num is {}, the difference is 1.".format(goal_num, tactic_num))
                        for i in range(tactic_num):
                            pm.write('goal:' + all_goals[i] + ';')
                            pm.write('tactic:' + all_tactics[i] + ';')
                            pm.write('\n')
                    else:
                        print ("File: {}, Line: {} Node Count: {} --- goal tactic don't match ...".format(file, count_1, count_2))
                        print ("Node is {}".format(node))
                        print ('\n')
                        print (all_goals)
                        print ('\n')
                        print (all_tactics)
                        print ('\n')
                        print ("goal_num is {}".format(goal_num) )
                        print ("tactic_num is {}".format(tactic_num) )
                    count_2 = count_2 + 1
                count_1 = count_1 + 1
            pm.close() 
         

# look at pytorch support choose a file format to store the goal-tactic pair data 

                


if __name__ == '__main__':
    try_main()

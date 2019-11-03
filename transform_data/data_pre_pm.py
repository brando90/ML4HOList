"""
# prepare the training data for premise slection and then write them as csv files ...
# some data statistics about the HOList Dataset ...
# Maybe it's better for us to make some sample csv file to open and review conveniently ...
"""

import os 
import sys 
import re
import csv
import glob
import numpy as np 
from collections import namedtuple     # nametuple ???

csv.field_size_limit(sys.maxsize)
# It's better to combine the two sets together ...
pm_add = '/Users/meiluyuan/Desktop/Theorem_Proving/data/premise_selection/human_test/'

def get_stats (csv_file):
    
    with open(csv_file, 'r') as csv_f:
        ### sample number and tactic category number and list ... ###
        reader = csv.reader(csv_f)
        next(reader)
        
        all_tactics = [ pair[1] for pair in reader ]
        print ("The sample number of the dataset is {}".format( len(all_tactics) ))
        tactic_category = set(all_tactics)
        print ( "All the tactic categories are {}".format(len(tactic_category)) )
        print ("They are: {}".format(tactic_category)) 

    with open(csv_file, 'r') as csv_f:
        ### the stats about the goal statement here include the max&min length,  ###
        reader = csv.reader(csv_f)
        next(reader)

        def pure_goal(ori_data):
            pure_goal = re.findall(r'"(.*?)"', ori_data)   # we need to input this pure data in our interactive program ...
            return pure_goal
        all_goals = [ pure_goal(pair[0]) for pair in reader ] 
        all_lengths = [ len( str(goal)) for goal in all_goals ]
        all_lengths = sorted(all_lengths)
        total_num = len(all_lengths)
        median = all_lengths[int(total_num/2)] 
        print ("This is the median-length goal:\n {}".format(median))
        print(all_goals[median])
        print("the median character number of goal statement is {}".format(median))
        lengths = np.array(all_lengths)
        max_len = np.max(lengths)
        min_len = np.min(lengths)
        average_len = np.average(lengths)
        print ("Goal stas of the training set are: \n max_length is {};\n min_length is {};\n median:{}\n average:{};\n".format(
            max_len, min_len, median, average_len)) 


# review the data organization and its structure again for further writing ...
# also obtain the node info ...
def try_main():
    all_files = glob.glob('/Users/meiluyuan/deephol-data/deepmath/deephol/proofs/human/train/*.pbtxt')
    pm = open(pm_add + 'train' + '.csv', 'w+')    # without marks include assumption and hypothesis ...
    headers = ['goal', 'tactic']   
    pm_csv = csv.writer(pm)
    pm_csv.writerow(headers)
    nodes_nums = []
    for file in all_files:    # to test the results ...
        print (file)
        with open(file, 'r') as f:
            all_lines = f.readlines()
            count_1 = 0
            for a_line in all_lines:   
                all_nodes = re.findall(r'nodes {   (.*?) status: PROVED }', a_line)
                nodes_nums.append(len(all_nodes))
                count_2 = 0   # this is used to get the statistics of node number ...
                for node in all_nodes:
                    all_goals = re.findall(r'goal {(.*?)     tag:', node)   # two conditions?: hypothesis and assumption ...??? differences ... ???
                    all_tactics = re.findall(r'proofs {     tactic: "(.*?)"', node)
                    goal_num = len(all_goals)
                    tactic_num = len(all_tactics)
                    if goal_num == tactic_num:
                        for i in range(goal_num):
                            # if it's set, we need to use set format ...
                            goal = re.findall(r'"(.*?)"', all_goals[i])
                            goal_tactic = [ goal, all_tactics[i] ]   
                            pm_csv.writerow(goal_tactic)
                    # whether we have this situation exists ... ?
                    elif goal_num - tactic_num == 1:
                        print ("File: {}, Line: {} Node Count: {} --- goal tactic don't match ...".format(file, count_1, count_2))
                        print ("Goal_num is {} and Tactic_num is {}, the difference is 1.".format(goal_num, tactic_num))
                    else:
                        print ("File: {}, Line: {} Node Count: {} --- goal tactic don't match ...".format(file, count_1, count_2))
                        print ("Node is {}".format(node))
                        print ("goal_num is {}".format(goal_num) )
                        print ("tactic_num is {}".format(tactic_num) )
                    count_2 = count_2 + 1
                count_1 = count_1 + 1
    pm.close() 
                    

if __name__ == '__main__':
    try_main()
    csv_file = pm_add + 'goal_tactic.csv'
    get_stats(csv_file)

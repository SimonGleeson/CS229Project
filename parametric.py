"test to see if we can implement the baseline from countinglab"

import numpy as np
import pandas as pd
import sklearn
from sklearn import linear_model as lm
import os
import csv

path = os.getcwd()
#read in the data
with open(path + '/GEFCOM/mod_data.csv', 'rt') as dcsv:
    csvreader = csv.reader(dcsv)
    x = []
    y = []
    for index, row in list(enumerate(csvreader)):
        if index == 0:
            continue
        for j, col in list(enumerate(row)):
            if j == len(row):
                y.append(col)
                continue
            if index == 1:
                x.append([col])
            else:
                x[j].append(col)
            


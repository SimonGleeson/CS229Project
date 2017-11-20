"test to see if we can implement the baseline from countinglab"

import numpy as np
import pandas as pd
import sklearn
from sklearn import linear_model as lm
import os
import csv


#create the separate time series fields
seasons = ['fall', 'winter', 'spring', 'summer']
zones = [i for i in range(1, 21)]
dayType = [1, 0]
hour = [i for i in range(24)]


path = os.getcwd()
'''#read in the data
with open(path + '/GEFCOM/mod_data.csv', 'rt') as dcsv:
    csvreader = csv.reader(dcsv)
    x = []
    y = []
    for index, row in list(enumerate(csvreader)):
        if index == 0:
            print(row)
            continue
        if index == 2000:
            break #for running tests
        for j, col in list(enumerate(row)):
            col = int(col)
            if j == len(row):
                y.append(col)
                continue
            if index == 1:
                x.append([col])
            else:
                x[j].append(col)
        #manually add interaction terms
        if index == 1:
            for k in range(11):
                x.append([int(row[7 + k])**2])
                x.append([int(row[4])*int(row[7 + k])])
                x.append([int(row[4])*int(row[7 + k])**2])
        else:
            for k in range(11):
                x[j+3*k+1].append(int(row[7 + k])**2)
                x[j+3*k+2].append(int(row[4])*int(row[7 + k]))
                x[j+3*k+3].append(int(row[4])*int(row[7 + k])**2)
'''



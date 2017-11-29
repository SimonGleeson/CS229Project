import pandas as pd
import csv
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt

path = os.getcwd()

#create a dict that stores the times and loads of each zone
temps  = {}

with open(path + '/GEFCOM/temperature_history.csv', 'rt') as tcsv:
    tempreader = csv.reader(tcsv)
    for index, row in list(enumerate(tempreader)):
        #skip first row
        if index == 0:
            continue
        for i, col in enumerate(row):
           #ignore empty entries
           if col == '':
               continue
           #we look at the loads and temperatures which 
           #start in the 5th column
           if i > 3:
                hour = i - 4
                year = int(row[1])
                month = int(row[2])
                day = int(row[3])
                timeVal = datetime(year, month, day, hour)
                if timeVal in temps:
                    temps[timeVal].append(int(col))
                else:
                    temps[timeVal] = [int(col)]

#read in temperatures from solutions

with open(path + '/GEFCOM/temperature_solution.csv', 'rt') as tcsv:
    tempreader = csv.reader(tcsv)
    for index, row in list(enumerate(tempreader)):
        #skip first row
        if index == 0:
            continue
        hour = int(row[6]) - 1
        month = int(row[4])
        year  = int(row[3])
        day = int(row[5])
        timeVal = datetime(year, month, day, hour)
        if timeVal in temps:
            temps[timeVal].append(int(row[7]))
        else:
            temps[timeVal] = [int(row[7])]

#create a dict that stores the times and loads of each zone
loads = {}
#key for the load
loads['load'] = []
#key for the time (datetime objects)
loads['time'] = []
#key for the load zone
for i in range(1, 20):
    loads['zone_{}'.format(i)] = []
for i in range(1, 12):
    loads['weather_{}'.format(i)] = []
loads['weekday'] = []

with open(path + '/GEFCOM/Load_history.csv', 'rt', encoding='ascii') as lcsv:
    loadreader = csv.reader(lcsv)
    for index, row in list(enumerate(loadreader)):
        if index == 0:
            continue
        for i, col in enumerate(row):
           if col == '':
               continue
           #we look at the loads and temperatures which 
           #start in the 5th column
           if i > 3:
                hour = i - 4
                year = int(row[1])
                month = int(row[2])
                day = int(row[3])
                load = int(col.replace(',', ''))
                time = datetime(year, month, day, hour) 
                loads['time'].append(time)
                loads['load'].append(load)
                if time.weekday() < 5:
                    loads['weekday'].append(1)
                else:
                    loads['weekday'].append(0)

                for j in range(1, 20):
                    if j == int(row[0]):
                        loads['zone_{}'.format(j)].append(1)
                    else:
                        loads['zone_{}'.format(j)].append(0)
                weather = temps[time]
                for index, val in list(enumerate(weather, 1)):
                    loads['weather_{}'.format(index)].append(val)
                    

with open(path + '/GEFCOM/Load_solution.csv', 'rt', encoding='ascii') as lcsv:
    loadreader = csv.reader(lcsv)
    for index, row in list(enumerate(loadreader)):
        if index == 0:
            continue
        #Solutions have aggregated values, we will skip for now
        if int(row[1]) == 21:
            continue
        for i, col in enumerate(row):
           if col == '' or i == 29: #skip the weights part
               continue
           #we look at the loads and temperatures which 
           #start in the 5th column
           if i > 4:
                hour = i - 5
                year = int(row[2])
                month = int(row[3])
                day = int(row[4])
                load = int(col.replace(',', ''))
                time = datetime(year, month, day, hour) 
                loads['time'].append(time)
                loads['load'].append(load)
                if time.weekday() < 5:
                    loads['weekday'].append(1)
                else:
                    loads['weekday'].append(0)

                for j in range(1, 20):
                    if j == int(row[1]):
                        loads['zone_{}'.format(j)].append(1)
                    else:
                        loads['zone_{}'.format(j)].append(0)
                weather = temps[time]
                for index, val in list(enumerate(weather, 1)):
                    loads['weather_{}'.format(index)].append(val)
            
            
"""
#Create total load
totalLoad = []
for i in range(len(loads['load_1'])):
    totalLoad.append(sum(loads['load_{}'.format(j)][i] for j in range(1, 21)))
"""

"""
j = 0
tempList = []
for k in range(len(temps['time'])):
    if loads['time'][j] == temps['time'][k]:
        tempList.append(temps['temp'][k])
        j += 1
temps['temp'] = tempList


"""
"""
#colors
colors = ['aqua', 'azure', 'coral', 'lavender', 'lightgreen', 'grey', 'orangered', 'wheat', 'purple', 'tomato', 'sienna']
"""

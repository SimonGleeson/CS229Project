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


#create a dict that stores the times and loads of each zone
loads = {}
#key for the load
loads['load'] = []
#key for the time (datetime objects)
loads['time'] = []
#key for the load zone
loads['zone'] = []
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
                loads['zone'].append(int(row[0]))
                if time.weekday() < 5:
                    loads['weekday'].append(1)
                else:
                    loads['weekday'].append(0)

                weather = temps[time]
                for index, val in list(enumerate(weather, 1)):
                    loads['weather_{}'.format(index)].append(val)

mindate = datetime(2004, 1, 1)
with open(path + '/GEFCOM/mod_data.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(['id','zone','month','day','totDay','hour', \
            'weekday','w1', 'w2','w3','w4','w5','w6','w7',\
            'w8','w9','w10','w11','load'])
    for i in range(len(loads['zone'])):
        output = [str(i), str(loads['zone'][i])]
        date = loads['time'][i]
        output.append(str(date.month))
        output.append(str(date.day))
        output.append(str((date - mindate).days))
        output.append(str(date.hour))
        output.append(str(loads['weekday'][i]))
        for j in range(1, 12):
            w = 'weather_{}'.format(j)
            output.append(str(loads[w][i]))
        output.append(str(loads['load'][i]))
        csvwriter.writerow(output)

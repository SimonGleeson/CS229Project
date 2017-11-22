import copy
import os
from datetime import datetime
import numpy as np
import csv
import pandas as pd

path = os.getcwd()
solutions = pd.read_csv(path + '/GEFCOM/Load_solution.csv')

temps  = {}
for i in range(1, 12):
    #keys for the temperature
    temps['temp_{}'.format(i)] = [] 
    #keys for the time (datetime objects)
    temps['time_{}'.format(i)] = []

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
                temps['time_{}'.format(row[0])].append(timeVal)
                temps['temp_{}'.format(row[0])].append(int(col))

#Look at the dates in the answer solutions
dates = set()
seen = {}

for i in range(len(solutions['id'])):
    year = int(solutions['year'][i])
    month = int(solutions['month'][i])
    day = int(solutions['day'][i])
    if (year, month, day) in seen:
        continue
    seen[(year, month, day)] = True
    for j in range(24):
        dates.add((year, month, day, j))

tempvals = {}
for i in range(len(temps['time_1'])):
    if len(dates) == 0:
        break
    year = temps['time_1'][i].year
    month = temps['time_1'][i].month
    day = temps['time_1'][i].day
    hour = temps['time_1'][i].hour

    if year == 2004 or year == 2007 or year == 2008:
       continue 
    val = (year, month, day, hour)
    if val in dates:
        for j in range(1, 12):
            header = 'temp_{}'.format(j)
            if j == 1:
                tempvals[val] = [temps[header][i]]
            else:
                tempvals[val].append(temps[header][i])
        dates.remove(val)

minDate = datetime(2004, 1, 1)
with open('GEFCOM/temp_for_solutions.csv', 'w') as tcsv:
    csvwriter = csv.writer(tcsv, delimiter=',')
    csvwriter.writerow(['id','zone','year','month','day',\
            'totDay','hour','weekday','w1','w2','w3',\
            'w4','w5','w6','w7','w8','w9','w10','w11','load'])
    for i in range(len(solutions['id'])):
        print(i)
        output = [str(i), str(solutions['zone_id'][i])]
        yr= solutions['year'][i]
        if yr == 2008:
            break
        m = solutions['month'][i]
        d = solutions['day'][i]
        output.append(str(yr))
        output.append(str(m))
        output.append(str(d))

        date = datetime(yr, m, d)
        totDay = (date - minDate).days
        output.append(str(totDay))
        for k in range(24):
            tempoutput = output.copy()
            tempoutput.append(str(k))
            wd = (1 if date.weekday() < 5 else 0)
            tempoutput.append(str(wd))
            weather = [str(val) for val in tempvals[(yr, m, d, k)]]
            load = [solutions['h{}'.format(k+1)][i]]
            csvwriter.writerow(tempoutput + weather + load)


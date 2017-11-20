
import numpy as np
import pandas as pd
import os
import csv
from collections import defaultdict
import statsmodels.formula.api as sm
from datetime import datetime
import matplotlib.pyplot as plt

path = os.getcwd()

#read in solutions
solutions = pd.read_csv(path + '/GEFCOM/Load_solution.csv')
solutions = solutions[:][0:1175] #remove forecast values
solutions['season'] = solutions.apply(season, axis=1)

#create a dict that stores the times and loads of each zone
#Read in the temperatures
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
    if year == 2004 or year == 2007 or year == 2008:
        continue
    month = temps['time_1'][i].month
    day = temps['time_1'][i].day
    hour = temps['time_1'][i].hour
    val = (year, month, day, hour)
    
    if val in dates:
        for j in range(1, 12):
            header = 'temp_{}'.format(j)
            tempvals[(year, month, day, hour, j)] = temps[header][i]
        dates.remove(val)

#evaluate our models
sampleSize = int(1175* 0.25)
sample = np.random.randint(0, 1175, sampleSize)
minDate = datetime(2004, 1, 1)
num = 0
denom = 0
for i in sample:
    #pull out relevant indicators
    s = solutions['season'][i] #get the season
    z = solutions['zone_id'][i] #get the zone number
    date = datetime(solutions['year'][i], solutions['month'][i], solutions['day'][i])
    d = (date - minDate).days #total days
    wd = (1 if date.weekday() < 5 else 0)
    for j in range(24):
        hr = 'h{}'.format(j + 1)
        val = solutions[hr][i]
        if z == 21:
            pred = 0
            for k in range(1, 21):
                model = bestModel[s][wd][k][j]
                wIndex = bestWeather[s][wd][k][j]
                T = tempvals[(date.year, date.month, date.day, j, wIndex)]
                inpt = [1, T, T**2, T*d, T**2*d, d]
                pred += sum(inpt[i]*model.params[i] for i in range(len(inpt)))
        else:
            model = bestModel[s][wd][z][j]
            wIndex = bestWeather[s][wd][z][j]
            T = tempvals[(date.year, date.month, date.day, j, wIndex)]
            inpt = [1, T, T**2, T*d, T**2*d, d]
            pred = sum(inpt[i]*model.params[i] for i in range(len(inpt)))
        num += (pred - val)**2 * solutions['weight'][i]
        denom += solutions['weight'][i]
        
print('WMSE is: ', (num/denom)**0.5)


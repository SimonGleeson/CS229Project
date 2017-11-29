import pandas as pd
import csv
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt

path = os.getcwd()

#create a dict that stores the times and loads of each zone
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




"""
#colors
colors = ['aqua', 'azure', 'coral', 'lavender', 'lightgreen', 'grey', 'orangered', 'wheat', 'purple', 'tomato', 'sienna']

###Generate some exploratory plots
for i in range(1, 12):
    temp = 'temp_{}'.format(i)
    load = 'load_{}'.format(i)
    plt.scatter(temps[temp], loads[load], c='xkcd:{}'.format(colors[i-1]))
    plt.title('Temperature versus Load for zone {}'.format(i))
    plt.xlabel('Temperature (fahrenheit)')
    plt.ylabel('Load (kWh)?')
    plt.savefig('plots/tempvsload{}'.format(i), bbox_inches='tight')
    plt.clf()


#Plot a day in winter for each zone - Jan 17
for i in range(1, 22):
    plt.plot(loads['time_{}'.format(i)][384:408], loads['load_{}'.format(i)][384:408], label = 'Zone{}.'format(i))
    plt.legend()
    plt.savefig('plots/Winter_jan_17', bbox_inches='tight')
"""

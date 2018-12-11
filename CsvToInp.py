import csv
import sys
import numpy
import matplotlib.pyplot as plt

def extractCSVData(cwd, fileName):
    with open(cwd + fileName + '.csv', 'r') as fname:
        dataFile = list(csv.reader(fname))
    return dataFile


cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_25PER/HPC_25PER/S7_25PER_new3/'
filename = ['ElecpotentialsS7_25PER_new3end']

for fname in filename:
    elecData = extractCSVData(cwd, fname)

    with open(cwd + fname + '.inp', 'w') as fwrite:
        for count,i in enumerate(elecData):
            fwrite.write('RVE.' + str(count+1) + ', \t' + i[0] + '\n')
    print('{} written'.format(cwd+fname + '.inp'))

import csv
# import sys
# import numpy
# import matplotlib.pyplot as plt

def extractCSVData(cwd, fileName):
    with open(cwd + fileName + '.csv', 'r') as fname:
        dataFile = list(csv.reader(fname))
    return dataFile


# cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_34PER/HPC_34PER/'
# filename = ['S1_34PER_new2/ElecpotentialsS1_34PER_new2330','S1_34PER_new2/ElecpotentialsS1_34PER_new2660',
#             'S1_34PER_new2/ElecpotentialsS1_34PER_new21650', 'S4_34PER_new2/ElecpotentialsS4_34PER_new2430',
#             'S6_34PER_new2/ElecpotentialsS6_34PER_new2end']

# cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_42PER/HPC_42PER/'
# filename = ['S1_42PER_new2/ElecpotentialsS1_42PER_new2327','S1_42PER_new2/ElecpotentialsS1_42PER_new2763',
#             'S1_42PER_new2/ElecpotentialsS1_42PER_new21635', 'S4_42PER_new3/ElecpotentialsS4_42PER_new3430',
#             'S6_42PER_new3/ElecpotentialsS6_42PER_new3end']

cwd = '/home/cerecam/Desktop/RVE_25_34_42_50/2M_NEW_96x96x96_50PER/HPC_50PER/'
filename = ['S1_50PER_new3/ElecpotentialsS1_50PER_new3327','S1_50PER_new3/ElecpotentialsS1_50PER_new3763',
            'S1_50PER_new3/ElecpotentialsS1_50PER_new31635', 'S3_50PER_new3/ElecpotentialsS3_50PER_new3end',
            'S6_50PER_new3/ElecpotentialsS6_50PER_new3end']

for fname in filename:
    elecData = extractCSVData(cwd, fname)

    with open(cwd + fname + '.inp', 'w') as fwrite:
        for count,i in enumerate(elecData):

            fwrite.write('RVE.' + str(count+1) + ', \t' + i[0] + '\n')
    print('{} written'.format(cwd+fname + '.inp'))

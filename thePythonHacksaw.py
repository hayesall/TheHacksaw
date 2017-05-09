'''
BoostSRL-Hacksaw v0.02
   "Now with 90% more Python!"
   Written by Alexander L. Hayes
   hayesall@indiana.edu
   Last updated: May 9, 2017

Sample Calls:
   $ python thePythonHacksaw.py v1-0.jar
'''

from __future__ import print_function
from scipy import stats
from tabulate import tabulate
import numpy as np

EPOCHS = 1
TREES = 10
AUCJARPATH = ' -aucJarPath .'

# DATASETS: a list of tuples: 'Name-of-directory', 'target'
DATASETS = [#['Father', 'father'],
            #['Toy-Cancer', 'cancer'],
            ['WebKB', 'faculty'],
            #['IMDB', 'female_gender'], 
            ['Cora', 'sameauthor']]

for e in range(EPOCHS):
    for d in DATASETS:

        dataset = d[0]
        target = d[1]
        # java -jar [n] -l -train datasets/[SET]/train/ -target [TARGET] -trees TREES > trainlog.txt
        # java -jar [n] -i -model datasets/[SET]/train/models/ -test datasets/[SET]/test/ -target [TARGET] AUCJARPATH -trees TREES > testlog.txt

	#rm -rf "datasets/$SET/train/models/*"

        print('java -jar v1-0.jar -l -train datasets/' + dataset + '/train/ -target ' + target + ' -trees ' + str(TREES) + ' > trainlog.txt')
        print('java -jar v1-0.jar -i -model datasets/' + dataset + '/train/models/ -test datasets/' + dataset + '/ -target ' + target + AUCJARPATH + ' -trees ' + str(TREES) + ' > testlog.txt')

        #print(dataset, target)

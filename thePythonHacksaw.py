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
#from tabulate import tabulate
import numpy as np
import os
import re
import sys

# https://github.com/google/python-subprocess32
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess

EPOCHS = 25
TREES = 10
AUCJARPATH = ' -aucJarPath .'

# DATASETS: a list of tuples: 'Name-of-directory', 'target'

DATASETS = [['Cora', 'sameauthor', 9],
            ['WebKB', 'faculty', 5]]

ALGOS = [['RDN-Boost', '']]

FLAGS = ['tushar', '-e', '-rw', '-w', '-s']

for d in DATASETS:
    
    dataset = d[0]
    target = d[1]
    number_of_features = d[2]

    for a in ALGOS:

        params = a[1]

        for f in FLAGS:
            
            if f in ['-rw', '-w', '-s']:
                for n in range(number_of_features):

                    traintime = []
                    roc = []
                    pr = []

                    print(dataset, '| # of features:', n + 1, '| flag:', f)
                    for e in range(EPOCHS):
                        
                        #print(dataset, '| # of features:', n + 1, '| flag:', f, '| epoch:', e)

                        # Extra parameters to Cora Modes (won't work without them):
                        if dataset == 'Cora':
                            CALL = 'echo -e "setParam: maxTreeDepth=3.\nsetParam: nodeSize=2." > datasets/Cora/cora_bk.txt'
                            p = subprocess.Popen(CALL, shell=True)
                            os.waitpid(p.pid, 0)

                        # Create the modes file
                        CALL = 'python walker2.py --number ' + str(n+1) + ' ' + f + ' ' + dataset + '.mayukh | grep "mode:" >> datasets/' + dataset + '/' + dataset.lower() + '_bk.txt'
                        p = subprocess.Popen(CALL, shell=True)
                        os.waitpid(p.pid, 0)

                        # Call RDN-Boost Training
                        #print('Training')

                        CALL = 'java -jar v1-0.jar -l -train datasets/' + dataset + '/train/ ' + params + '-target ' + target + ' -trees ' + str(TREES) + ' > trainlog.txt'
                        p = subprocess.Popen(CALL, shell=True)
                        os.waitpid(p.pid, 0)

                        # Find the time from the log file
                        text = open('trainlog.txt','r').read()
                        line = re.findall(r'trees\): \d*.\d*', text)
                        traintime.append(float(line[0].split()[1]))

                        # Call RDN-Boost Testing
                        #print('Testing')
                        
                        CALL = 'java -jar v1-0.jar -i -model datasets/' + dataset + '/train/models/ -test datasets/' + dataset + '/test/ -target ' + target + AUCJARPATH + ' -trees ' + str(TREES) + ' > testlog.txt'
                        #subprocess.call(CALL.split())
                        p = subprocess.Popen(CALL, shell=True)
                        os.waitpid(p.pid, 0)
                        
                        text = open('testlog.txt','r').read()
                        line = re.findall(r'AUC ROC   = \d.\d*|AUC PR    = \d.\d*', text)
                        # ROC
                        roc.append(float(line[0].split()[3]))
                        # PR
                        pr.append(float(line[1].split()[3]))
                    print('Training Time |', np.mean(traintime), '+-', np.std(traintime))
                    print('AUC ROC       |', np.mean(roc), '+-', np.std(roc))
                    print('AUC PR        |', np.mean(pr), '+-', np.std(pr))
                    #exit()
                exit()
            else:
                for e in range(EPOCHS):
                    print(dataset, '| flag:', f, '| epoch:', e)






'''
DATASETS = [['Father', 'father'],
            ['Toy-Cancer', 'cancer'],
            ['WebKB', 'faculty'],
            ['IMDB', 'female_gender'],
            ['Cora', 'sameauthor']]

ALGOS = [['RDN-Boost', ''],
         ['Soft Margin with alpha(0.5) and beta(-2)', '-softm 0.5 -beta -2 '],
         ['Soft Margin with alpha(2) and beta(-10)', '-softm 2 -beta -10 '],
         ['MLN-Boost', '-mln '],
         ['MLN-Boost with -mlnClause', '-mln -mlnClause '],
         ['LSTree Boosting Regression', '-reg ']]
'''


'''
BoostSRL-Hacksaw v0.02
   "Now with 90% more Python!"
   Written by Alexander L. Hayes
   hayesall@indiana.edu
   Last updated: May 9, 2017

Sample Calls:
   $ python thePythonHacksaw.py
'''

from __future__ import print_function
from scipy import stats
from sklearn import cross_validation

#from tabulate import tabulate
import os
import re
import sys

import numpy as np
import matplotlib.pyplot as plt

# https://github.com/google/python-subprocess32
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess

EPOCHS = 2
TREES = 5
RDNJARPATH = ' v1-0.jar '
AUCJARPATH = ' -aucJarPath .'

DATASETS = [['Cora', 'sameauthor', 9],
            ['WebKB', 'faculty', 5]]

ALGOS = [['RDN-Boost', '']]

FLAGS = ['tushar', '-e', '-rw', '-w', '-s']

def main():

    for d in DATASETS:

        dataset = d[0]
        target = d[1]
        number_of_features = d[2]

        for a in ALGOS:

            params = a[1]

            for f in FLAGS:
                print(dataset, '| flag:', f)

                training_time_means, training_time_stds = [], []
                roc_means, roc_stds = [], []
                pr_means, pr_stds = [], []
                
                if f in ['-rw', '-w', '-s']:
                    # Random Walk, Walk, or Shortest Walk

                    for n in range(number_of_features):
                        traintime, roc, pr = [], [], []
                        
                        print(dataset, '| # of features:', n + 1, '| flag:', f)
                        
                        for e in range(EPOCHS):
                            
                            # Create the modes file for this Train/Test epoch
                            construct_modes(dataset, f, NUMBER=n)

                            # BoostSRL Training
                            train_model(dataset, params, target)

                            # Find the time (in seconds) from the log file
                            traintime.append(get_training_time())

                            # BoostSRL Testing
                            test_model(dataset, params, target)

                            # Find the AUC ROC and AUC PR
                            roc_score, pr_score = get_roc_and_pr_score()
                            roc.append(roc_score)
                            pr.append(pr_score)
                        
                        # Calculate mean and standard deviation for Training Time, AUC ROC, and AUC PR
                        training_mean, training_std = np.mean(traintime), np.std(traintime)
                        auc_roc_mean, auc_roc_std = np.mean(roc), np.std(roc)
                        auc_pr_mean, auc_pr_std = np.mean(pr), np.std(pr)

                        # Update the arrays holding the values, these will be used for plotting the information
                        training_time_means.append(training_mean)
                        training_time_stds.append(training_std)
                        roc_means.append(auc_roc_mean)
                        roc_stds.append(auc_roc_std)
                        pr_means.append(auc_pr_mean)
                        pr_stds.append(auc_pr_std)
                        
                        '''
                        print_information(training_mean, training_std,
                                          auc_roc_mean, auc_roc_std,
                                          auc_pr_mean, auc_pr_std)
                        '''

                    name_to_save = dataset + '-' + f + '-' + str(EPOCHS) + '.png'

                    plot_errorbars(training_time_means, training_time_stds,
                                   roc_means, roc_stds,
                                   pr_means, pr_stds, name_to_save)
                    log_progress(training_time_means, training_time_stds,
                                 roc_means, roc_stds,
                                 pr_means, pr_stds, name_to_save)
                    exit()
                    
                else:
                    # for now, do not worry about these while I work on the code for them
                    continue
                    
                    for e in range(EPOCHS):
                        print(dataset, '| flag:', f, '| epoch:', e)
                        
def import_data(file_to_read):
    if os.path.isfile(file_to_read):
        with open(file_to_read, 'r') as f:
            data = f.read().splitlines()
        return data
    else:
        raise('Error, there were problems when reading ' + file_to_read)

def data_validation(data):
    #x_train, x_test, y_train, y_test = cross_validation()
    pass

def call_process(call):
    p = subprocess.Popen(call, shell=True)
    os.waitpid(p.pid, 0)

def construct_modes(dataset, flag, NUMBER=None):
    # Extra parameters to Cora Modes (won't work without them):
    if dataset == 'Cora':
        call_process('echo -e "setParam: maxTreeDepth=3.\nsetParam: nodeSize=2." > datasets/Cora/cora_bk.txt')

    # Create the modes file
    if NUMBER is not None:
        CALL = 'python walker2.py --number ' + str(NUMBER) + ' ' + flag + ' ' + dataset + \
               '.mayukh | grep "mode:" >> datasets/' + dataset + '/' + dataset.lower() + '_bk.txt'
        call_process(CALL)

def train_model(dataset, params, target):
    # BoostSRL Training
    CALL = 'java -jar' + RDNJARPATH + '-l -train datasets/' + dataset + '/train/ ' + params + '-target ' + \
           target + ' -trees ' + str(TREES) + ' > trainlog.txt'
    call_process(CALL)

def test_model(dataset, params, target):
    # BoostSRL Testing
    CALL = 'java -jar' + RDNJARPATH + '-i -model datasets/' + dataset + '/train/models/ -test datasets/' + \
           dataset + '/test/ -target ' + target + AUCJARPATH + ' -trees ' + str(TREES) + ' > testlog.txt'
    call_process(CALL)

def get_training_time():
    text = open('trainlog.txt', 'r').read()
    line = re.findall(r'trees\): \d*.\d* seconds', text)
    if not line:
        # Seconds should always be a decimal value, otherwise we need to deal in minutes and seconds
        line = re.findall(r'trees\): \d* minutes and \d*.\d* seconds', text)
        # Convert the minutes into seconds and add the seconds:
        splitline = line[0].split()
        seconds = float(splitline[1] * 60 + float(splitline[4]))
    else:
        seconds = float(line[0].split()[1])
    return seconds

def get_roc_and_pr_score():
    text = open('testlog.txt','r').read()
    line = re.findall(r'AUC ROC   = \d.\d*|AUC PR    = \d.\d*', text)
    roc_score = float(line[0].split()[3])
    pr_score = float(line[1].split()[3])
    return roc_score, pr_score

def print_information(training_mean, training_std, auc_roc_mean, auc_roc_std, auc_pr_mean, auc_pr_std):
    print('Training Time |', training_mean, '+-', training_std)
    print('AUC ROC       |', auc_roc_mean, '+-', auc_roc_std)
    print('AUC PR        |', auc_pr_mean, '+-', auc_pr_std)

def log_progress(training_time_means, training_time_stds, roc_means, roc_stds, pr_means, pr_stds, name_to_save):
    print('Saving information for', name_to_save, 'to file.')
    with open('hacksaw_log.txt', 'a') as f:
        f.write(name_to_save + '\n' + \
                str(training_time_means) + '\n' + str(training_time_stds) + '\n' + \
                str(roc_means) + '\n' + str(roc_stds) + '\n' + \
                str(pr_means) + '\n' + str(pr_stds) + '\n')

def plot_errorbars(training_time_means, training_time_stds, roc_means, roc_stds, pr_means, pr_stds, name_to_save):
    print('Saving image for', name_to_save)
    
    x_axis = range(len(training_time_means)+1)[1:]
    fig, (ax0, ax1, ax2) = plt.subplots(ncols=3, figsize=(15,5))

    # Name at the top
    fig.suptitle(name_to_save)
    
    # ax0: Time
    ax0.errorbar(x_axis, training_time_means, yerr=training_time_stds, fmt='-o')
    ax0.set_xlabel('Number of Steps')
    ax0.set_ylabel('Time')
    ax0.set_title('Training Time')
    ax0.set_xlim([0, len(training_time_means)+1])
    ax0.set_ylim([0, max(training_time_means) + max(training_time_stds) + 1])
    
    # ax1: AUC ROC
    ax1.errorbar(x_axis, roc_means, yerr=roc_stds, fmt='-o')
    ax1.set_xlabel('Number of Steps')
    ax1.set_ylabel('AUC ROC')
    ax1.set_title('AUC ROC')
    ax1.set_xlim([0, len(roc_means)+1])
    ax1.set_ylim([0.4,1])
    
    # ax2: AUC PR
    ax2.errorbar(x_axis, pr_means, yerr=pr_stds, fmt='-o')
    ax2.set_xlabel('Number of Steps')
    ax2.set_ylabel('AUC PR')
    ax2.set_title('AUC PR')
    ax2.set_xlim([0, len(pr_means)+1])
    ax2.set_ylim([0.4,1])
    
    plt.savefig(name_to_save, dpi=600)

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

if __name__ == '__main__': main()

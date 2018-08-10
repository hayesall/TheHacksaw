'''
Comparator for the autograder
read in file at $1 and $2
'''
from __future__ import print_function
import os
import sys

import numpy as np

SENSITIVITY = 0.03


class Error:
    """
    Measure the error to guage performance.
    """

    def __init__(self, A, B):
        self.mae = self.mean_absolute_error(A, B)
        self.mse = self.mean_square_error(A, B)
        self.rmse = np.sqrt(self.mse)

    def mean_absolute_error(self, A, B):
        return np.abs(np.subtract(A, B)).mean()

    def mean_square_error(self, A, B):
        return np.square(np.subtract(A, B)).mean()

    def root_mean_square_error(self, A, B):
        return np.sqrt(mean_square_error(A, B))


def compare(file1, file2):
    """
    Compare the contents of two files.

    Returns a 3-tuple of floats measuring error:
        (mean_absolute_error, mean_square_error, root_mean_square_error)
    """

    lines1, lines2 = [], []

    with open(file1, 'r') as f:
        f1lines = f.read().splitlines()
        for line in f1lines:
            lines1.append(float(line.split()[-1]))

    with open(file2, 'r') as f:
        f2lines = f.read().splitlines()
        for line in f2lines:
            lines2.append(float(line.split()[-1]))

    A = np.array(lines1)
    B = np.array(lines2)

    E = Error(A, B)
    return E.mae, E.mse, E.rmse

    '''
    # Start at 0 and add one every time a difference is encountered.
    differences = 0
    total = len(lines1)

    print('Results for:', file1, file2)

    for p in range(len(lines1)):
        diff = abs(lines1[p] - lines2[p])
        if diff > SENSITIVITY:
            print('Line', str(p+1), f1lines[p].split(')')[0] + ')')
            print('FOUND:', lines1[p],
                  '| EXPECTED:', lines2[p],
                  '| DIFF:', diff)
            differences += 1

    return total, differences, SENSITIVITY, total - differences
    '''

if __name__ == '__main__':

    args = sys.argv[1:]
    if len(args) != 2:
        print('Error, specify two files to compare.')
        print('       $ python compare.py [COMPARE-FROM] [COMPARE-TO]')
        exit(2)

    if ((os.path.isfile(args[0])) and (os.path.isfile(args[1]))):
        file1 = args[0]
        file2 = args[1]
    else:
        print('Error, files could not be found.')
        print('       $ python compare.py [COMPARE-FROM] [COMPARE-TO]')
        exit(2)

    # Compare the two files
    total, differences, sensitivity, correct = compare(file1, file2)

    print('Checked', total, 'lines, found', differences, 'discrepancies at',
          str(sensitivity), 'sensitivity.', str(correct) + '/' + str(total))

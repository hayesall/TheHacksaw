'''
Comparator for the autograder
read in file at $1 and $2
'''
from __future__ import print_function
import os
import sys

SENSITIVITY = 0.05

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

lines1 = []
lines2 = []

with open(file1,'r') as f:
    file1lines = f.read().splitlines()
    for line in file1lines:
        lines1.append(float(line.split()[-1]))
with open(file2,'r') as f:
    file2lines = f.read().splitlines()
    for line in file2lines:
        lines2.append(float(line.split()[-1]))

#print(lines1)
#print(lines2)

# start at 0 and add every time a difference is encountered

# check the absolute difference between lines1 and lines2
if not ((len(lines1)) == (len(lines2))):
    print('Error, files are not the same length, cannot compare them.')
    print('       $ python compare.py [COMPARE-FROM] [COMPARE-TO]')
    exit(2)

differences = 0
total = len(lines1)

print('Results for:', file1, file2)

for p in range(len(lines1)):
    diff = abs(lines1[p] - lines2[p])
    if diff > SENSITIVITY:
        print('Line', str(p+1), file1lines[p].split(')')[0] + ')')
        print('FOUND:', lines1[p], '| EXPECTED:', lines2[p], '| DIFF:', diff)
        differences += 1

print('Checked', total, 'lines, found', differences, 'discrepancies at', str(SENSITIVITY), 'sensitivity.', str(total - differences) + '/' + str(total))

from __future__ import print_function
import json
import os
import subprocess
import sys

'''
Import a json file and convert it into a series of bash arrays.
'''

class CommandifyException(Exception):
    def handle(self):
        print(self.message)

class CmdArguments:

    def __init__(self):
        self.arg = sys.argv[1:]

    def import_and_check(self):

        if not self.arg:
            raise(CommandifyException('Error on argument parsing, please specify a file to read from.'))
        elif not (len(self.arg) == 1):
            raise(CommandifyException('Error on argument parsing, exactly one file needs to be specified.'))
        elif not (os.path.isfile(self.arg[0])):
            raise(CommandifyException('Error on argument parsing, file does not exist.'))
        else:
            print(self.arg[0])

class BashifyTheJSON:

    def __init__(self):
        self.arg = c.arg
        print(self.arg)
        print('hello')
    
    #print(self.arg)

if __name__ == '__main__':
    c = CmdArguments()
    c.import_and_check()
    #print(c.arg)
    
    b = BashifyTheJSON()

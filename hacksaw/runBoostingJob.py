"""
A Python script for evaluating BoostSRL .jar files, in order to evaluate
whether the outputs produced between two versions are consistent.
"""

from __future__ import print_function

from .compare import compare

import json
import os
import re
import sys

import numpy as np

# https://github.com/google/python-subprocess32
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess


class RunBoostSRLJob(object):

    aucJarPath = ' -aucJarPath . '

    def __init__(self, jarpath, params, target, trainPath, testPath, trees):
        """
        Initialize a BoostSRL object which performs learning and inference
        on a given data set.
        """

        self.jarpath = jarpath
        self.target = target
        self.train = trainPath

        self.trees = str(trees)

        self.test = testPath
        self.model = trainPath + 'models/'

        # Learning
        self._train_model(params)

        # Inference
        self._test_model(params)

        # Gather Scores
        #print('Gathering scores.')
        #print()


    def _call_process(self, call):
        """
        Use subprocess.Popen to make a system call.

        This is a bit of a "helper function."

        :param call: A system command (e.g. 'echo Hello')
        """
        p = subprocess.Popen(call, shell=True)
        os.waitpid(p.pid, 0)


    def _train_model(self, params):
        """
        Use a jar file to train a model.

        :param jarpath: Path to the jar file used for training.
        :param dataset: Path to the training set.
        :param params: Additional parameters to specify during training.
        :param target: Target predicate to learn.
        :param trees: Number of trees to learn.

        :returns: None
        """

        # Construct a call based on provided arguments.
        CALL = 'java -jar ' + self.jarpath + \
               ' -l -train ' + self.train + \
               ' -target ' + self.target + \
               ' -trees ' + self.trees + " " + \
               params + ' > trainlog.txt'

        self._call_process(CALL)
        #print(CALL)


    def _test_model(self, params):
        """
        Use a jar file to test a model.

        :returns: None.
        """

        # Construct a call based on provided arguments.
        CALL = 'java -jar ' + self.jarpath + \
               ' -i -model ' + self.model + \
               ' -test ' + self.test + \
               ' -target ' + self.target + \
               ' -trees ' + self.trees + \
               ' -aucJarPath . ' + \
               params + ' > testlog.txt'

        self._call_process(CALL)
        #print(CALL)


    def _get_roc_and_pr_score(self):
        pass


def hacksaw(configuration, jar1, jar2):
    """
    The main hacksaw driver function.

    :param configuration: Configuration file loaded via json.
    :type configuration: dict.
    """

    results = {}

    for config in configuration:

        _trainPath = config['trainPath']
        _testPath = config['testPath']
        _target = config['target']
        _trees = config['trees']
        _params = config['params']

        for param in _params:

            error = []

            for _ in range(5):
                # Run BoostSRL based on the specific parameters for a data set.
                RunBoostSRLJob(jar1, param, _target, _trainPath, _testPath, _trees)

                # Store the results in a temporary location
                os.rename(_testPath + 'results_' + _target + '.db', 'results.txt')

                # Run BoostSRL again and compare the results.
                RunBoostSRLJob(jar2, param, _target, _trainPath, _testPath, _trees)

                E = compare('results.txt', _testPath + 'results_' + _target + '.db')
                error.append(list(E))

            error = np.array(error, dtype=np.float64)

            results_key = config['name'] + param
            results[results_key] = list(np.mean(error, axis=0))

            # Dump the results dictionary following an update.
            with open('results.json', 'w') as f:
                json.dump(results, f, indent=2)

    return results

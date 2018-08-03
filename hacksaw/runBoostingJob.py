"""
A Python script for evaluating BoostSRL .jar files, in order to evaluate
whether the outputs produced between two versions are consistent.
"""

from __future__ import print_function

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

    def __init__(self, jarpath, target, trainPath, testPath):
        """
        Initialize a BoostSRL object which performs learning and inference
        on a given data set.
        """

        self.jarpath = jarpath
        self.target = target
        self.train = trainPath
        self.test = testPath

        # Learning
        #self._train_model()

        # Inference
        #self._test_model()


    def _call_process(self, call):
        """
        Use subprocess.Popen to make a system call.

        This is a bit of a "helper function."

        :param call: A system command (e.g. 'echo Hello')
        """
        p = subprocess.Popen(call, shell=True)
        os.waitpid(p.pid, 0)


    def _train_model(self, jarpath, dataset, params, target, trees):
        """
        Use a jar file to train a model.

        :param jarpath: Path to the jar file used for training.
        :param dataset: Path to the training set.
        :param params: Additional parameters to specify during training.
        :param target: Target predicate to learn.
        :param trees: Number of trees to learn.

        :returns: None
        """

        CALL = 'java -jar ' + jarpath + ' -l -train ' + dataset + ' ' + \
               params + ' -target ' + target + ' -trees ' + str(trees) + \
               ' > testlog.txt'
        self._call_process(CALL)


    def _test_model(self, jarpath, model, dataset, params, target, trees):
        """
        Use a jar file to test a model.

        :returns: None.
        """

        CALL = 'java -jar ' + jarpath + ' -i -model ' + model + ' ' + \
               ' -test ' + dataset + ' ' + \
               params + ' -target ' + target + ' -trees ' + str(trees)
        self._call_proces(CALL)


    def _get_roc_and_pr_score(self):
        pass


def hacksaw(configuration):
    """
    The main hacksaw driver function.

    :param configuration: Configuration file loaded via json.
    :type configuration: dict.
    """
    pass

    results = []

    for config in configuration:
        results.append(RunBoostSRLJob(*config))

    return results

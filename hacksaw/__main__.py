"""
The main driver script for the hacksaw.

Takes three items as input:

- A .jar file to evaluate.
- A .jar file to compare against.
- A .json configuration file.
"""

from . import compare
from . import runBoostingJob

import argparse
import codecs
import json

parser = argparse.ArgumentParser()

parser.add_argument('-j1', required=True)
parser.add_argument('-j2', required=True)

parser.add_argument('-f', '--file', required=True,
                    help='Path to a json configuration file.')

args = parser.parse_args()

with codecs.open(args.file) as f:
    config = json.load(f)

runBoostingJob.hacksaw(config)

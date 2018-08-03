"""
The main driver script for the hacksaw.
"""

from . import compare
from . import runBoostingJob

import argparse
import json

with open('config.json') as f:
    config = json.load(f)

runBoostingJob.hacksaw(config)

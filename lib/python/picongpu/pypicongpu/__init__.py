"""
internal representation of params to generate PIConGPU input files
"""
import sys

assert sys.version_info.major > 3 or sys.version_info.minor >= 9, \
    "Python 3.9 is required for PIConGPU"

from .simulation import *
from .runner import *

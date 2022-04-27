"""
PICMI for PIConGPU
"""

import sys

assert sys.version_info.major > 3 or sys.version_info.minor >= 9, \
    "Python 3.9 is required for PIConGPU PICMI"

from .simulation import *
from .grid import *
from .solver import *
from .gaussian_laser import *
from .species import *
from .layout import *
from .distribution import *
from . import constants

import picmistandard

codename = "picongpu"
"""
name of this PICMI implementation
required by PICMI interface
"""

picmistandard.register_constants(constants)

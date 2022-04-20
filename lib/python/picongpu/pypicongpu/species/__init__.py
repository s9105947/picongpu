"""
Data structures to specify and initialize particle species.

Note that the data structure (the classes) here use a different architecure
than both (!) PIConGPU and PICMI.

Please refer to the documentation for a deeper (overview) discussion.

If you want to read the code in order of dependency, I suggest:
Flag, Substance, Attribute, Momentum, Ionization, Position, Placement, Layout,
Profile, Species, InitManager
"""

from . import operation
from . import attribute
from . import constant

from .species import Species
from .initmanager import InitManager

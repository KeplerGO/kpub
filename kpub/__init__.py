__version__ = "1.1.dev"

import os

# Useful constants
PACKAGEDIR = os.path.abspath(os.path.dirname(__file__))
MISSIONS = ['kepler', 'k2']
SCIENCES = ['exoplanets', 'astrophysics']

from .kpub import *

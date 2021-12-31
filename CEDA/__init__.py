import sys
import os

__version__ = "0.2.2"
__author__ = "Terence Lau"


if sys.version_info < (3, 6):
    print(f"CEDA {__version__} requires Python 3.6+")
    sys.exit(1)
del sys

from CEDA import * 
from CEDA import macroecon
from CEDA import market
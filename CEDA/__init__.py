import sys
import os

__version__ = "0.3.6"
__author__ = "Terence Lau"


if sys.version_info < (3, 6):
    print(f"CEDA {__version__} requires Python 3.6+")
    sys.exit(1)
del sys
import sys
import os

__version__ = "0.1.2"
__author__ = "Terence Lau"

__data_source__ = open(os.path.join(
                       os.path.dirname(__file__),
                       'source.md')).read()

if sys.version_info < (3, 6):
    print(f"CEDA {__version__} requires Python 3.6+")
    sys.exit(1)
del sys

from CEDA import * 
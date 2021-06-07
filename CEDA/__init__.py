__version__ = "0.1.1"
__author__ = "TerenceLau"

import sys

if sys.version_info < (3, 6):
    print(f"CEDA {__version__} requires Python 3.6+")
    sys.exit(1)

del sys

from CEDA import * 
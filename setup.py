from setuptools import setup, find_packages
import os
setup(
    name = "CEDApy",
    version = "0.1",
    keywords = "economic data api",
    long_description = open(
    os.path.join(
        os.path.dirname(__file__),
        'README.md'
    )).read(),
    author = "JUNJIE-LIU",
    author_email = "terenceliu1012@outlook.com",
    url = "https://github.com/TerenceLiu98/CEDApy",
    packages = find_packages(),
    license = "MIT"
)
from setuptools import setup, find_packages
import os
setup(
    name = "CEDApy",
    version = "0.1-alpha",
    keywords = "economic data api",
    long_description = open(
    os.path.join(
        os.path.dirname(__file__),
        'README.md'
    )).read(),
    long_description_content_type='text/markdown',
    author = "TerenceCKLau",
    author_email = "terenceliu1012@outlook.com",
    url = "https://github.com/TerenceLiu98/CEDApy",
    packages = find_packages(),
    license = "MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
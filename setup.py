from setuptools import setup, find_packages
import os
setup(
    name = "CEDApy",
    version = "0.2-beta",
    keywords = "economic data",
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
    install_requires=[
        "numpy>=1.15.4",
        "pandas>=0.25",
        "requests>=2.22.0",
        "demjson>=2.2.4",
        "pillow>=6.2.0",
        "xlrd==1.2.0",
        "tqdm>=4.43.0",
        "tabulate>=0.8.6",
        "fake_useragent"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
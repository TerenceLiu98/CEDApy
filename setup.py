from setuptools import setup, find_packages
import os
setup(
    name = "CEDApy",
    version = "0.1.9a",
    keywords = "quantitative economic data",
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
    install_requires=[
        "matplotlib>=3.1.1",
        "numpy>=1.15.4",
        "pandas>=0.25",
        "requests>=2.22.0",
        "demjson>=2.2.4",
        "html5lib>=1.0.1",
        "xlrd==1.2.0",
        "bs4",
        "urllib3>=1.26.5",
        "fake-useragent"
    ],
    license = "MIT",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

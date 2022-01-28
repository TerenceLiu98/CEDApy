# Centralized Economic Data API

![py_version](https://img.shields.io/badge/python-3.6+-brightgreen)
[![PyPI Version](https://img.shields.io/pypi/v/CEDApy.svg)](https://pypi.org/project/CEDApy)
[![Package Status](https://img.shields.io/pypi/status/CEDApy.svg)](https://pypi.org/project/CEDApy/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5229506.svg)](https://doi.org/10.5281/zenodo.5229506)

## Introduction

This is a economic data collecting library, with both `python`

* `python` version: [https://github.com/TerenceLiu98/CEDApy](https://github.com/TerenceLiu98/CEDApy)

### Economic Data

We have included multiple API for banks or statistics deparment of countries/region:

* North America:
  - [x] `FredData` for [Fred Reserve Bank](https://fred.stlouisfed.org/)

* Europe:
  - [x] `ECBData` for [European Central Bank](https://www.ecb.europa.eu/home/html/index.en.html)
  - [x] `EurostatData` for [European Statistics](https://ec.europa.eu/eurostat)

* Asia:
  - [ ] `NBSCData` for [National Bureau of Statistics of China](http://www.stats.gov.cn/english/)
  - [x] `XHData` for [Xinhua](https://www.cnfin.com/data/macro-data/index.html)
  - [x] `BOJData` for [Bank of Japan](https://www.boj.or.jp/en/index.htm/)

### Market Data

We have two api for approaching the market data:

- [x] `marketwatch` for [MarketWatch](https://www.marketwatch.com/)
- [x] `dukascopy` for [Dukascopy Historial Data](https://www.dukascopy.com/swiss/english/marketwatch/historical/)


### Other 

We also collect some interesting data which may useful in your reserach or project
- [x] `EPU` for [Economic Policy Uncertainty](https://www.policyuncertainty.com/) and [Economic Policy Uncertainty in China](https://economicpolicyuncertaintyinchina.weebly.com/)

## Installation

Via the source code

```shell
git clone https://github.com/TerenceLiu98/CEDApy.git
python setup.py install
```

Via the `pypi`:

```shell
python -m pip install CEDApy
```

## How to use

Please check [Wiki](https://github.com/TerenceLiu98/CEDApy/wiki)

## Acknowledgement

* [akshare](https://github.com/jindaxiang/akshare/)
* [EastMoney](https://www.eastmoney.com)
* [St.Louis Federal Reserve Bank](https://fred.stlouisfed.org/), [Chicago Federal Reserve Bank](https://www.chicagofed.org/), [Philadelphia Federal Reserve Bank](https://www.philadelphiafed.org/), [eurostat Economic Indicators](https://ec.europa.eu/eurostat/cache/infographs/economy/desktop/index.html)
* [Europen Central Bank](https://www.ecb.europa.eu)
* [MarketWatch](https://www.marketwatch.com/)
* [Dukascopy](https://www.dukascopy.bank/swiss)

## Other Interesting Project

Here is a list for some related packages or tools that may help you finding the data you want:

* [akshare](https://github.com/jindaxiang/akshare/) - an elegant and simple financial data interface library for Python, built for human beings
* [tushare](https://github.com/waditu/tushare) - a utility for crawling historial data of China stocks
* [investpy](https://github.com/alvarobartt/investpy) - Financial Data Extraction from Investing.com with Python

## If you want to cite...

```txt
@software{terencelau_2021_5229506,
  author       = {TerenceLau},
  title        = {TerenceLiu98/CEDApy: V0.2.2},
  month        = aug,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {V0.2.2},
  doi          = {10.5281/zenodo.5229506},
  url          = {https://doi.org/10.5281/zenodo.5229506}
}
```
import re
import io
import requests
import demjson
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote, urlencode
from fake_useragent import UserAgent

url = {
    "dukascopy": "http://data.deluxelau.com/forex/api/v1.0/getdata?"
}

#?instrument=usdcnh&startdate=2014-01-01&enddate=2014-12-31&timeframe=d1&pricetype=ask&utc=0&volume=false&flat=false

def dukascopy(
        instrument: str,
        startdate: str,
        enddate: str,
        timeframe: str,
        pricetype: str,
        utc: int,
        volume: bool,
        flat: bool):
    tmp_url = url["dukascopy"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "instrument": "{}".format(instrument),
        "startdate": "{}".format(startdate),
        "enddate": "{}".format(enddate),
        "timeframe": "{}".format(timeframe),
        "utc": "{}".format(utc),
        "pricetype": "{}".format(pricetype),
        "volume": "{}".format(str(volume).lower()),
        "flat": "{}".format(str(flat).lower())

    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    output_file = demjson.decode(data_text)
    return pd.json_normalize(output_file)

# example:
""" 
df = dukascopy(instrument = "btcusd", 
               startdate = "2020-01-01",
               enddate = "2021-01-01",
               timeframe = "d1",
               pricetype = "bid",
               utc = 0,
               volume = True,
               flat = True)
"""
import requests
import pandas as pd
from fake_useragent import UserAgent

url = {
    "dukascopy": "https://data.deluxelau.com/api/v1.0/finance/getdata?"
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
        "flat": "{}".format(str(flat).lower()),
        "token": "token=6dc8797f-aa4b-4b8c-b137-cfe9a9ace5a1"

    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    output_file = r.json()
    return pd.json_normalize(output_file)

# example:
""" 
df = dukascopy(instrument = "usdcnh", 
               startdate = "2014-01-01",
               enddate = "2020-01-01",
               timeframe = "m1",
               pricetype = "bid",
               utc = 0,
               volume = False,
               flat = False)
"""
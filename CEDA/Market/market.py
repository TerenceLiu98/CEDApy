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
    "dukascopy": "http://data.uicstat.com/api_1.0",
    "moneywatch": "https://www.marketwatch.com/investing/"
}


def dukascopy(
        instrument: str,
        startdate: str,
        enddate: str,
        timeframe: str,
        pricetype: str,
        volume: bool,
        flat: bool):
    tmp_url = url["dukascopy"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "instrument": "{}".format(instrument),
        "startdate": "{}".format(startdate),
        "enddate": "{}".format(enddate),
        "timeframe": "{}".format(timeframe),
        "pricetype": "{}".format(pricetype),
        "volume": "{}".format(volume),
        "flat": "{}".format(flat)

    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text)
    df = pd.DataFrame(data_json['result'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.columns = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]
    return df

def currency_list(instrument = "eurusd", startdate="01/01/2020", enddate = "01/01/2021"):
    """
    https://www.marketwatch.com/investing/
    """
    tmp_url = url["moneywatch"] + "currency/{}/downloaddatapartial".format(instrument)
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = urlencode({
        "startdate": r"{}".format(startdate),
        "enddate": r"{}".format(enddate),
        "daterange": "d30",
        "frequency": "p1d",
        "csvdownload": "true",
        "downloadpartial": "false",
        "newdates": "false"}, quote_via= quote)
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    Date = []
    for i in range(0, len(df)):
        Date.append(datetime.strptime(df["Date"][i], "%m/%d/%Y"))
    
    df["Date"] = Date
    return df


if __name__ == "__main__":
    data = dukascopy(instrument="eurusd",
                       startdate="2020-01-01",
                       enddate="2021-01-01",
                       timeframe="d1",
                       pricetype="bid",
                       volume=True,
                       flat=True)

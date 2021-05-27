import pandas as pd
import numpy as np
import re
import demjson
import requests
from fake_useragent import UserAgent

# TODO need add comments

url = {
    "eurostat": "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/",
    "ecb": "https://sdw.ecb.europa.eu/servlet/homePageChart?from=dynamic&"
}


def ecb_data():
    """
    Full Name:  Gross Domestic Product
    Description: Billions of Dollars, Quarterly, Seasonally Adjusted Annual Rate
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "GDP",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    return df

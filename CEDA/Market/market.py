import requests
import demjson
import pandas as pd
from fake_useragent import UserAgent

url = {
    "dukascopy": "http://data.uicstat.com/api_1.0"
}

def market_data(instrument:str, startdate:str, enddate:str, timeframe:str, pricetype:str, volume:bool, flat:bool):
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
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

if __name__ == "__main__":
    data = market_data(instrument="eurusd", 
                       startdate="2020-01-01", 
                       enddate="2021-01-01", 
                       timeframe="d1", 
                       pricetype="bid", 
                       volume=True, 
                       flat=True)
import io
import requests
import pandas as pd
from datetime import datetime
from urllib.parse import quote, urlencode
from fake_useragent import UserAgent

url = {
    "moneywatch": "https://www.marketwatch.com/investing/"
}

def forex(instrument="eurusd", startdate="2019-01-01", enddate="2021-01-01"):
    startdate = datetime.strptime(startdate, "%Y-%m-%d").strftime("%m/%d/%y")
    enddate = datetime.strptime(enddate, "%Y-%m-%d").strftime("%m/%d/%y")
    df = pd.DataFrame()

    def _FX(instrument="eurusd", startdate="01/01/2020", enddate="01/01/2021"):
        """
        https://www.marketwatch.com/investing/
        """
        tmp_url = url["moneywatch"] + \
            "currency/{}/downloaddatapartial".format(instrument)
        ua = UserAgent(verify_ssl=False)
        request_header = {"User-Agent": ua.random}
        request_params = urlencode({
            "startdate": r"{}".format(startdate),
            "enddate": r"{}".format(enddate),
            "daterange": "d30",
            "frequency": "p1d",
            "csvdownload": "true",
            "downloadpartial": "false",
            "newdates": "false"}, quote_via=quote)
        r = requests.get(tmp_url, params=request_params.replace(
            "%2F", "/").replace("%20", " ").replace("%3A", ":"), headers=request_header)
        data_text = r.content
        df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
        Date = []
        for i in range(0, len(df)):
            Date.append(datetime.strptime(df["Date"][i], "%m/%d/%Y"))

        df["Date"] = Date
        return df

    for i in range(int(startdate[6:10]), int(enddate[6:10])):
        if i == int(startdate[6:10]):
            tmp_startdate = startdate
        else:
            tmp_startdate = "01/01/" + str(i) + " 00:00:00"
        if (i + 1) == int(enddate[6:10]):
            tmp_enddate = enddate
        else:
            tmp_enddate = "01/01/" + str(i + 1) + " 00:00:00"

        tmp_df = _FX(
            instrument=instrument,
            startdate=tmp_startdate,
            enddate=tmp_enddate)
        if i == int(startdate[6:10]):
            df = tmp_df
        else:
            df = pd.concat([tmp_df, df], axis=0)

    df = df.reset_index(drop=True)
    return df


def index(instrument="vix", startdate="2019-01-01", enddate="2021-01-01", countrycode=None):
    startdate = datetime.strptime(startdate, "%Y-%m-%d").strftime("%m/%d/%y")
    enddate = datetime.strptime(enddate, "%Y-%m-%d").strftime("%m/%d/%y")
    df = pd.DataFrame()

    def _index(instrument="vix", startdate="01/01/2020", enddate="01/01/2021", countrycode=None):
        """
        https://www.marketwatch.com/investing/
        """
        tmp_url = url["moneywatch"] + \
            "index/{}/downloaddatapartial".format(instrument)
        ua = UserAgent(verify_ssl=False)
        request_header = {"User-Agent": ua.random}
        if countrycode == None:
            request_params = urlencode({
                "startdate": r"{}".format(startdate),
                "enddate": r"{}".format(enddate),
                "daterange": "d30",
                "frequency": "p1d",
                "csvdownload": "true",
                "downloadpartial": "false",
                "newdates": "false"}, quote_via=quote)
        elif countrycode != None:
            request_params = urlencode({
                "startdate": r"{}".format(startdate),
                "enddate": r"{}".format(enddate),
                "daterange": "d30",
                "frequency": "p1d",
                "csvdownload": "true",
                "downloadpartial": "false",
                "newdates": "false",
                "countrycode": "{}".format(countrycode)}, quote_via=quote)

        r = requests.get(tmp_url, params=request_params.replace("%2F", "/").replace("%20", " ").replace("%3A", ":"), \
            headers=request_header)
        data_text = r.content
        df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
        Date = []
        for i in range(0, len(df)):
            Date.append(datetime.strptime(df["Date"][i], "%m/%d/%Y"))

        df["Date"] = Date
        return df

    for i in range(int(startdate[6:10]), int(enddate[6:10])):
        if i == int(startdate[6:10]):
            tmp_startdate = startdate
        else:
            tmp_startdate = "01/01/" + str(i) + " 00:00:00"
        if (i + 1) == int(enddate[6:10]):
            tmp_enddate = enddate
        else:
            tmp_enddate = "01/01/" + str(i + 1) + " 00:00:00"

        tmp_df = _index(
            instrument=instrument,
            startdate=tmp_startdate,
            enddate=tmp_enddate, countrycode=countrycode)
        if i == int(startdate[6:10]):
            df = tmp_df
        else:
            df = pd.concat([tmp_df, df], axis=0)

    df = df.reset_index(drop=True)
    return df


def crypto(instrument="btcusd", startdate="2019-01-01", enddate="2021-01-01"):
    startdate = datetime.strptime(startdate, "%Y-%m-%d").strftime("%m/%d/%y")
    enddate = datetime.strptime(enddate, "%Y-%m-%d").strftime("%m/%d/%y")
    df = pd.DataFrame()

    def _crypto(
            instrument="btcusd",
            startdate="01/01/2020",
            enddate="01/01/2021"):
        """
        https://www.marketwatch.com/investing/
        """
        tmp_url = url["moneywatch"] + \
            "cryptocurrency/{}/downloaddatapartial".format(instrument)
        ua = UserAgent(verify_ssl=False)
        request_header = {"User-Agent": ua.random}
        request_params = urlencode({
            "startdate": r"{}".format(startdate),
            "enddate": r"{}".format(enddate),
            "daterange": "d30",
            "frequency": "p1d",
            "csvdownload": "true",
            "downloadpartial": "false",
            "newdates": "false"}, quote_via=quote)
        r = requests.get(tmp_url, params=request_params.replace(
            "%2F", "/").replace("%20", " ").replace("%3A", ":"), headers=request_header)
        data_text = r.content
        df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
        Date = []
        for i in range(0, len(df)):
            Date.append(datetime.strptime(df["Date"][i], "%m/%d/%Y"))

        df["Date"] = Date
        return df

    for i in range(int(startdate[6:10]), int(enddate[6:10])):
        if i == int(startdate[6:10]):
            tmp_startdate = startdate
        else:
            tmp_startdate = "01/01/" + str(i) + " 00:00:00"
        if (i + 1) == int(enddate[6:10]):
            tmp_enddate = enddate
        else:
            tmp_enddate = "01/01/" + str(i + 1) + " 00:00:00"

        tmp_df = _crypto(
            instrument=instrument,
            startdate=tmp_startdate,
            enddate=tmp_enddate)
        if i == int(startdate[6:10]):
            df = tmp_df
        else:
            df = pd.concat([tmp_df, df], axis=0)

    df = df.reset_index(drop=True)
    return df


def stock(
        countrycode="cn",
        instrument="601988",
        startdate="2019-01-01",
        enddate="2021-01-01"):
    startdate = datetime.strptime(startdate, "%Y-%m-%d").strftime("%m/%d/%y")
    enddate = datetime.strptime(enddate, "%Y-%m-%d").strftime("%m/%d/%y")
    df = pd.DataFrame()

    def _stock(
            countrycode="cn",
            instrument="601988",
            startdate="01/01/2020",
            enddate="01/01/2021"):
        """
        https://www.marketwatch.com/investing/
        """
        tmp_url = url["moneywatch"] + \
            "stock/{}/downloaddatapartial".format(instrument)
        ua = UserAgent(verify_ssl=False)
        request_header = {"User-Agent": ua.random}
        request_params = urlencode({
            "startdate": r"{}".format(startdate),
            "enddate": r"{}".format(enddate),
            "daterange": "d30",
            "frequency": "p1d",
            "csvdownload": "true",
            "downloadpartial": "false",
            "newdates": "false",
            "countrycode": "{}".format(countrycode)}, quote_via=quote)
        r = requests.get(tmp_url, params=request_params.replace(
            "%2F", "/").replace("%20", " ").replace("%3A", ":"), headers=request_header)
        data_text = r.content
        df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
        Date = []
        for i in range(0, len(df)):
            Date.append(datetime.strptime(df["Date"][i], "%m/%d/%Y"))

        df["Date"] = Date
        return df

    for i in range(int(startdate[6:10]), int(enddate[6:10])):
        if i == int(startdate[6:10]):
            tmp_startdate = startdate
        else:
            tmp_startdate = "01/01/" + str(i) + " 00:00:00"
        if (i + 1) == int(enddate[6:10]):
            tmp_enddate = enddate
        else:
            tmp_enddate = "01/01/" + str(i + 1) + " 00:00:00"

        if countrycode == "us":
            countrycode = ""
        tmp_df = _stock(
            countrycode=countrycode,
            instrument=instrument,
            startdate=tmp_startdate,
            enddate=tmp_enddate)
        if i == int(startdate[6:10]):
            df = tmp_df
        else:
            df = pd.concat([tmp_df, df], axis=0)

    df = df.reset_index(drop=True)
    return df


if __name__ == "__main__":
    data = FX()

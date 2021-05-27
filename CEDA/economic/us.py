import pandas as pd
import numpy as np
import requests
from fake_useragent import UserAgent
import io

# Main Economic Indicators: https://alfred.stlouisfed.org/release?rid=205
url = {
    "fred_econ": "https://fred.stlouisfed.org/graph/fredgraph.csv?"
}

def gdp_quarterly(startdate="1947-01-01", enddate="2021-01-01"):
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

def gdpc1_quarterly(startdate="1947-01-01", enddate="2021-01-01"):
    """
    Full Name: Real Gross Domestic Product
    Description: Billions of Chained 2012 Dollars, Quarterly, Seasonally Adjusted Annual Rate
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "GDPC1",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    return df

def oecd_gdp_monthly(startdate="1947-01-01", enddate="2021-01-01"):
    """
    Full Name: Real Gross Domestic Product
    Description: Billions of Chained 2012 Dollars, Quarterly, Seasonally Adjusted Annual Rate
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "USALORSGPNOSTSAM",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    return df

def payems_monthly(startdate="1939-01-01", enddate="2021-01-01"):
    """
    Full Name: All Employees, Total Nonfarm
    Description: Thousands of Persons,Seasonally Adjusted, Monthly
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "PAYEMS",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    return df

def unrate_monthly(startdate="1948-01-01", enddate="2021-01-01"):
    """
    Full Name: Unemployment Rate: Aged 15-64: All Persons for the United States
    Description: Percent, Seasonally Adjusted, Monthly, Quarterly and Annually
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "LRUN64TTUSM156S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "LRUN64TTUSQ156S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "LRUN64TTUSA156S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(df_quarterly["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(df_monthly, df_quarterly, on = "DATE", direction = "backward")
    df = pd.merge_asof(df, df_annually, on = "DATE", direction = "backward")
    df.columns = ["Date", "UR_Monthly", "UR_Quarterly", "UR_Annually"]
    return df

def pce_monthly(startdate="1959-01-01", enddate="2021-01-01"):
    """
    Full Name: PCE
    Description: Percent, Monthly, Seasonally Adjusted
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "PCE",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    return df

def cpi(startdate="1960-01-01", enddate="2021-01-01"):
    """
    Full Name: Consumer Price Index: Total All Items for the United States
    Description: Percent, Monthly, Quarterly and Annually, Seasonally Adjusted
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "CPALTT01USM661S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "CPALTT01USQ661S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "CPALTT01USA661S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(df_quarterly["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(df_monthly, df_quarterly, on = "DATE", direction = "backward")
    df = pd.merge_asof(df, df_annually, on = "DATE", direction = "backward")
    df.columns = ["Date", "CPI_Monthly", "CPI_Quarterly", "CPI_Annually"]
    return df

def m1(startdate="1960-01-01", enddate="2021-01-01"):
    """
    Full Name: Consumer Price Index: M3 for the United States
    Description: Growth Rate Previous Period, Monthly, Quarterly and Annually, Seasonally Adjusted
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "MANMM101USM657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "MANMM101USQ657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "MANMM101USA657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(df_quarterly["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(df_monthly, df_quarterly, on = "DATE", direction = "backward")
    df = pd.merge_asof(df, df_annually, on = "DATE", direction = "backward")
    df.columns = ["Date", "M1_Monthly", "M1_Quarterly", "M1_Annually"]
    return df


def m3(startdate="1960-01-01", enddate="2021-01-01"):
    """
    Full Name: Consumer Price Index: M3 for the United States
    Description: Growth Rate Previous Period, Monthly, Quarterly and Annually, Seasonally Adjusted
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "MABMM301USM657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "MABMM301USQ657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "MABMM301USA657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(df_quarterly["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(df_monthly, df_quarterly, on = "DATE", direction = "backward")
    df = pd.merge_asof(df, df_annually, on = "DATE", direction = "backward")
    df.columns = ["Date", "M3_Monthly", "M3_Quarterly", "M3_Annually"]
    return df

def ltgby(startdate="1955-01-01", enddate="2021-01-01"):
    """
    Full Name: Long-Term Government Bond Yields: 10-year: Main (Including Benchmark) for the United States
    Description: Percent,Not Seasonally Adjusted, Monthly, Quarterly and Annually
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "IRLTLT01USM156N",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "IRLTLT01USQ156N",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "IRLTLT01USA156N",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(df_quarterly["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(df_monthly, df_quarterly, on = "DATE", direction = "backward")
    df = pd.merge_asof(df, df_annually, on = "DATE", direction = "backward")
    df.columns = ["Date", "ltgby_Monthly", "ltgby_Quarterly", "ltgby_Annually"]
    return df

def gdp_ipd(startdate="1955-01-01", enddate="2021-01-01"):
    """
    Full Name: Long-Term Government Bond Yields: 10-year: Main (Including Benchmark) for the United States
    Description: Percent,Not Seasonally Adjusted, Monthly, Quarterly and Annually
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "USAGDPDEFQISMEI",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "USAGDPDEFAISMEI",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(df_quarterly["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(df_quarterly, df_annually, on = "DATE", direction = "backward")
    df.columns = ["Date", "gdp_ipd_Quarterly", "gdp_ipd_Annually"]
    return df

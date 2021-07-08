import pandas as pd
import numpy as np
import requests
from fake_useragent import UserAgent
import io
import os
import time
import json
import demjson
from datetime import datetime
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Main Economic Indicators: https://alfred.stlouisfed.org/release?rid=205
url = {
    "fred_econ": "https://fred.stlouisfed.org/graph/fredgraph.csv?",
    "philfed": "https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/",
    "chicagofed": "https://www.chicagofed.org/~/media/publications/",
    "OECD": "https://stats.oecd.org/sdmx-json/data/DP_LIVE/"
}

def date_transform(df, format_origin, format_after):
    return_list = []
    for i in range(0, len(df)):
        return_list.append(datetime.strptime(df[i], format_origin).strftime(format_after))
    
    return return_list

def gdp_quarterly(startdate="1947-01-01", enddate="2021-01-01"):
    """
    Full Name:  Gross Domestic Product
    Description: Billions of Dollars, Quarterly, Seasonally Adjusted Annual Rate
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "GDP",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df.columns = ["Date", "GDP"]
    df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d")
    df["GDP"] = df["GDP"].astype(float)
    return df


def gdpc1_quarterly(startdate="1947-01-01", enddate="2021-01-01"):
    """
    Full Name: Real Gross Domestic Product
    Description: Billions of Chained 2012 Dollars, Quarterly, Seasonally Adjusted Annual Rate
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "GDPC1",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
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
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "USALORSGPNOSTSAM",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
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
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "PAYEMS",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df.columns = ["Date", "Payems"]
    df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d")
    df["Payems"] = df["Payems"].astype(float)
    return df

def ppi():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=968&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PPIACO,PCUOMFGOMFG&scale=left,left&cosd=1913-01-01,1984-12-01&coed=2021-04-01,2021-04-01&line_color=%234572a7,%23aa4643&link_values=false,false&line_style=solid,solid&mark_type=none,none&mw=3,3&lw=2,2&ost=-99999,-99999&oet=99999,99999&mma=0,0&fml=a,a&fq=Monthly,Monthly&fam=avg,avg&fgst=lin,lin&fgsnd=2020-02-01,2020-02-01&line_index=1,2&transformation=lin,lin&vintage_date=2021-06-10,2021-06-10&revision_date=2021-06-10,2021-06-10&nd=1913-01-01,1984-12-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        "PPIACO": "Producer Price Index by Commodity: All Commodities",
        "PCUOMFGOMFG": "Producer Price Index by Industry: Total Manufacturing Industries"
    }
    df.replace(".", np.nan, inplace = True)
    df.columns = ["Date", "PPI_C", "PPI_I"]
    df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d")
    df[["PPI_C", "PPI_I"]] = df[["PPI_C", "PPI_I"]].astype(float)
    return df

def pmi():
    t = time.time()
    res = requests.get(
    f"https://cdn.jin10.com/dc/reports/dc_usa_ism_pmi_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国ISM制造业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "28",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_ism_pmi"
    temp_df = temp_df.astype("float")
    PMI_I = pd.DataFrame()
    PMI_I["Date"] = pd.to_datetime(temp_df.index, format = "%Y-%m-%d")
    PMI_I["ISM_PMI_I"] = np.array(temp_df).astype(float)

    t = time.time()
    res = requests.get(
        f"https://cdn.jin10.com/dc/reports/dc_usa_ism_non_pmi_all.js?v={str(int(round(t * 1000))), str(int(round(t * 1000)) + 90)}"
    )
    json_data = json.loads(res.text[res.text.find("{"): res.text.rfind("}") + 1])
    date_list = [item["date"] for item in json_data["list"]]
    value_list = [item["datas"]["美国ISM非制造业PMI报告"] for item in json_data["list"]]
    value_df = pd.DataFrame(value_list)
    value_df.columns = json_data["kinds"]
    value_df.index = pd.to_datetime(date_list)
    temp_df = value_df["今值"]
    url = "https://datacenter-api.jin10.com/reports/list_v2"
    params = {
        "max_date": "",
        "category": "ec",
        "attr_id": "29",
        "_": str(int(round(t * 1000))),
    }
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://datacenter.jin10.com",
        "pragma": "no-cache",
        "referer": "https://datacenter.jin10.com/reportType/dc_usa_michigan_consumer_sentiment",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-app-id": "rU6QIu7JHe2gOUeR",
        "x-csrf-token": "",
        "x-version": "1.0.0",
    }
    r = requests.get(url, params=params, headers=headers)
    temp_se = pd.DataFrame(r.json()["data"]["values"]).iloc[:, :2]
    temp_se.index = pd.to_datetime(temp_se.iloc[:, 0])
    temp_se = temp_se.iloc[:, 1]
    temp_df = temp_df.append(temp_se)
    temp_df.dropna(inplace=True)
    temp_df.sort_index(inplace=True)
    temp_df = temp_df.reset_index()
    temp_df.drop_duplicates(subset="index", inplace=True)
    temp_df.set_index("index", inplace=True)
    temp_df = temp_df.squeeze()
    temp_df.index.name = None
    temp_df.name = "usa_ism_non_pmi"
    temp_df = temp_df.astype("float")
    PMI_NI = pd.DataFrame()
    PMI_NI["Date"] = pd.to_datetime(temp_df.index, format = "%Y-%m-%d")
    PMI_NI["ISM_PMI_NI"] = np.array(temp_df).astype(float)
    PMI = pd.merge_asof(PMI_I, PMI_NI, on = "Date")
    return PMI


def unrate(startdate="1948-01-01", enddate="2021-01-01"):
    """
    Full Name: Unemployment Rate: Aged 15-64: All Persons for the United States
    Description: Percent, Seasonally Adjusted, Monthly, Quarterly and Annually
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "LRUN64TTUSM156S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "LRUN64TTUSQ156S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(
        df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "LRUN64TTUSA156S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(
        df_annually["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(
        df_monthly,
        df_quarterly,
        on="DATE",
        direction="backward")
    df = pd.merge_asof(df, df_annually, on="DATE", direction="backward")
    df.columns = ["Date", "UR_Monthly", "UR_Quarterly", "UR_Annually"]
    return df


def erate(startdate="1955-01-01", enddate="2021-01-01"):
    """
    Full Name: Employment Rate: Aged 25-54: All Persons for the United States
    Description: Percent,Seasonally Adjusted, Monthly, Quarterly and Annually
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "LREM25TTUSM156S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "LREM25TTUSQ156S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(
        df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "LREM25TTUSA156S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(
        df_annually["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(
        df_monthly,
        df_quarterly,
        on="DATE",
        direction="backward")
    df = pd.merge_asof(df, df_annually, on="DATE", direction="backward")
    df.columns = ["Date", "ER_Monthly", "ER_Quarterly", "ER_Annually"]


def pce_monthly(startdate="1959-01-01", enddate="2021-01-01"):
    """
    Full Name: PCE
    Description: Percent, Monthly, Seasonally Adjusted
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "PCE",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
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
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "CPALTT01USM661S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "CPALTT01USQ661S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(
        df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "CPALTT01USA661S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(
        df_annually["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(
        df_monthly,
        df_quarterly,
        on="DATE",
        direction="backward")
    df = pd.merge_asof(df, df_annually, on="DATE", direction="backward")
    df.columns = ["Date", "CPI_Monthly", "CPI_Quarterly", "CPI_Annually"]
    df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d")
    df[["CPI_Monthly", "CPI_Quarterly", "CPI_Annually"]] = df[["CPI_Monthly", "CPI_Quarterly", "CPI_Annually"]].astype(float)
    return df


def m1(startdate="1960-01-01", enddate="2021-01-01"):
    """
    Full Name: Consumer Price Index: M3 for the United States
    Description: Growth Rate Previous Period, Monthly, Quarterly and Annually, Seasonally Adjusted
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "WM1NS",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_weekly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_weekly["DATE"] = pd.to_datetime(df_weekly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "MANMM101USM657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "MANMM101USQ657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(
        df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "MANMM101USA657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(
        df_annually["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(df_weekly, df_monthly, on="DATE", direction="backward")
    df = pd.merge_asof(df, df_quarterly, on="DATE", direction="backward")
    df = pd.merge_asof(df, df_annually, on="DATE", direction="backward")
    df.columns = [
        "Date",
        "M1_Weekly",
        "M1_Monthly",
        "M1_Quarterly",
        "M1_Annually"]
    return df


def m2(startdate="1960-01-01", enddate="2021-01-01"):
    """
    Full Name: M2 Money Stock
    Description: Seasonally Adjusted, Weekly, Monthly, Quarterly and Annually, Seasonally Adjusted
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "WM2NS",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_weekly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_weekly["DATE"] = pd.to_datetime(df_weekly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "M2SL",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(df_weekly, df_monthly, on="DATE", direction="backward")
    df.columns = ["Date", "M2_Weekly", "M2_Monthly"]
    return df


def m3(startdate="1960-01-01", enddate="2021-01-01"):
    """
    Full Name: Consumer Price Index: M3 for the United States
    Description: Growth Rate Previous Period, Monthly, Quarterly and Annually, Seasonally Adjusted
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "MABMM301USM657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "MABMM301USQ657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(
        df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "MABMM301USA657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(
        df_annually["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(
        df_monthly,
        df_quarterly,
        on="DATE",
        direction="backward")
    df = pd.merge_asof(df, df_annually, on="DATE", direction="backward")
    df.columns = ["Date", "M3_Monthly", "M3_Quarterly", "M3_Annually"]
    return df


def ltgby_10(startdate="1955-01-01", enddate="2021-01-01"):
    """
    Full Name: Long-Term Government Bond Yields: 10-year: Main (Including Benchmark) for the United States
    Description: Percent,Not Seasonally Adjusted, Monthly, Quarterly and Annually
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "IRLTLT01USM156N",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "IRLTLT01USQ156N",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(
        df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "IRLTLT01USA156N",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(
        df_annually["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(
        df_monthly,
        df_quarterly,
        on="DATE",
        direction="backward")
    df = pd.merge_asof(df, df_annually, on="DATE", direction="backward")
    df.columns = ["Date", "ltgby_Monthly", "ltgby_Quarterly", "ltgby_Annually"]
    return df


def gdp_ipd(startdate="1955-01-01", enddate="2021-01-01"):
    """
    Full Name: Long-Term Government Bond Yields: 10-year: Main (Including Benchmark) for the United States
    Description: Percent,Not Seasonally Adjusted, Monthly, Quarterly and Annually
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "USAGDPDEFQISMEI",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(
        df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "USAGDPDEFAISMEI",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(
        df_annually["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(
        df_quarterly,
        df_annually,
        on="DATE",
        direction="backward")
    df.columns = ["Date", "gdp_ipd_Quarterly", "gdp_ipd_Annually"]
    return df


def cci(startdate="1955-01-01", enddate="2021-01-01"):
    """
    Full Name: Consumer Opinion Surveys: Confidence Indicators: Composite Indicators: OECD Indicator for the United States
    Description: Normalised (Normal=100), Seasonally Adjusted, Monthly
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "CSCICP03USM665S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df.columns = ["Date", "CCI_Monthly"]
    df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d")
    return df


def bci(startdate="1955-01-01", enddate="2021-01-01"):
    """
    Full Name: Business confidence index OECD Indicator for the United States
    Description: Normalised (Normal=100), Seasonally Adjusted, Monthly
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "BSCICP03USM665S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df.columns = ["Date", "BCI_Annually"]
    df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d")
    return df


def ibr_3(startdate="1965-01-01", enddate="2021-01-01"):
    """
    Full Name: 3-Month or 90-day Rates and Yields: Interbank Rates for the United States
    Description: Percent, Not Seasonally Adjusted, Monthly and Quarterly
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "IR3TIB01USM156N",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "IR3TIB01USQ156N",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(
        df_quarterly["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(
        df_quarterly,
        df_quarterly,
        on="DATE",
        direction="backward")
    df.columns = ["Date", "ibr3_Monthly", "ibr3_Quarterly"]


def gfcf_3(startdate="1965-01-01", enddate="2021-01-01"):
    """
    Full Name: Gross Fixed Capital Formation in United States
    Description: United States Dollars,Not Seasonally Adjusted, Quarterly and Annually
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "USAGFCFQDSMEI",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(
        df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "USAGFCFADSMEI",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(
        df_annually["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(
        df_quarterly,
        df_quarterly,
        on="DATE",
        direction="backward")
    df.columns = ["Date", "ibr3_Monthly", "ibr3_Annually"]
    return df


def pfce(startdate="1955-01-01", enddate="2021-01-01"):
    """
    Full Name: Private Final Consumption Expenditure in United States
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "USAPFCEQDSMEI",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(
        df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "USAPFCEADSMEI",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(
        df_annually["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(
        df_quarterly,
        df_annually,
        on="DATE",
        direction="backward")
    df.columns = ["Date", "PFCE_Quarterly", "PFCE_Annually"]
    return df


def tlp(startdate="1955-01-01", enddate="2021-01-01"):
    """
    Full Name: Early Estimate of Quarterly ULC Indicators: Total Labor Productivity for the United States
    Description: Growth Rate Previous Period,Seasonally Adjusted, Quarterly and YoY
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "ULQELP01USQ657S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_quarterly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_quarterly["DATE"] = pd.to_datetime(
        df_quarterly["DATE"], format="%Y-%m-%d")
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "ULQELP01USQ659S",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(
        df_annually["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(
        df_quarterly,
        df_annually,
        on="DATE",
        direction="backward")
    df.columns = ["Date", "PFCE_Quarterly", "PFCE_Quarterly_YoY"]
    return df


def rt(startdate="1955-01-01", enddate="2021-01-01"):
    """
    Full Name:Total Retail Trade in United States
    Description: Monthly and Anually
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "USASARTMISMEI",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_monthly = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_monthly["DATE"] = pd.to_datetime(df_monthly["DATE"], format="%Y-%m-%d")
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "USASARTAISMEI",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_annually = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_annually["DATE"] = pd.to_datetime(
        df_annually["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(
        df_monthly,
        df_annually,
        on="DATE",
        direction="backward")
    df.columns = ["Date", "RT_Quarterly", "RT_Annually"]
    return df


def bir(startdate="2003-01-01", enddate="2021-01-01"):
    """
    Full Name:Total Retail Trade in United States
    Description: Monthly and Anually
    Return: pd.DataFrame
    """
    tmp_url = url["fred_econ"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "T5YIE",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_5y = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_5y["DATE"] = pd.to_datetime(df_5y["DATE"], format="%Y-%m-%d")
    request_header = {"User-Agent": ua.random}
    request_params = {
        "id": "T10YIE",
        "cosd": "{}".format(startdate),
        "coed": "{}".format(enddate)
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.content
    df_10y = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df_10y["DATE"] = pd.to_datetime(df_10y["DATE"], format="%Y-%m-%d")
    df = pd.merge_asof(df_5y, df_10y, on="DATE", direction="backward")
    df.columns = ["Date", "BIR_5y", "BIR_10y"]
    return df


def adsbci():
    """
    An index designed to track real business conditions at high observation frequency
    """
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["philfed"] + "ads"
    r = requests.get(tmp_url, headers=request_header)
    file = open("ads_temp.xls", "wb")
    file.write(r.content)
    file.close()
    df = pd.read_excel("ads_temp.xls")
    df.columns = ["Date", "ADS_Index"]
    df['Date'] = pd.to_datetime(df["Date"], format="%Y:%m:%d")
    os.remove("ads_temp.xls")
    return df


def pci():
    """
    Tracks the degree of political disagreement among U.S. politicians at the federal level, Monthly
    """
    df = pd.read_excel(
        "https://www.philadelphiafed.org/-/media/frbp/assets/data-visualizations/partisan-conflict.xlsx")
    df["Date"] = df["Year"].astype(str) + df["Month"]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y%B")
    df = df.drop(["Year", "Month"], axis=1)
    df = df[["Date", "Partisan Conflict"]]
    return df


def inflation_nowcasting():
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = "https://www.clevelandfed.org/~/media/files/charting/%20nowcast_quarter.json"

    r = requests.get(tmp_url, headers=request_header)
    tmp_df = pd.DataFrame(demjson.decode(r.text))
    df = pd.DataFrame()
    for i in range(0, len(tmp_df)):
        date = tmp_df['chart'][i]['subcaption'][:4] + "/" + \
            pd.DataFrame(tmp_df["dataset"][i][0]['data'])['tooltext'].str.extract(r"\b(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])\b")[0] + "/" + \
            pd.DataFrame(tmp_df["dataset"][i][0]['data'])['tooltext'].str.extract(r"\b(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])\b")[1]
        CPI_I = pd.DataFrame(
            (pd.DataFrame(tmp_df["dataset"][i])['data'])[0])["value"]
        C_CPI_I = pd.DataFrame(
            (pd.DataFrame(tmp_df["dataset"][i])['data'])[1])["value"]
        PCE_I = pd.DataFrame(
            (pd.DataFrame(tmp_df["dataset"][i])['data'])[2])["value"]
        C_PCE_I = pd.DataFrame(
            (pd.DataFrame(tmp_df["dataset"][i])['data'])[3])["value"]
        A_CPI_I = pd.DataFrame(
            (pd.DataFrame(tmp_df["dataset"][i])['data'])[4])["value"]
        A_C_CPI_I = pd.DataFrame(
            (pd.DataFrame(tmp_df["dataset"][i])['data'])[5])["value"]
        A_PCE_I = pd.DataFrame(
            (pd.DataFrame(tmp_df["dataset"][i])['data'])[6])["value"]
        A_C_PCE_I = pd.DataFrame(
            (pd.DataFrame(tmp_df["dataset"][i])['data'])[7])["value"]
        tmp_df2 = pd.DataFrame({"Date": date,
                                "CPI_I": CPI_I,
                                "C_CPI_I": C_CPI_I,
                                "PCE_I": PCE_I,
                                "C_PCE_I": C_PCE_I,
                                "A_CPI_I": A_CPI_I,
                                "A_C_CPI_I": A_C_CPI_I,
                                "A_PCE_I": A_PCE_I,
                                "A_C_PCE_I": A_C_PCE_I})
        df = pd.concat([df, tmp_df2], axis=0)
        df.reset_index(drop=True, inplace=True)

    df.replace('', np.nan, inplace=True)
    return df


def bbki():
    tmp_url = url["chicagofed"] + "bbki/bbki-monthly-data-series-csv.csv"
    df = pd.read_csv(tmp_url)
    df["Date"] = date_transform(df["Date"], "%m/%d/%Y", "%Y-%m-%d")
    df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d")
    return df


def cfnai():
    tmp_url = url["chicagofed"] + "cfnai/cfnai-data-series-csv.csv"
    df = pd.read_csv(tmp_url)
    df["Date"] = date_transform(df["Date"], "%Y/%m", "%Y-%m-%d")
    df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d")
    return df


def cfsbc():
    tmp_url = url["chicagofed"] + "cfsbc/cfsbc-data-xlsx.xlsx"
    df = pd.read_excel(tmp_url)
    df["Date"] = date_transform(df["Date"], "%Y-%m", "%Y-%m-%d")
    df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d")
    return df


def nfci():
    tmp_url = url["chicagofed"] + "nfci/decomposition-nfci-csv.csv"
    df = pd.read_csv(tmp_url)
    df.columns = ["Date", "NFCI", "Risk", "Credit", "Leverage"]
    df["Date"] = date_transform(df["Date"], "%Y/%m/%d", "%Y-%m-%d")
    df["Date"] = pd.to_datetime(df["Date"], format = "%Y-%m-%d")
    return df

def Leading_Indicators_OECD(startdate = "1950-01", enddate = "2021-05"):
    # CLI
    tmp_url = url["OECD"] + "USA.CLI.AMPLITUD.LTRENDIDX.M/OECD"
    ua = UserAgent(verify_ssl=False)
    request_params = {
        "contentType": "csv",
        "detail": "code",
        "separator": "comma",
        "csv-lang": "en",
        "startPeriod": "{}".format(startdate),
        "endPeriod": "{}".format(enddate)
    }
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, params = request_params, headers=request_header)
    data_text = r.content
    df_cli = pd.read_csv(io.StringIO(data_text.decode('utf-8')))[["TIME", "Value"]]
    df_cli.columns = ["Date", "US_OECD_CLI"]
    df_cli["Date"] = pd.to_datetime(df_cli["Date"], format = "%Y-%m")
    df_cli["US_OECD_CLI"] = df_cli["US_OECD_CLI"].astype(float)
    #BCI
    tmp_url = url["OECD"] + "USA.BCI.AMPLITUD.LTRENDIDX.M/OECD"
    ua = UserAgent(verify_ssl=False)
    request_params = {
        "contentType": "csv",
        "detail": "code",
        "separator": "comma",
        "csv-lang": "en",
        "startPeriod": "{}".format(startdate),
        "endPeriod": "{}".format(enddate)
    }
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, params = request_params, headers=request_header)
    data_text = r.content
    df_bci = pd.read_csv(io.StringIO(data_text.decode('utf-8')))[["TIME", "Value"]]
    df_bci.columns = ["Date", "US_OECD_BCI"]
    df_bci["Date"] = pd.to_datetime(df_bci["Date"], format = "%Y-%m")
    df_bci["US_OECD_BCI"] = df_bci["US_OECD_BCI"].astype(float)
    # CCI
    tmp_url = url["OECD"] + "USA.CCI.AMPLITUD.LTRENDIDX.M/OECD"
    ua = UserAgent(verify_ssl=False)
    request_params = {
        "contentType": "csv",
        "detail": "code",
        "separator": "comma",
        "csv-lang": "en",
        "startPeriod": "{}".format(startdate),
        "endPeriod": "{}".format(enddate)
    }
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, params = request_params, headers=request_header)
    data_text = r.content
    df_cci = pd.read_csv(io.StringIO(data_text.decode('utf-8')))[["TIME", "Value"]]
    df_cci.columns = ["Date", "US_OECD_CCI"]
    df_cci["Date"] = pd.to_datetime(df_cci["Date"], format = "%Y-%m")
    df_cci["US_OECD_CCI"] = df_cci["US_OECD_CCI"].astype(float)
    df = pd.merge_asof(df_cli, df_bci, on = "Date")
    df = pd.merge_asof(df, df_cci, on = "Date")
    
    return df
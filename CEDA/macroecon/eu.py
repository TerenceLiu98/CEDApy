import io
import os
import demjson
import requests
import numpy as np
import pandas as pd
from fake_useragent import UserAgent
from pandas.core.frame import DataFrame
from pandas.core.reshape.merge import merge

# Main Economic Indicators: https://alfred.stlouisfed.org/release?rid=205
url = {
    "fred_econ": "https://fred.stlouisfed.org/graph/fredgraph.csv?",
    "eurostat": "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/",
    "ecb": "https://sdw-wsrest.ecb.europa.eu/service/data/"
}


def merge_data(data_1: pd.DataFrame, data_2: pd.DataFrame, col_name: str):
    data = pd.merge_asof(data_1, data_2, on=col_name)
    return data


def National_Account():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=NAEXCP04EZQ189S,NAEXCP02EZQ189S,NAEXCP01EZQ189S,NAEXCP06EZQ189S,NAEXCP07EZQ189S,NAEXCP03EZQ189S,NAGIGP01EZQ661S,NAEXKP06EZQ659S,NAEXKP04EZQ659S,NAEXKP01EZQ652S,NAEXKP07EZQ652S,NAEXKP03EZQ659S&scale=left,left,left,left,left,left,left,left,left,left,left,left&cosd=1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1996-01-01,1996-01-01,1995-01-01,1995-01-01,1996-01-01&coed=2020-10-01,2020-10-01,2020-10-01,2020-10-01,2020-10-01,2020-10-01,2020-10-01,2020-10-01,2020-10-01,2021-01-01,2020-10-01,2020-10-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c,%23b5ca92,%2391e8e1,%238d4653,%238085e8&link_values=false,false,false,false,false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a,a,a,a,a&fq=Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly&fam=avg,avg,avg,avg,avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8,9,10,11,12&transformation=lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1996-01-01,1996-01-01,1995-01-01,1995-01-01,1996-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'NAEXCP04EZQ189S': "Gross Domestic Product by Expenditure in Current Prices: Gross Fixed Capital Formation for the Euro Area",
        'NAEXCP02EZQ189S': "Gross Domestic Product by Expenditure in Current Prices: Private Final Consumption Expenditure for the Euro Area",
        'NAEXCP01EZQ189S': "Gross Domestic Product by Expenditure in Current Prices: Total Gross Domestic Product for the Euro Area",
        'NAEXCP06EZQ189S': "Gross Domestic Product by Expenditure in Current Prices: Exports of Goods and Services for the Euro Area",
        'NAEXCP07EZQ189S': "Gross Domestic Product by Expenditure in Current Prices: Less Imports of Goods and Services for the Euro Area",
        'NAEXCP03EZQ189S': "Gross Domestic Product by Expenditure in Current Prices: Government Final Consumption Expenditure for the Euro Area",
        'NAGIGP01EZQ661S': "Gross Domestic Product Deflator for the Euro Area",
        'NAEXKP06EZQ659S': "Gross Domestic Product by Expenditure in Constant Prices: Exports of Goods and Services for the Euro Area",
        'NAEXKP04EZQ659S': "Gross Domestic Product by Expenditure in Constant Prices: Gross Fixed Capital Formation for the Euro Area",
        'NAEXKP01EZQ652S': "Gross Domestic Product by Expenditure in Constant Prices: Total Gross Domestic Product for the Euro Area",
        'NAEXKP07EZQ652S': "Gross Domestic Product by Expenditure in Constant Prices: Less: Imports of Goods and Services for the Euro Area",
        'NAEXKP03EZQ659S': "Gross Domestic Product by Expenditure in Constant Prices: Government Final Consumption Expenditure for the Euro Area"}
    description = "National Accounts, Quarterly, Seasonally, Adjusted"
    return df, name_list, description


def International_Trade():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=XTEXVA01EZQ188S,XTIMVA01EZQ188S,EA19XTNTVA01STSAQ&scale=left,left,left&cosd=1995-01-01,1995-01-01,1995-01-01&coed=2020-10-01,2020-10-01,2017-04-01&line_color=%234572a7,%23aa4643,%2389a54e&link_values=false,false,false&line_style=solid,solid,solid&mark_type=none,none,none&mw=3,3,3&lw=2,2,2&ost=-99999,-99999,-99999&oet=99999,99999,99999&mma=0,0,0&fml=a,a,a&fq=Quarterly,Quarterly,Quarterly&fam=avg,avg,avg&fgst=lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2017-04-01&line_index=1,2,3&transformation=lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07&nd=1995-01-01,1995-01-01,1995-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'XTEXVA01EZQ188S': "Exports: Value Goods for the Euro Area",
        'XTIMVA01EZQ188SS': "Imports: Value Goods for the Euro Area",
        'EA19XTNTVA01STSAQ': "International Trade: Net trade: Value (goods): Total for the Euro Area"}
    description = "International Trade, Quarterly, Seasonally Adjusted"
    return df, name_list, description


def Balance_of_Payments_BPM6():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EA19B6BLTT02STSAQ,EA19B6DBSE02STSAQ,EA19B6DBSE03STSAQ,EA19B6CRSE03STSAQ,EA19B6CRSE02STSAQ&scale=left,left,left,left,left&cosd=1999-01-01,1999-01-01,1999-01-01,1999-01-01,1999-01-01&coed=2020-10-01,2020-10-01,2020-10-01,2020-10-01,2020-10-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae&link_values=false,false,false,false,false&line_style=solid,solid,solid,solid,solid&mark_type=none,none,none,none,none&mw=3,3,3,3,3&lw=2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999&mma=0,0,0,0,0&fml=a,a,a,a,a&fq=Quarterly,Quarterly,Quarterly,Quarterly,Quarterly&fam=avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5&transformation=lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1999-01-01,1999-01-01,1999-01-01,1999-01-01,1999-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'EA19B6BLTT02STSAQ': "Balance of payments BPM6: Current account Debits: Services: Total Debits as % of Current account for the Euro Area",
        'EA19B6DBSE02STSAQ': "Balance of payments BPM6: Current account Debits: Services: Total Debits as % of Current account for the Euro Area",
        'EA19B6DBSE03STSAQ': "Balance of payments BPM6: Current account Debits: Services: Total Debits as % of Goods and Services for the Euro Area",
        'EA19B6CRSE03STSAQ': "Balance of payments BPM6: Current account Credits: Services: Total Credits as % of Goods and Services for Euro Area",
        'EA19B6CRSE02STSAQ': "Balance of payments BPM6: Current account Credits: Services: Total Credits as % of Current account for Euro Area"}
    description = "Balanced of payments BPM6, Quarterly, Seasonally Adjusted"
    return df, name_list, description


def Learning_Indicators_OECD():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EA19LORSGPNOSTSAM,EA19LOLITOTRGYSAM,EA19LOLITONOSTSAM,EA19LOLITOAASTSAM,EA19LORSGPORIXOBSAM,EA19LORSGPRTSTSAM,EA19LORSGPTDSTSAM&scale=left,left,left,left,left,left,left&cosd=1960-03-01,1966-12-01,1965-12-01,1965-12-01,1960-03-01,1960-03-01,1960-03-01&coed=2020-11-01,2020-11-01,2021-03-01,2021-03-01,2020-11-01,2020-11-01,2020-11-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd&link_values=false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7&transformation=lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1960-03-01,1966-12-01,1965-12-01,1965-12-01,1960-03-01,1960-03-01,1960-03-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'EA19CPALTT01GYQ': "Leading Indicators OECD: Reference series: Gross Domestic Product (GDP): Normalised for the Euro Area",
        'EA19LOLITOTRGYSAM': "Leading Indicators OECD: Leading indicators: CLI: Trend restored for the Euro Area",
        'EA19LOLITONOSTSAM': "Leading Indicators OECD: Leading indicators: CLI: Normalised for the Euro Area",
        'EA19LOLITOAASTSAM': "Leading Indicators OECD: Leading indicators: CLI: Amplitude adjusted for the Euro Area",
        'EA19LORSGPORIXOBSAM': "Leading Indicators OECD: Reference series: Gross Domestic Product (GDP): Original series for the Euro Area",
        'EA19LORSGPRTSTSAM': "Leading Indicators OECD: Reference series: Gross Domestic Product (GDP): Ratio to trend for the Euro Area",
        'EA19LORSGPTDSTSAM': "Leading Indicators OECD: Reference series: Gross Domestic Product (GDP): Trend for the Euro Area"}
    description = "Leading Indicators OECD, Monthly, Seasonally Adjusted"
    return df, name_list, description


def Monetary_Aggregates_Monthly_Adj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EA19MABMM301GYSAM,EA19MANMM101IXOBSAM&scale=left,left&cosd=1971-01-01,1970-01-01&coed=2021-03-01,2021-03-01&line_color=%234572a7,%23aa4643&link_values=false,false&line_style=solid,solid&mark_type=none,none&mw=3,3&lw=2,2&ost=-99999,-99999&oet=99999,99999&mma=0,0&fml=a,a&fq=Monthly,Monthly&fam=avg,avg&fgst=lin,lin&fgsnd=2020-02-01,2020-02-01&line_index=1,2&transformation=lin,lin&vintage_date=2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07&nd=1971-01-01,1970-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {'EA19MABMM301GYSAM': "Monetary aggregates and their components: Broad money and components: M3: M3 for the Euro Area",
                 'EA19MANMM101IXOBSAM': "Monetary aggregates and their components: Narrow money and components: M1 and components: M1 for the Euro Area"}
    description = "Monetary aggregates and their components, Monthly, Seasonally Adjusted"
    return df, name_list, description


def Monetary_Aggregates_Quarterly_Adj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=MABMM301EZQ189S,MANMM101EZQ189S&scale=left,left&cosd=1970-01-01,1970-01-01&coed=2021-01-01,2021-01-01&line_color=%234572a7,%23aa4643&link_values=false,false&line_style=solid,solid&mark_type=none,none&mw=3,3&lw=2,2&ost=-99999,-99999&oet=99999,99999&mma=0,0&fml=a,a&fq=Quarterly,Quarterly&fam=avg,avg&fgst=lin,lin&fgsnd=2020-02-01,2020-02-01&line_index=1,2&transformation=lin,lin&vintage_date=2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07&nd=1970-01-01,1970-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'MABMM301EZQ189S': "M3 for the Euro Area",
        'MANMM101EZQ189S': "M1 for the Euro Area"
    }
    description = "Monetary aggregates and their components, Quarterly, Seasonally Adjusted"
    return df, name_list, description


def Currency_Conversion_Quarterly():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CCEUSP02EZQ655N,CCUSMA02EZQ618N,CCUSSP01EZQ650N,CCRETT02EZQ661N,CCRETT01EZQ661N&scale=left,left,left,left,left&cosd=1999-01-01,1979-01-01,1999-01-01,1970-01-01,1970-01-01&coed=2021-01-01,2021-01-01,2021-01-01,2021-01-01,2021-01-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae&link_values=false,false,false,false,false&line_style=solid,solid,solid,solid,solid&mark_type=none,none,none,none,none&mw=3,3,3,3,3&lw=2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999&mma=0,0,0,0,0&fml=a,a,a,a,a&fq=Quarterly,Quarterly,Quarterly,Quarterly,Quarterly&fam=avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5&transformation=lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1999-01-01,1979-01-01,1999-01-01,1970-01-01,1970-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'CCEUSP02EZQ655N': "National Currency to Euro Spot Exchange Rate for the Euro Area",
        'CCUSMA02EZQ618N': "National Currency to US Dollar Exchange Rate: Average of Daily Rates for the Euro Area",
        'CCUSSP01EZQ650N': "US Dollar to National Currency Spot Exchange Rate for the Euro Area",
        'CCRETT02EZQ661N': "Real Effective Exchange Rates Based on Manufacturing Unit Labor Cost for the Euro Area",
        'CCRETT01EZQ661N': "Real Effective Exchange Rates Based on Manufacturing Consumer Price Index for the Euro Area"}
    description = "Currency Conversions, Quarterly, Not Seasonally Adjusted"
    return df, name_list, description


def Currency_Conversion_Monthly():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CCRETT01EZM661N,CCUSMA02EZM659N,CCUSSP01EZM650N,CCEUSP02EZM655N&scale=left,left,left,left&cosd=1970-01-01,1991-01-01,1999-01-01,1999-01-01&coed=2021-04-01,2021-04-01,2021-03-01,2021-03-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b&link_values=false,false,false,false&line_style=solid,solid,solid,solid&mark_type=none,none,none,none&mw=3,3,3,3&lw=2,2,2,2&ost=-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999&mma=0,0,0,0&fml=a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg&fgst=lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4&transformation=lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1970-01-01,1991-01-01,1999-01-01,1999-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'CCRETT01EZM661N': "Real Effective Exchange Rates Based on Manufacturing Consumer Price Index for the Euro Area",
        'CCUSMA02EZM659N': "National Currency to US Dollar Exchange Rate: Average of Daily Rates for the Euro Area",
        'CCUSSP01EZM650N': "US Dollar to National Currency Spot Exchange Rate for the Euro Area",
        'CCEUSP02EZM655N': "National Currency to Euro Spot Exchange Rate for the Euro Area"}
    description = "Currency Conversions, Monthly, Not Seasonally Adjusted"
    return df, name_list, description


def Interest_Rates_Quarterly():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=IRLTLT01EZQ156N,IR3TIB01EZQ156N,IRSTCI01EZQ156N&scale=left,left,left&cosd=1970-01-01,1994-01-01,1994-01-01&coed=2021-01-01,2021-01-01,2021-01-01&line_color=%234572a7,%23aa4643,%2389a54e&link_values=false,false,false&line_style=solid,solid,solid&mark_type=none,none,none&mw=3,3,3&lw=2,2,2&ost=-99999,-99999,-99999&oet=99999,99999,99999&mma=0,0,0&fml=a,a,a&fq=Quarterly,Quarterly,Quarterly&fam=avg,avg,avg&fgst=lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3&transformation=lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07&nd=1970-01-01,1994-01-01,1994-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'IRLTLT01EZQ156N': "Long-Term Government Bond Yields: 10-year: Main (Including Benchmark) for the Euro Area",
        'IR3TIB01EZQ156N': "3-Month or 90-day Rates and Yields: Interbank Rates for the Euro Area",
        'IRSTCI01EZQ156N': "Immediate Rates: Less than 24 Hours: Call Money/Interbank Rate for the Euro Area"}
    description = "Interest Rates, Quarterly, Not Seasonally Adjusted"
    return df, name_list, description


def Interest_Rates_Monthly():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=IRLTLT01EZM156N,IR3TIB01EZM156N,IRSTCI01EZM156N&scale=left,left,left&cosd=1970-01-01,1994-01-01,1994-01-01&coed=2021-04-01,2021-04-01,2021-04-01&line_color=%234572a7,%23aa4643,%2389a54e&link_values=false,false,false&line_style=solid,solid,solid&mark_type=none,none,none&mw=3,3,3&lw=2,2,2&ost=-99999,-99999,-99999&oet=99999,99999,99999&mma=0,0,0&fml=a,a,a&fq=Monthly,Monthly,Monthly&fam=avg,avg,avg&fgst=lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3&transformation=lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07&nd=1970-01-01,1994-01-01,1994-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'IRLTLT01EZM156N': "Long-Term Government Bond Yields: 10-year: Main (Including Benchmark) for the Euro Area",
        'IR3TIB01EZM156N': "3-Month or 90-day Rates and Yields: Interbank Rates for the Euro Area",
        'IRSTCI01EZM156N': "Immediate Rates: Less than 24 Hours: Call Money/Interbank Rate for the Euro Area"}
    description = "Interest Rates, Monthly, Not Seasonally Adjusted"
    return df, name_list, description


def Share_Prices_Quarterly():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=SPASTT01EZQ661N&scale=left&cosd=1987-01-01&coed=2021-01-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2021-06-07&revision_date=2021-06-07&nd=1987-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'SPASTT01EZQ661N': "Total Share Prices for All Shares for the Euro Area"}
    description = "Share Prices, Quarterly, Not Seasonally Adjusted"
    return df, name_list, description


def Share_Prices_Monthly():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=SPASTT01EZM661N&scale=left&cosd=1986-12-01&coed=2021-04-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2021-06-07&revision_date=2021-06-07&nd=1986-12-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'SPASTT01EZM661N': "Total Share Prices for All Shares for the Euro Area"}
    description = "Share Prices, Monthly, Not Seasonally Adjusted"
    return df, name_list, description


def CPI_Monthly(startdate="1970-01-01", enddate="2021-01-01"):
    """
    """
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CPHPTT01EZM661N,EA19CPHP0401IXOBM,EA19CPHP0403IXOBM,EA19CPHP0404IXOBM,EA19CPHP0405IXOBM,EA19CPHP0500IXOBM,EA19CPHP0600IXOBM,EA19CPHP0700IXOBM,EA19CPHP0702IXOBM,EA19CPHP0800IXOBM,EA19CPHP0900IXOBM,CPHPEN01EZM661N&scale=left,left,left,left,left,left,left,left,left,left,left,left&cosd=1990-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01&coed=2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c,%23b5ca92,%2391e8e1,%238d4653,%238085e8&link_values=false,false,false,false,false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8,9,10,11,12&transformation=lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1990-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01,1996-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        "CPHPTT01EZM661N": "CPI:Harmonized Prices: Total All Items for the Euro Area",
        "EA19CPHP0401IXOBM": "CPI:Harmonised_Price:Housing, water, electricity, gas and other fuels (COICOP 04): Actual rentals for housing for the Euro Area",
        "EA19CPHP0403IXOBM": "CPI:Harmonised_Price:Housing, water, electricity, gas and other fuels (COICOP 04): Maintenance & repairs of the dwellings for the Euro Area",
        "EA19CPHP0404IXOBM": "CPI:Harmonised_Price:Housing, water, electricity, gas and other fuels (COICOP 04): Water supply and miscellaneous services relating to the dwelling for the Euro Area",
        "EA19CPHP0405IXOBM": "CPI:Harmonised_Price:Housing, water, electricity, gas and other fuels (COICOP 04): Electricity, gas and other fuels for the Euro Area",
        "EA19CPHP0500IXOBM": "CPI:Harmonised_Price:Furnishings, household equip. and routine household maintenance (COICOP 05): Total for the Euro Area ",
        "EA19CPHP0600IXOBM": "CPI:Harmonised_Price:Health (COICOP 06): Total for the Euro Area",
        "EA19CPHP0700IXOBM": "CPI:Harmonised_Price:Transport (COICOP 07): Total for the Euro Area",
        "EA19CPHP0702IXOBM": "CPI:Harmonised_Price:Transport (COICOP 07): Fuels and lubricants for personal transport equipment for the Euro Area",
        "EA19CPHP0800IXOBM": "CPI:Harmonised_Price:Communication (COICOP 08): Total for the Euro Area",
        "EA19CPHP0900IXOBM": "CPI:Harmonised_Price:Recreation and culture (COICOP 09): Total for the Euro Area",
        "CPHPEN01EZM661N": "CPI:Harmonized Prices: Total Energy for the Euro Area"}
    description = "Consumer Price Index, Monthly, Not Seasonally Adjusted"
    return df, name_list, description


def CPI_Quarterly():
    """
    """
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EA19CPALTT01GYQ,EA19CPGRLE01GYQ,EA19CPGREN01GYQ,EA19CPHP0401IXOBQ&scale=left,left,left,left&cosd=1991-01-01,1997-01-01,1997-01-01,1996-01-01&coed=2021-01-01,2021-01-01,2021-01-01,2021-01-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b&link_values=false,false,false,false&line_style=solid,solid,solid,solid&mark_type=none,none,none,none&mw=3,3,3,3&lw=2,2,2,2&ost=-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999&mma=0,0,0,0&fml=a,a,a,a&fq=Quarterly,Quarterly,Quarterly,Quarterly&fam=avg,avg,avg,avg&fgst=lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4&transformation=lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1991-01-01,1997-01-01,1997-01-01,1996-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'EA19CPALTT01GYQ': "CPI:All items:Total:Total for the Euro Area",
        'EA19CPGRLE01GYQ': "CPI:OECD Groups:All items non-food non-energy:Total for the Euro Area",
        'EA19CPGREN01GYQ': "CPI:OECD Groups:Energy (Fuel, electricity & gasoline):Total for the Euro Area",
        'EA19CPHP0401IXOBQ': "CPI:Harmonised prices:Housing, water, electricity, gas and other fuels (COICOP 04):Actual rentals for housing for the Euro Area"}
    description = "Consumer Price Index, Quarterly, Not Seasonally Adjusted"
    return df, name_list, description


def PPI_Monthly():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PIEAMP02EZM659N,PIEAMP01EZM661N,PIEATI01EZM661N,PIEATI02EZM661N,PITGND02EZM661N,PITGND01EZM661N,PITGIG01EZM661N,PITGIG02EZM661N,PIEAFD02EZM661N,PITGCG02EZM661N,PITGCG01EZM661N,PITGCD01EZM661N&scale=left,left,left,left,left,left,left,left,left,left,left,left&cosd=1996-01-01,2000-01-01,2000-01-01,2000-01-01,1995-01-01,2000-01-01,2000-01-01,1995-01-01,1995-01-01,1995-01-01,2000-01-01,2000-01-01&coed=2021-03-01,2021-02-01,2021-02-01,2021-03-01,2021-03-01,2021-02-01,2021-02-01,2021-03-01,2021-03-01,2021-03-01,2021-02-01,2021-02-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c,%23b5ca92,%2391e8e1,%238d4653,%238085e8&link_values=false,false,false,false,false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8,9,10,11,12&transformation=lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1996-01-01,2000-01-01,2000-01-01,2000-01-01,1995-01-01,2000-01-01,2000-01-01,1995-01-01,1995-01-01,1995-01-01,2000-01-01,2000-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'PIEAMP02EZM659N': "Producer Prices Index: Economic Activities: Domestic Manufacturing for the Euro Area",
        "PIEAMP01EZM661N": "Producer Prices Index: Economic Activities: Total Manufacturing for the Euro Area",
        "PIEATI01EZM661N": "Producer Prices Index: Economic Activities: Total Industrial Activities for the Euro Area",
        "PIEATI02EZM661N": "Producer Prices Index: Economic Activities: Domestic Industrial Activities for the Euro Area",
        "PITGND02EZM661N": "Producer Prices Index: Domestic Nondurable Consumer Goods for the Euro Area",
        "PITGND01EZM661N": "Producer Prices Index: Total Nondurable Consumer Goods for the Euro Area",
        "PITGIG01EZM661N": "Producer Prices Index: Total Intermediate Goods for the Euro Area",
        "PITGIG02EZM661N": "Producer Prices Index: Domestic Intermediate Goods for the Euro Area",
        "PIEAFD02EZM661N": "Producer Prices Index: Economic Activities: Domestic Manufacture of Food Products for the Euro Area",
        "PITGCG02EZM661N": "Producer Prices Index: Domestic Consumer Goods for the Euro Area",
        "PITGCG01EZM661N": "Producer Prices Index: Total Consumer Goods for the Euro Area",
        "PITGCD01EZM661N": "Producer Prices Index: Total Durable Consumer Goods for the Euro Area"}
    description = "Producer Prices Index, Monthly, Not Seasonally Adjusted"
    return df, name_list, description


def PPI_Quarterly():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PIEAFD01EZQ661N,PIEAEN02EZQ661N,PIEAEN01EZQ661N,PITGND02EZQ661N,PITGND01EZQ661N,PITGIG01EZQ661N,PITGIG02EZQ661N,PIEAFD02EZQ661N,PITGCD02EZQ661N,PITGCD01EZQ661N,PITGVG01EZQ661N,PITGVG02EZQ661N&scale=left,left,left,left,left,left,left,left,left,left,left,left&cosd=2000-01-01,2000-01-01,2000-01-01,1995-01-01,2000-01-01,2000-01-01,1995-01-01,1995-01-01,2000-01-01,2000-01-01,2000-01-01,1995-01-01&coed=2020-10-01,2021-01-01,2020-10-01,2021-01-01,2020-10-01,2020-10-01,2021-01-01,2021-01-01,2021-01-01,2020-10-01,2020-10-01,2021-01-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c,%23b5ca92,%2391e8e1,%238d4653,%238085e8&link_values=false,false,false,false,false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a,a,a,a,a&fq=Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly&fam=avg,avg,avg,avg,avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8,9,10,11,12&transformation=lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=2000-01-01,2000-01-01,2000-01-01,1995-01-01,2000-01-01,2000-01-01,1995-01-01,1995-01-01,2000-01-01,2000-01-01,2000-01-01,1995-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'PIEAFD01EZQ661N': "Producer Prices Index: Economic Activities: Total Manufacture of Food Products for the Euro Area",
        "PIEAEN02EZQ661N": "Producer Prices Index: Economic Activities: Domestic Energy for the Euro Area",
        "PIEAEN01EZQ661N": "Producer Prices Index: Economic Activities: Total Energy for the Euro Area",
        "PITGND02EZQ661N": "Producer Prices Index: Domestic Nondurable Consumer Goods for the Euro Area",
        "PITGND01EZQ661N": "Producer Prices Index: Total Nondurable Consumer Goods for the Euro Area",
        "PITGIG01EZQ661N": "Producer Prices Index: Total Intermediate Goods for the Euro Area",
        "PITGIG02EZQ661N": "Producer Prices Index: Domestic Intermediate Goods for the Euro Area",
        "PIEAFD02EZQ661N": "Producer Prices Index: Economic Activities: Domestic Manufacture of Food Products for the Euro Area",
        "PITGCD02EZQ661N": "Producer Prices Index: Domestic Durable Consumer Goods for the Euro Area",
        "PITGCD01EZQ661N": "Producer Prices Index: Total Durable Consumer Goods for the Euro Area",
        "PITGVG01EZQ661N": "Producer Prices Index: Investments Goods: Total for the Euro Area",
        "PITGVG02EZQ661N": "Producer Prices Index: Domestic Investments Goods for the Euro Area"}
    description = "Producer Prices Index, Quarterly, Not Seasonally Adjusted"
    return df, name_list, description


def Business_Tendency_Surveys_Construction():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EA19BCBUTE02STSAM,BCOBLV02EZM460S,BCEMFT02EZM460S,BCCICP02EZM460S,BCSPFT02EZM460S&scale=left,left,left,left,left&cosd=1985-01-01,1985-01-01,1985-01-01,1985-01-01,1985-01-01&coed=2021-04-01,2021-04-01,2021-04-01,2021-04-01,2021-04-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae&link_values=false,false,false,false,false&line_style=solid,solid,solid,solid,solid&mark_type=none,none,none,none,none&mw=3,3,3,3,3&lw=2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999&mma=0,0,0,0,0&fml=a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5&transformation=lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1985-01-01,1985-01-01,1985-01-01,1985-01-01,1985-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'EA19BCBUTE02STSAM': "Business tendency surveys (construction): Business situation - Activity: Tendency: National indicator for the Euro Area",
        'BCOBLV02EZM460S': "Business Tendency Surveys for Construction: Order Books: Level: European Commission Indicator for the Euro Area",
        'BCEMFT02EZM460S': "Business Tendency Surveys for Construction: Employment: Future Tendency: European Commission and National Indicators for the Euro Area",
        'BCCICP02EZM460S': "Business Tendency Surveys for Construction: Confidence Indicators: Composite Indicators: European Commission and National Indicators for the Euro Area",
        'BCSPFT02EZM460S': "Business Tendency Surveys for Construction: Selling Prices: Future Tendency: European Commission Indicator for the Euro Area"}
    description = "Business tendency surveys (construction), Monthly, Seasonally Adjusted"
    return df, name_list, description


def Business_Tendency_Surveys_Services():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EA19BVBUTE02STSAM,BVCICP02EZM460S,BVEMTE02EZM460S,BVEMFT02EZM460S,BVDEFT02EZM460S,BVDETE02EZM460S&scale=left,left,left,left,left,left&cosd=1995-04-01,1995-04-01,1995-04-01,1996-10-01,1995-04-01,1995-04-01&coed=2021-04-01,2021-04-01,2021-04-01,2021-04-01,2021-04-01,2021-04-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d&link_values=false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none&mw=3,3,3,3,3,3&lw=2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0&fml=a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6&transformation=lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1995-04-01,1995-04-01,1995-04-01,1996-10-01,1995-04-01,1995-04-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'EA19BVBUTE02STSAM': "Business tendency surveys (services): Business situation - Activity: Tendency: National indicator for Euro Area",
        'BVCICP02EZM460S': "Business Tendency Surveys for Services: Confidence Indicators: Composite Indicators: European Commission and National Indicators for the Euro Area",
        'BVEMTE02EZM460S': "Business Tendency Surveys for Services: Employment: Tendency: European Commission Indicator for the Euro Area",
        'BVEMFT02EZM460S': "Business Tendency Surveys for Services: Employment: Future Tendency: European Commission and National Indicators for the Euro Area",
        'BVDEFT02EZM460S': "Business Tendency Surveys for Services: Demand Evolution: Future Tendency: European Commission Indicator for the Euro Area",
        'BVDETE02EZM460S': "Business Tendency Surveys for Services: Demand Evolution: Tendency: European Commission Indicator for the Euro Area"}
    description = "Business tendency surveys (services), Monthly, Seasonally Adjusted"
    return df, name_list, description


def Business_Tendency_Surveys_Manufacturing_Quarterly():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=BSCURT02EZQ160S,BSOITE02EZQ460S&scale=left,left&cosd=1985-01-01,1985-01-01&coed=2021-04-01,2021-04-01&line_color=%234572a7,%23aa4643&link_values=false,false&line_style=solid,solid&mark_type=none,none&mw=3,3&lw=2,2&ost=-99999,-99999&oet=99999,99999&mma=0,0&fml=a,a&fq=Quarterly,Quarterly&fam=avg,avg&fgst=lin,lin&fgsnd=2020-02-01,2020-02-01&line_index=1,2&transformation=lin,lin&vintage_date=2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07&nd=1985-01-01,1985-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'BSCURT02EZQ160S': "Business Tendency Surveys for Manufacturing: Capacity Utilization: Rate of Capacity Utilization: European Commission and National Indicators for the Euro Area",
        'BSOITE02EZQ460S': "Business Tendency Surveys for Manufacturing: Orders Inflow: Tendency: European Commission Indicator for the Euro Area"}
    description = "Business tendency surveys (manufacturing), Quarterly, Seasonally Adjusted"
    return df, name_list, description


def Business_Tendency_Surveys_Manufacturing_Monthly():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=BSSPFT02EZM460S,BSOBLV02EZM460S,BSEMFT02EZM460S,BSFGLV02EZM460S,BSXRLV02EZM086S,BSCICP02EZM460S,BSPRTE02EZM460S,BSPRFT02EZM460S&scale=left,left,left,left,left,left,left,left&cosd=1985-01-01,1985-01-01,1985-01-01,1985-01-01,1985-01-01,1985-01-01,1985-01-01,1985-01-01&coed=2021-04-01,2021-04-01,2021-04-01,2021-04-01,2021-04-01,2021-04-01,2021-04-01,2021-04-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c&link_values=false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8&transformation=lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1985-01-01,1985-01-01,1985-01-01,1985-01-01,1985-01-01,1985-01-01,1985-01-01,1985-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'BSSPFT02EZM460S': "Business Tendency Surveys for Manufacturing: Selling Prices: Future Tendency: European Commission Indicator for the Euro Area",
        'BSOBLV02EZM460S': "Business Tendency Surveys for Manufacturing: Order Books: Level: European Commission and National Indicators for the Euro Area",
        'BSEMFT02EZM460S': "Business Tendency Surveys for Manufacturing: Employment: Future Tendency: European Commission and National Indicators for the Euro Area",
        'BSFGLV02EZM460S': "Business Tendency Surveys for Manufacturing: Finished Goods Stocks: Level: European Commission and National Indicators for the Euro Area",
        'BSXRLV02EZM086S': "Business Tendency Surveys for Manufacturing: Export Order Books or Demand: Level: European Commission Indicator for the Euro Area",
        'BSCICP02EZM460S': "Business Tendency Surveys for Manufacturing: Confidence Indicators: Composite Indicators: European Commission and National Indicators for the Euro Area",
        'BSPRTE02EZM460S': "Business Tendency Surveys for Manufacturing: Production: Tendency: European Commission and National Indicators for the Euro Area",
        'BSPRFT02EZM460S': "Business Tendency Surveys for Manufacturing: Production: Future Tendency: European Commission and National Indicators for the Euro Area"}
    description = "Business tendency surveys (manufacturing), Monthly, Seasonally Adjusted"
    return df, name_list, description


def Business_Tendency_Surveys_Retail_Trade():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EA19BREMFT02STSAM,EA19BRODFT02STSAM,EA19BRVSLV02STSAM,EA19BRCICP02STSAM,EA19BRBUFT02STSAM,EA19BRBUTE02STSAM&scale=left,left,left,left,left,left&cosd=1985-04-01,1985-02-01,1985-01-01,1985-01-01,1985-01-01,1985-01-01&coed=2021-04-01,2021-04-01,2021-04-01,2021-04-01,2021-04-01,2021-04-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d&link_values=false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none&mw=3,3,3,3,3,3&lw=2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0&fml=a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6&transformation=lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1985-04-01,1985-02-01,1985-01-01,1985-01-01,1985-01-01,1985-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'EA19BREMFT02STSAM': "Business tendency surveys (retail trade): Employment: Future tendency: National indicator for the Euro Area",
        'EA19BRODFT02STSAM': "Business tendency surveys (retail trade): Order intentions or Demand: Future tendency: National indicator for the Euro Area",
        'EA19BRVSLV02STSAM': "Business tendency surveys (retail trade): Volume of stocks: Level: National indicator for the Euro Area",
        'EA19BRCICP02STSAM': "Business tendency surveys (retail trade): Confidence indicators: Composite indicators: National indicator for the Euro Area",
        'EA19BRBUFT02STSAM': "Business tendency surveys (retail trade): Business situation - Activity: Future tendency: National indicator for Euro Area",
        'EA19BRBUTE02STSAM': "Business tendency surveys (retail trade): Business situation - Activity: Tendency: National indicator for Euro Area"}
    description = "Business tendency surveys (retail trade), Monthly, Seasonally Adjusted"
    return df, name_list, description


def Labor_Compoenstiveion_Quarterly_Adj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=LCEAMN01EZQ661S,LCEAPR01EZQ661S&scale=left,left&cosd=1971-01-01,1996-01-01&coed=2020-10-01,2020-10-01&line_color=%234572a7,%23aa4643&link_values=false,false&line_style=solid,solid&mark_type=none,none&mw=3,3&lw=2,2&ost=-99999,-99999&oet=99999,99999&mma=0,0&fml=a,a&fq=Quarterly,Quarterly&fam=avg,avg&fgst=lin,lin&fgsnd=2020-02-01,2020-02-01&line_index=1,2&transformation=lin,lin&vintage_date=2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07&nd=1971-01-01,1996-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'LCEAMN01EZQ661S': "Hourly Earnings: Manufacturing for the Euro Area",
        'LCEAPR01EZQ661S': "Hourly Earnings: Private Sector for the Euro Area"
    }
    description = "Labor Compensation, Quarterly, Seasonally Adjusted"
    return df, name_list, description


def Labor_Compoenstiveion_Quarterly_NAdj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=LCEAMN01EZQ661S,LCEAPR01EZQ661S&scale=left,left&cosd=1971-01-01,1996-01-01&coed=2020-10-01,2020-10-01&line_color=%234572a7,%23aa4643&link_values=false,false&line_style=solid,solid&mark_type=none,none&mw=3,3&lw=2,2&ost=-99999,-99999&oet=99999,99999&mma=0,0&fml=a,a&fq=Quarterly,Quarterly&fam=avg,avg&fgst=lin,lin&fgsnd=2020-02-01,2020-02-01&line_index=1,2&transformation=lin,lin&vintage_date=2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07&nd=1971-01-01,1996-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'LCEAMN01EZQ661N': "Hourly Earnings: Manufacturing for the Euro Area",
        'LCEAPR01EZQ661N': "Hourly Earnings: Private Sector for the Euro Area"
    }
    description = "Labor Compensation, Quarterly, Not Seasonally Adjusted"
    return df, name_list, description


def Unit_Labor_costs():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=ULQECU01EZQ661S,ULQEUL01EZQ659S,ULQELP01EZQ661S&scale=left,left,left&cosd=1995-01-01,1996-01-01,1995-01-01&coed=2020-10-01,2020-10-01,2020-10-01&line_color=%234572a7,%23aa4643,%2389a54e&link_values=false,false,false&line_style=solid,solid,solid&mark_type=none,none,none&mw=3,3,3&lw=2,2,2&ost=-99999,-99999,-99999&oet=99999,99999,99999&mma=0,0,0&fml=a,a,a&fq=Quarterly,Quarterly,Quarterly&fam=avg,avg,avg&fgst=lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3&transformation=lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07&nd=1995-01-01,1996-01-01,1995-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'ULQECU01EZQ661S': "Early Estimate of Quarterly ULC Indicators: Total Labor Compensation per Unit of Labor Input for the Euro Area",
        'ULQEUL01EZQ659S': "Early Estimate of Quarterly ULC Indicators: Total for the Euro Area",
        'ULQELP01EZQ661S': "Early Estimate of Quarterly ULC Indicators: Total Labor Productivity for the Euro Area"}
    description = "Unit Labor Costs, Quarterly, Seasonally Adjusted"
    return df, name_list, description


def Labor_Force_Survey_Rates_Quarterly_NAdj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=LRHU24TTEZQ156N,LRHU24FEEZQ156N,LRHU24MAEZQ156N,LRHUADMAEZQ156N,LRHUADTTEZQ156N,LRHUADFEEZQ156N,LRHUTTFEEZQ156N,LRHUTTTTEZQ156N,LRHUTTMAEZQ156N&scale=left,left,left,left,left,left,left,left,left&cosd=1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1993-01-01,1993-01-01,1993-01-01&coed=2021-01-01,2021-01-01,2021-01-01,2021-01-01,2021-01-01,2021-01-01,2021-01-01,2021-01-01,2021-01-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c,%23b5ca92&link_values=false,false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a,a&fq=Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly&fam=avg,avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8,9&transformation=lin,lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1993-01-01,1993-01-01,1993-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'LRHU24TTEZQ156N': "Harmonized Unemployment: Aged 15-24: All Persons for the Euro Area",
        'LRHU24FEEZQ156N': "Harmonized Unemployment: Aged 15-24: Females for the Euro Area",
        'LRHU24MAEZQ156N': "Harmonized Unemployment: Aged 15-24: Males for the Euro Area",
        'LRHUADMAEZQ156N': "Harmonized Unemployment: Aged 25 and Over: Males for the Euro Area",
        'LRHUADTTEZQ156N': "Harmonized Unemployment: Aged 25 and Over: All Persons for the Euro Area",
        'LRHUADFEEZQ156N': "Harmonized Unemployment: Aged 25 and Over: Females for the Euro Area",
        'LRHUTTFEEZQ156N': "Harmonized Unemployment: Total: Females for the Euro Area",
        'LRHUTTTTEZQ156N': "Harmonized Unemployment Rate: Total: All Persons for the Euro Area",
        'LRHUTTMAEZQ156N': "Harmonized Unemployment: Total: Males for the Euro Area"}
    description = "Labor Force Survey - quarterly rates, Quarterly, Not Seasonally Adjusted"
    return df, name_list, description


def Labor_Force_Survey_Rates_Quarterly_Adj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=LRHU24MAEZQ156S,LRHU24TTEZQ156S,LRHU24FEEZQ156S,LRHUADFEEZQ156S,LRHUADMAEZQ156S,LRHUADTTEZQ156S,LRHUTTTTEZQ156S,LRHUTTMAEZQ156S,LRHUTTFEEZQ156S&scale=left,left,left,left,left,left,left,left,left&cosd=1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1990-07-01,1990-07-01,1990-07-01&coed=2021-01-01,2021-01-01,2021-01-01,2021-01-01,2021-01-01,2021-01-01,2021-01-01,2021-01-01,2021-01-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c,%23b5ca92&link_values=false,false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a,a&fq=Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly&fam=avg,avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8,9&transformation=lin,lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1990-07-01,1990-07-01,1990-07-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'LRHU24MAEZQ156S': "Harmonized Unemployment: Aged 15-24: Males for the Euro Area",
        'LRHU24TTEZQ156S': "Harmonized Unemployment: Aged 15-24: All Persons for the Euro Area",
        'LRHU24FEEZQ156S': "Harmonized Unemployment: Aged 15-24: Females for the Euro Area",
        'LRHUADFEEZQ156S': "Harmonized Unemployment: Aged 25 and Over: Females for the Euro Area",
        'LRHUADMAEZQ156S': "Harmonized Unemployment: Aged 25 and Over: Males for the Euro Area",
        'LRHUADTTEZQ156S': "Harmonized Unemployment: Aged 25 and Over: All Persons for the Euro Area",
        'LRHUTTTTEZQ156S': "Harmonized Unemployment Rate: Total: All Persons for the Euro Area",
        'LRHUTTMAEZQ156S': "Harmonized Unemployment: Total: Males for the Euro Area",
        'LRHUTTFEEZQ156S': "Harmonized Unemployment: Total: Females for the Euro Area"}
    description = "Labor Force Survey - quarterly rates, Quarterly, Seasonally Adjusted"
    return df, name_list, description


def Labor_Force_Survey_Rates_Monthly_NAdj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=LRHUTTFEEZM156N,LRHUTTMAEZM156N,LRHUTTTTEZM156N,LRHUADTTEZM156N,LRHUADMAEZM156N,LRHUADFEEZM156N,LRHU24FEEZM156N,LRHU24MAEZM156N,LRHU24TTEZM156N&scale=left,left,left,left,left,left,left,left,left&cosd=1993-01-01,1993-01-01,1993-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01&coed=2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c,%23b5ca92&link_values=false,false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8,9&transformation=lin,lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1993-01-01,1993-01-01,1993-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'LRHUTTFEEZM156N': "Harmonized Unemployment: Total: Females for the Euro Area",
        'LRHUTTMAEZM156N': "Harmonized Unemployment: Total: Males for the Euro Area",
        'LRHUTTTTEZM156N': "Harmonized Unemployment Rate: Total: All Persons for the Euro Area",
        'LRHUADTTEZM156N': "Harmonized Unemployment: Aged 25 and Over: All Persons for the Euro Area",
        'LRHUADMAEZM156N': "Harmonized Unemployment: Aged 25 and Over: Males for the Euro Area",
        'LRHUADFEEZM156N': "Harmonized Unemployment: Aged 25 and Over: Females for the Euro Area",
        'LRHU24FEEZM156N': "Harmonized Unemployment: Aged 15-24: Females for the Euro Area",
        'LRHU24MAEZM156N': "Harmonized Unemployment: Aged 15-24: Males for the Euro Area",
        'LRHU24TTEZM156N': "Harmonized Unemployment: Aged 15-24: All Persons for the Euro Area"}
    description = "Labor Force Survey - quarterly rates, Monthly, Seasonally Adjusted"
    return df, name_list, description


def Labor_Force_Survey_Level_Quarterly_NAdj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=LRHUTTFEEZM156N,LRHUTTMAEZM156N,LRHUTTTTEZM156N,LRHUADTTEZM156N,LRHUADMAEZM156N,LRHUADFEEZM156N,LRHU24FEEZM156N,LRHU24MAEZM156N,LRHU24TTEZM156N&scale=left,left,left,left,left,left,left,left,left&cosd=1993-01-01,1993-01-01,1993-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01&coed=2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c,%23b5ca92&link_values=false,false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8,9&transformation=lin,lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1993-01-01,1993-01-01,1993-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'LFHU24FEEZQ647N': "Harmonized Unemployment: Aged 15-24: Females for the Euro Area",
        'LFHU24TTEZQ647N': "Harmonized Unemployment: Aged 15-24: All Persons for the Euro Area",
        'LFHU24MAEZQ647N': "Harmonized Unemployment: Aged 15-24: Males for the Euro Area",
        'LFHUADTTEZQ647N': "Harmonized Unemployment: Aged 25 and Over: All Persons for the Euro Area",
        'LFHUADMAEZQ647N': "Harmonized Unemployment: Aged 25 and Over: Males for the Euro Area",
        'LFHUADFEEZQ647N': "Harmonized Unemployment: Aged 25 and Over: Females for the Euro Area",
        'LFHUTTMAEZQ647N': "Total Harmonized Unemployment: Males for the Euro Area",
        'LFHUTTFEEZQ647N': "Total Harmonized Unemployment: Females for the Euro Area",
        'LFHUTTTTEZQ647N': "Total Harmonized Unemployment: All Persons for the Euro Area"}
    description = "Labor Force Survey - quarterly levels, Quarterly, Not Seasonally Adjusted"
    return df, name_list, description


def Labor_Force_Survey_Level_Quarterly_Adj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=LRHUTTFEEZM156N,LRHUTTMAEZM156N,LRHUTTTTEZM156N,LRHUADTTEZM156N,LRHUADMAEZM156N,LRHUADFEEZM156N,LRHU24FEEZM156N,LRHU24MAEZM156N,LRHU24TTEZM156N&scale=left,left,left,left,left,left,left,left,left&cosd=1993-01-01,1993-01-01,1993-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01&coed=2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c,%23b5ca92&link_values=false,false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8,9&transformation=lin,lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1993-01-01,1993-01-01,1993-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'LFHU24TTEZQ647S': "Harmonized Unemployment: Aged 15-24: All Persons for the Euro Area",
        'LFHU24MAEZQ647S': "Harmonized Unemployment: Aged 15-24: Males for the Euro Area",
        'LFHU24FEEZQ647S': "Harmonized Unemployment: Aged 15-24: Females for the Euro Area",
        'LFHUTTFEEZQ647S': "Total Harmonized Unemployment: Females for the Euro Area",
        'LFHUTTTTEZQ647S': "Total Harmonized Unemployment: All Persons for the Euro Area",
        'LFHUTTMAEZQ647S': "Total Harmonized Unemployment: Males for the Euro Area",
        'LFHUADMAEZQ647S': "Harmonized Unemployment: Aged 25 and Over: Males for the Euro Area",
        'LFHUADFEEZQ647S': "Harmonized Unemployment: Aged 25 and Over: Females for the Euro Area",
        'LFHUADTTEZQ647S': "Harmonized Unemployment: Aged 25 and Over: All Persons for the Euro Area"}
    description = "Labor Force Survey - quarterly levels, Quarterly, Seasonally Adjusted"
    return df, name_list, description


def Labor_Force_Survey_Level_Monthly_Adj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=LFHU24FEEZM647S,LFHU24TTEZM647S,LFHU24MAEZM647S,LFHUADFEEZM647S,LFHUADTTEZM647S,LFHUADMAEZM647S,LFHUTTTTEZM647S,LFHUTTMAEZM647S,LFHUTTFEEZM647S&scale=left,left,left,left,left,left,left,left,left&cosd=1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01&coed=2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c,%23b5ca92&link_values=false,false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8,9&transformation=lin,lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'LFHU24FEEZM647S': "Harmonized Unemployment: Aged 15-24: Females for the Euro Area",
        'LFHU24TTEZM647S': "Harmonized Unemployment: Aged 15-24: All Persons for the Euro Area",
        'LFHU24MAEZM647S': "Harmonized Unemployment: Aged 15-24: Males for the Euro Area",
        'LFHUADFEEZM647S': "Harmonized Unemployment: Aged 25 and Over: Females for the Euro Area",
        'LFHUADTTEZM647S': "Harmonized Unemployment: Aged 25 and Over: All Persons for the Euro Area",
        'LFHUADMAEZM647S': "Harmonized Unemployment: Aged 25 and Over: Males for the Euro Area",
        'LFHUTTTTEZM647S': "Total Harmonized Unemployment: All Persons for the Euro Area",
        'LFHUTTMAEZM647S': "Total Harmonized Unemployment: Males for the Euro Area",
        'LFHUTTFEEZM647S': "Total Harmonized Unemployment: Females for the Euro Area"}
    description = "Labor Force Survey - quarterly levels, Monthly, Seasonally Adjusted"
    return df, name_list, description


def Labor_Force_Survey_Level_Monthly_NAdj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=LFHU24MAEZM647N,LFHU24FEEZM647N,LFHU24TTEZM647N,LFHUADMAEZM647N,LFHUADFEEZM647N,LFHUADTTEZM647N,LFHUTTFEEZM647N,LFHUTTTTEZM647N,LFHUTTMAEZM647N&scale=left,left,left,left,left,left,left,left,left&cosd=1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01&coed=2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01,2021-03-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c,%23b5ca92&link_values=false,false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7,8,9&transformation=lin,lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01,1995-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'LFHU24MAEZM647N': "Harmonized Unemployment: Aged 15-24: Males for the Euro Area",
        'LFHU24FEEZM647N': "Harmonized Unemployment: Aged 15-24: Females for the Euro Area",
        'LFHU24TTEZM647N': "Harmonized Unemployment: Aged 15-24: All Persons for the Euro Area",
        'LFHUADMAEZM647N': "Harmonized Unemployment: Aged 25 and Over: Males for the Euro Area",
        'LFHUADFEEZM647N': "Harmonized Unemployment: Aged 25 and Over: Females for the Euro Area",
        'LFHUADTTEZM647N': "Harmonized Unemployment: Aged 25 and Over: All Persons for the Euro Area",
        'LFHUTTFEEZM647N': "Total Harmonized Unemployment: Females for the Euro Area",
        'LFHUTTTTEZM647N': "Total Harmonized Unemployment: All Persons for the Euro Area",
        'LFHUTTMAEZM647N': "Total Harmonized Unemployment: Males for the Euro Area"}
    description = "Labor Force Survey - quarterly levels, Monthly, Not Seasonally Adjusted"
    return df, name_list, description


def Production_Monthly_Adj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EA19PRINTO01GYSAM,EA19PRMNCG03IXOBSAM,EA19PRMNCG02IXOBSAM,EA19PRMNVG01IXOBSAM,EA19PRMNTO01IXOBSAM,EA19PRMNIG01IXOBSAM,EA19PRCNTO01IXOBSAM&scale=left,left,left,left,left,left,left&cosd=1976-07-01,1985-01-01,1990-01-01,1985-01-01,1980-01-01,1985-01-01,1985-01-01&coed=2021-02-01,2017-12-01,2018-12-01,2018-12-01,2021-02-01,2018-12-01,2021-02-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd&link_values=false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2017-12-01,2018-12-01,2018-12-01,2020-02-01,2018-12-01,2020-02-01&line_index=1,2,3,4,5,6,7&transformation=lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1976-07-01,1985-01-01,1990-01-01,1985-01-01,1980-01-01,1985-01-01,1985-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'EA19PRINTO01GYSAM': "Production: Industry: Total industry: Total industry excluding construction for the Euro Area",
        'EA19PRMNCG03IXOBSAM': "Production: Manufacturing: Consumer goods: Non durable goods for the Euro Area",
        'EA19PRMNCG02IXOBSAM': "Production: Manufacturing: Consumer goods: Durable goods for the Euro Area",
        'EA19PRMNVG01IXOBSAM': "Production: Manufacturing: Investment goods: Total for the Euro Area",
        'EA19PRMNTO01IXOBSAM': "Production: Manufacturing: Total manufacturing: Total manufacturing for the Euro Area",
        'EA19PRMNIG01IXOBSAM': "Production: Manufacturing: Intermediate goods: Total for the Euro Area",
        'EA19PRCNTO01IXOBSAM': "Production: Construction: Total construction: Total for the Euro Area"}
    description = "Production, Monthly, Seasonally Adjusted"
    return df, name_list, description


def Production_Quarterly_Adj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PRINTO01EZQ659S,PRMNVG01EZQ661S,PRMNCG02EZQ661S,PRMNCG03EZQ661S,PRMNTO01EZQ661S,PRMNIG01EZQ661S,PRCNTO01EZQ661S&scale=left,left,left,left,left,left,left&cosd=1976-07-01,1985-01-01,1990-01-01,1985-01-01,1980-01-01,1985-01-01,1985-01-01&coed=2020-10-01,2018-10-01,2018-10-01,2017-10-01,2020-10-01,2018-10-01,2020-10-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd&link_values=false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a&fq=Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly&fam=avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2018-10-01,2018-10-01,2017-10-01,2020-02-01,2018-10-01,2020-02-01&line_index=1,2,3,4,5,6,7&transformation=lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1976-07-01,1985-01-01,1990-01-01,1985-01-01,1980-01-01,1985-01-01,1985-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'PRINTO01EZQ659S': "Total Industry Production Excluding Construction for the Euro Area",
        'PRMNVG01EZQ661S': "Total Production of Investment Goods for Manufacturing for the Euro Area",
        'PRMNCG02EZQ661S': "Production of Durable Consumer Goods for Manufacturing for the Euro Area",
        'PRMNCG03EZQ661S': "Production of Nondurable Consumer Goods for Manufacturing for the Euro Area",
        'PRMNTO01EZQ661S': "Total Manufacturing Production for the Euro Area",
        'PRMNIG01EZQ661S': "Total Production of Intermediate Goods for Manufacturing for the Euro Area",
        'PRCNTO01EZQ661S': "Total Construction for the Euro Area"}
    description = "Production, Monthly, Not Seasonally Adjusted"
    return df, name_list, description


def Production_Monthly_NAdj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EA19PRMNIG01IXOBM,EA19PRMNTO01IXOBM,EA19PRMNCG02IXOBM,EA19PRMNCG03IXOBM,EA19PRMNVG01IXOBM,EA19PRCNTO01IXOBM,EA19PRINTO01IXOBM&scale=left,left,left,left,left,left,left&cosd=1985-01-01,1980-01-01,1990-01-01,1985-01-01,1985-01-01,1985-01-01,1980-01-01&coed=2018-12-01,2021-02-01,2018-12-01,2018-12-01,2018-12-01,2021-02-01,2021-02-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd&link_values=false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin&fgsnd=2018-12-01,2020-02-01,2018-12-01,2018-12-01,2018-12-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7&transformation=lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1985-01-01,1980-01-01,1990-01-01,1985-01-01,1985-01-01,1985-01-01,1980-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'EA19PRMNIG01IXOBM': "Production: Manufacturing: Intermediate goods: Total for the Euro Area",
        'EA19PRMNTO01IXOBM': "Production: Manufacturing: Total manufacturing: Total manufacturing for the Euro Area",
        'EA19PRMNCG02IXOBM': "Production: Manufacturing: Consumer goods: Durable goods for the Euro Area",
        'EA19PRMNCG03IXOBM': "Production: Manufacturing: Consumer goods: Non durable goods for the Euro Area",
        'EA19PRMNVG01IXOBM': "Production: Manufacturing: Investment goods: Total for the Euro Area",
        'EA19PRCNTO01IXOBM': "Production: Construction: Total construction: Total for the Euro Area",
        'EA19PRINTO01IXOBM': "Production: Industry: Total industry: Total industry excluding construction for the Euro Area"}
    description = "Production, Monthly, Not Seasonally Adjusted"
    return df, name_list, description


def Production_Quarterly_NAdj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=PRMNCG03EZQ661N,PRMNCG02EZQ661N,PRMNVG01EZQ661N,PRMNIG01EZQ661N,PRMNTO01EZQ661N,PRINTO01EZQ661N,PRCNTO01EZQ661N&scale=left,left,left,left,left,left,left&cosd=1985-01-01,1990-01-01,1985-01-01,1985-01-01,1980-01-01,1980-01-01,1985-01-01&coed=2018-10-01,2018-10-01,2018-10-01,2018-10-01,2020-10-01,2020-10-01,2020-10-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd&link_values=false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a&fq=Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly&fam=avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin&fgsnd=2018-10-01,2018-10-01,2018-10-01,2018-10-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7&transformation=lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1985-01-01,1990-01-01,1985-01-01,1985-01-01,1980-01-01,1980-01-01,1985-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'PRMNCG03EZQ661N': "Production of Nondurable Consumer Goods for Manufacturing for the Euro Area",
        'PRMNCG02EZQ661N': "Production of Durable Consumer Goods for Manufacturing for the Euro Area",
        'PRMNVG01EZQ661N': "Total Production of Investment Goods for Manufacturing for the Euro Area",
        'PRMNIG01EZQ661N': "Total Production of Intermediate Goods for Manufacturing for the Euro Area",
        'PRMNTO01EZQ661N': "Total Manufacturing Production for the Euro Area",
        'PRINTO01EZQ661N': "Total Industry Production Excluding Construction for the Euro Area",
        'PRCNTO01EZQ661N': "Total Construction for the Euro Area"}
    description = "Production, Quarterly, Not Seasonally Adjusted"
    return df, name_list, description


def Sales_Monthly_Adj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EA19SLMNTO02IXOBSAM,EA19SLMNIG02IXOBSAM,EA19SLMNCD02IXOBSAM,EA19SLMNCN02IXOBSAM,EA19SLMNVG02IXOBSAM,EA19SLRTTO01IXOBSAM,EA19SLRTTO02IXOBSAM,EA19SLRTCR03IXOBSAM&scale=left,left,left,left,left,left,left,left&cosd=1980-01-01,1990-01-01,1993-01-01,1995-01-01,1980-01-01,1995-01-01,1995-01-01,1970-01-01&coed=2021-02-01,2018-12-01,2018-12-01,2018-12-01,2018-12-01,2021-02-01,2021-02-01,2018-12-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c&link_values=false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2018-12-01,2018-12-01,2018-12-01,2018-12-01,2020-02-01,2020-02-01,2018-12-01&line_index=1,2,3,4,5,6,7,8&transformation=lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1980-01-01,1990-01-01,1993-01-01,1995-01-01,1980-01-01,1995-01-01,1995-01-01,1970-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'EA19SLMNTO02IXOBSAM': "Sales: Manufacturing: Total manufacturing: Value for the Euro Area",
        'EA19SLMNIG02IXOBSAM': "Sales: Manufacturing: Intermediate goods: Value for the Euro Area",
        'EA19SLMNCD02IXOBSAM': "Sales: Manufacturing: Consumer goods durable: Value for the Euro Area",
        'EA19SLMNCN02IXOBSAM': "Sales: Manufacturing: Consumer goods non durable: Value for the Euro Area",
        'EA19SLMNVG02IXOBSAM': "Sales: Manufacturing: Investment goods: Value for the Euro Area",
        'EA19SLRTTO01IXOBSAM': "Sales: Retail trade: Total retail trade: Volume for the Euro Area",
        'EA19SLRTTO02IXOBSAM': "Sales: Retail trade: Total retail trade: Value for the Euro Area",
        'EA19SLRTCR03IXOBSAM': "Sales: Retail trade: Car registration: Passenger cars for the Euro Area"}
    description = "Sales, Monthly, Seasonally Adjusted"
    return df, name_list, description


def Sales_Quarterly_Adj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=SLMNTO02EZQ661S,SLMNVG02EZQ661S,SLMNCD02EZQ661S,SLMNCN02EZQ661S,SLMNIG02EZQ661S,SLRTTO02EZQ661S,SLRTTO01EZQ659S,SLRTCR03EZQ661S&scale=left,left,left,left,left,left,left,left&cosd=1980-01-01,1980-01-01,1993-01-01,1995-01-01,1990-01-01,1995-01-01,1996-01-01,1970-01-01&coed=2020-10-01,2018-10-01,2018-10-01,2018-10-01,2018-10-01,2020-10-01,2020-10-01,2018-10-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd,%23a47d7c&link_values=false,false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a,a&fq=Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly&fam=avg,avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin,lin&fgsnd=2020-02-01,2018-10-01,2018-10-01,2018-10-01,2018-10-01,2020-02-01,2020-02-01,2018-10-01&line_index=1,2,3,4,5,6,7,8&transformation=lin,lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1980-01-01,1980-01-01,1993-01-01,1995-01-01,1990-01-01,1995-01-01,1996-01-01,1970-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'SLMNTO02EZQ661S': "Sales Value of Total Manufactured Goods for the Euro Area",
        'SLMNVG02EZQ661S': "Sales Value of Manufactured Investment Goods for the Euro Area",
        'SLMNCD02EZQ661S': "Sales Value of Manufactured Durable Consumer Goods for the Euro Area",
        'SLMNCN02EZQ661S': "Sales Value of Manufactured Nondurable Consumer Goods for the Euro Area",
        'SLMNIG02EZQ661S': "Sales Value of Manufactured Intermediate Goods for the Euro Area",
        'SLRTTO02EZQ661S': "Value of Total Retail Trade sales for the Euro Areaa",
        'SLRTTO01EZQ659S': "Volume of Total Retail Trade sales for the Euro Area",
        'SLRTCR03EZQ661S': "Retail Trade Sales: Passenger Car Registrations for the Euro Area"}
    description = "Sales, Quarterly, Seasonally Adjusted"
    return df, name_list, description


def Sales_Monthly_NAdj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=EA19SLMNIG02IXOBM,EA19SLRTTO02IXOBM,EA19SLMNCD02IXOBM,EA19SLMNCN02IXOBM,EA19SLMNTO02IXOBM,EA19SLRTCR03IXOBM,EA19SLRTTO01IXOBM&scale=left,left,left,left,left,left,left&cosd=1990-01-01,1995-01-01,1993-01-01,1995-01-01,1980-01-01,1985-01-01,1995-01-01&coed=2018-12-01,2021-02-01,2018-12-01,2018-12-01,2021-02-01,2021-03-01,2021-02-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd&link_values=false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a&fq=Monthly,Monthly,Monthly,Monthly,Monthly,Monthly,Monthly&fam=avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin&fgsnd=2018-12-01,2020-02-01,2018-12-01,2018-12-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7&transformation=lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1990-01-01,1995-01-01,1993-01-01,1995-01-01,1980-01-01,1985-01-01,1995-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'EA19SLMNIG02IXOBM': "Sales: Manufacturing: Intermediate goods: Value for the Euro Area",
        'EA19SLRTTO02IXOBM': "Sales: Retail trade: Total retail trade: Value for the Euro Area",
        'EA19SLMNCD02IXOBM': "Sales: Manufacturing: Consumer goods durable: Value for the Euro Area",
        'EA19SLMNCN02IXOBM': "Sales: Manufacturing: Consumer goods non durable: Value for the Euro Area",
        'EA19SLMNTO02IXOBM': "Sales: Manufacturing: Total manufacturing: Value for the Euro Area",
        'EA19SLRTCR03IXOBM': "Sales: Retail trade: Car registration: Passenger cars for the Euro Area",
        'EA19SLRTTO01IXOBM': "Sales: Retail trade: Total retail trade: Volume for the Euro Area"}
    description = "Sales, Monthly, Not Seasonally Adjusted"
    return df, name_list, description


def Sales_Quarterly_NAdj():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=SLMNIG02EZQ661N,SLMNTO02EZQ661N,SLMNCD02EZQ661N,SLMNCN02EZQ661N,SLRTTO01EZQ661N,SLRTTO02EZQ661N,SLRTCR03EZQ661N&scale=left,left,left,left,left,left,left&cosd=1990-01-01,1980-01-01,1993-01-01,1995-01-01,1995-01-01,1995-01-01,1985-01-01&coed=2018-10-01,2020-10-01,2018-10-01,2018-10-01,2020-10-01,2020-10-01,2021-01-01&line_color=%234572a7,%23aa4643,%2389a54e,%2380699b,%233d96ae,%23db843d,%2392a8cd&link_values=false,false,false,false,false,false,false&line_style=solid,solid,solid,solid,solid,solid,solid&mark_type=none,none,none,none,none,none,none&mw=3,3,3,3,3,3,3&lw=2,2,2,2,2,2,2&ost=-99999,-99999,-99999,-99999,-99999,-99999,-99999&oet=99999,99999,99999,99999,99999,99999,99999&mma=0,0,0,0,0,0,0&fml=a,a,a,a,a,a,a&fq=Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly,Quarterly&fam=avg,avg,avg,avg,avg,avg,avg&fgst=lin,lin,lin,lin,lin,lin,lin&fgsnd=2018-10-01,2020-02-01,2018-10-01,2018-10-01,2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3,4,5,6,7&transformation=lin,lin,lin,lin,lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07,2021-06-07&nd=1990-01-01,1980-01-01,1993-01-01,1995-01-01,1995-01-01,1995-01-01,1985-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'SLMNIG02EZQ661N': "Sales Value of Manufactured Intermediate Goods for the Euro Area",
        'SLMNTO02EZQ661N': "Sales Value of Total Manufactured Goods for the Euro Area",
        'SLMNCD02EZQ661N': "Sales Value of Manufactured Durable Consumer Goods for the Euro Area",
        'SLMNCN02EZQ661N': "Sales Value of Manufactured Nondurable Consumer Goods for the Euro Area",
        'SLRTTO01EZQ661N': "Volume of Total Retail Trade sales for the Euro Area",
        'SLRTTO02EZQ661N': "Value of Total Retail Trade sales for the Euro Area",
        'SLRTCR03EZQ661N': "Retail Trade Sales: Passenger Car Registrations for the Euro Area"}
    description = "Sales, Quarterly, Not Seasonally Adjusted"
    return df, name_list, description


def Cumsumer_Opinion_Survey():
    tmp_url = url["fred_econ"] + "bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=off&txtcolor=%23444444&ts=12&tts=12&width=748&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CSCICP02EZM460S,CSESFT02EZM460S,CSINFT02EZM460S&scale=left,left,left&cosd=1973-01-01,1985-01-01,1985-01-01&coed=2021-04-01,2021-04-01,2021-04-01&line_color=%234572a7,%23aa4643,%2389a54e&link_values=false,false,false&line_style=solid,solid,solid&mark_type=none,none,none&mw=3,3,3&lw=2,2,2&ost=-99999,-99999,-99999&oet=99999,99999,99999&mma=0,0,0&fml=a,a,a&fq=Monthly,Monthly,Monthly&fam=avg,avg,avg&fgst=lin,lin,lin&fgsnd=2020-02-01,2020-02-01,2020-02-01&line_index=1,2,3&transformation=lin,lin,lin&vintage_date=2021-06-07,2021-06-07,2021-06-07&revision_date=2021-06-07,2021-06-07,2021-06-07&nd=1973-01-01,1985-01-01,1985-01-01"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    r = requests.get(tmp_url, headers=request_header)
    data_text = r.content
    df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    #df = df[list(df.columns[1:])].replace(".", np.nan).astype(float)
    name_list = {
        'CSCICP02EZM460S': "Consumer Opinion Surveys: Confidence Indicators: Composite Indicators: European Commission and National Indicators for the Euro Area",
        'CSESFT02EZM460S': "Consumer Opinion Surveys: Economic Situation: Future Tendency: European Commission Indicator for the Euro Area",
        'CSINFT02EZM460S': "Consumer Opinion Surveys: Consumer Prices: Future Tendency of Inflation: European Commission and National Indicators for the Euro Area"}
    description = "Consumer opinion surveys, Monthly, Seasonally Adjusted"
    return df, name_list, description


class ecb_data(object):
    def __init__(self, url=url["ecb"]):
        self.url = url

    def codebook(self):
        return "please follow the ECB's codebook: https://sdw.ecb.europa.eu/browse.do?node=9691101"

    def get_data(self,
                 datacode="ICP",
                 key="M.U2.N.000000.4.ANR",
                 startdate="2000-01-01",
                 enddate="2020-01-01"):
        """
        """
        tmp_url = self.url + "{}/".format(datacode) + "{}".format(key)
        ua = UserAgent(verify_ssl=False)
        request_header = {"User-Agent": ua.random, 'Accept': 'text/csv'}
        request_params = {
            "startPeriod": "{}".format(startdate),
            "endPeriod": "{}".format(enddate)
        }
        r = requests.get(
            tmp_url,
            params=request_params,
            headers=request_header)
        data_text = r.content
        df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
        return df


class eurostat_data(object):
    def __init__(self, url=url["eurostat"]):
        self.url = url

    def codebook(self):
        return "please follow the EuroStat's codebook: \nhttps://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&dir=dic"

    def get_data(self,
                 datasetcode="nama_10_gdp",
                 precision="1",
                 unit="CP_MEUR",
                 na_item="B1GQ",
                 time="2020"):
        """
        """
        tmp_url = self.url + "{}".format(datasetcode)
        ua = UserAgent(verify_ssl=False)
        request_header = {"User-Agent": ua.random, 'Accept': 'text/csv'}
        request_params = {
            "precision": "{}".format(precision),
            "unit": "{}".format(unit),
            "na_item": "{}".format(na_item),
            "time": "{}".format(time)
        }
        r = requests.get(
            tmp_url,
            params=request_params,
            headers=request_header)
        data_text = r.text
        data_json = demjson.decode(data_text)
        value = data_json['value']
        abb = data_json['dimension']['geo']['category']['index']
        abb = {abb[k]: k for k in abb}
        geo = data_json['dimension']['geo']['category']['label']
        geo_list = [abb[int(k)] for k in list(value.keys())]
        geo = [geo[k] for k in geo_list]
        df = pd.DataFrame(
            {"Geo": geo, "{}".format(na_item): list(value.values())})
        return df


if __name__ == "__main__":
    data, name_list = CPI_monthly()

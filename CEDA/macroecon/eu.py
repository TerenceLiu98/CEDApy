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
    "ecb": "https://sdw-wsrest.ecb.europa.eu/service/data/",
    "OECD": "https://stats.oecd.org/sdmx-json/data/DP_LIVE/"
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


def Leading_Indicators_OECD(startdate = "1950-01", enddate = "2021-05"):
    # CLI
    tmp_url = url["OECD"] + "EA19.CLI.AMPLITUD.LTRENDIDX.M/OECD"
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
    df_cli.columns = ["Date", "EU_OECD_CLI"]
    df_cli["Date"] = pd.to_datetime(df_cli["Date"], format = "%Y-%m")
    df_cli["EU_OECD_CLI"] = df_cli["EU_OECD_CLI"].astype(float)
    #BCI
    tmp_url = url["OECD"] + "EA19.BCI.AMPLITUD.LTRENDIDX.M/OECD"
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
    df_bci.columns = ["Date", "EU_OECD_BCI"]
    df_bci["Date"] = pd.to_datetime(df_bci["Date"], format = "%Y-%m")
    df_bci["EU_OECD_BCI"] = df_bci["EU_OECD_BCI"].astype(float)
    # CCI
    tmp_url = url["OECD"] + "EA19.CCI.AMPLITUD.LTRENDIDX.M/OECD"
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
    df_cci.columns = ["Date", "EU_OECD_CCI"]
    df_cci["Date"] = pd.to_datetime(df_cci["Date"], format = "%Y-%m")
    df_cci["EU_OECD_CCI"] = df_cci["EU_OECD_CCI"].astype(float)
    df = pd.merge_asof(df_cli, df_bci, on = "Date")
    df = pd.merge_asof(df, df_cci, on = "Date")
    
    return df


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


def Labor_Compensation_Quarterly_Adj():
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


def Labor_Compensation_Quarterly_NAdj():
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


def Consumer_Opinion_Survey():
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

def EU_EPU_Monthly():
    df = pd.read_excel("https://www.policyuncertainty.com/media/Europe_Policy_Uncertainty_Data.xlsx")[:-1]
    df['Date']=pd.to_datetime(df['Year'].apply(str).str.cat(df['Month'].apply(int).apply(str),sep='-'), format='%Y-%m')
    df = df[["Date", "European_News_Index", "Germany_News_Index", "Italy_News_Index", "UK_News_Index", "France_News_Index"]]
    return df

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

def QtoM(data:pd.Series):
    date = pd.PeriodIndex(data.str.replace(r'(Q\d)_(\d+)', r'20\2-\1'), freq='Q').strftime('%Y-%m-%d')
    return date

# EU - Main Economic Indicator
ecb = ecb_data()
eurostat = eurostat_data()
eu_columns_list = {
    "Gross Domestic Product", "Private Finance Consumption", "Government final consumption",
    "Gross fixed capital formation", "Changes in inventories and acquisition less disposals of valuables",
    "Exports of goods and services", "Imports of goods and services"
    }

# https://www.ecb.europa.eu/stats/ecb_statistics/key_euro_area_indicators/html/index.en.html

startdate, enddate = "2010-01-01", "2021-01-01"
daterange = pd.DataFrame({"Date": pd.date_range(start=startdate, end=enddate, freq="MS")})

class real_sector():
    def __init__(self, startdate=startdate, enddate=enddate, daterange=daterange):
        self.startdate = startdate
        self.enddate = enddate
        self.daterange = daterange
        
class current_price_gdp_by_expenditure_category(real_sector):
    ## National Account (current price)
    def __init__(self):
        super(current_price_gdp_by_expenditure_category, self).__init__()
        pass

    def gdp(self):
        """
        * Title: Gross domestic product at market prices
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=MNA.Q.Y.I8.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.V.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_gdp = ecb.get_data(datacode="MNA", key="Q.Y.I8.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.V.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_gdp.columns = ["Date", "EU_GDP"]
        eu_gdp["Date"] = pd.to_datetime(QtoM(eu_gdp["Date"]), format="%Y-%m-%d")
        eu_gdp = pd.merge_asof(self.daterange, eu_gdp, on="Date", direction="nearest")
        return eu_gdp

    def pfc(self):
        """
        * Title: Private final consumption 
        * URL: http://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=MNA.Q.Y.I8.W0.S1M.S1.D.P31._Z._Z._T.EUR.V.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_pfc = ecb.get_data(datacode="MNA", key="Q.Y.I8.W0.S1M.S1.D.P31._Z._Z._T.EUR.V.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pfc.columns = ["Date", "EU_PFC"]
        eu_pfc["Date"] = pd.to_datetime(QtoM(eu_pfc["Date"]), format="%Y-%m-%d")
        eu_pfc = pd.merge_asof(self.daterange, eu_pfc, on="Date", direction="nearest")
        return eu_pfc

    def gfc(self):
        """
        * Title: Government final consumption
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=MNA.Q.Y.I8.W0.S13.S1.D.P3._Z._Z._T.EUR.V.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_gfc = ecb.get_data(datacode="MNA", key="Q.Y.I8.W0.S13.S1.D.P3._Z._Z._T.EUR.V.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_gfc.columns = ["Date", "EU_GFC"]
        eu_gfc["Date"] = pd.to_datetime(QtoM(eu_gfc["Date"]), format="%Y-%m-%d")
        eu_gfc = pd.merge_asof(daterange, self.eu_gfc, on="Date", direction="nearest")
        return eu_gfc

    def gfcf(self):
        """
        * Title: Gross fixed capital formation
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=MNA.Q.Y.I8.W0.S1.S1.D.P51G.N11G._T._Z.EUR.V.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_gfcf = ecb.get_data(datacode="MNA", key="Q.Y.I8.W0.S1.S1.D.P51G.N11G._T._Z.EUR.V.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_gfcf.columns = ["Date", "EU_GFCF"]
        eu_gfcf["Date"] = pd.to_datetime(QtoM(eu_gfcf["Date"]), format="%Y-%m-%d")
        eu_gfcf = pd.merge_asof(self.daterange, eu_gfcf, on="Date", direction="nearest")
        return eu_gfcf

    def cia(self):
        """
        * Title: Changes in inventories and acquisition less disposals of valuables
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=MNA.Q.Y.I8.W0.S1.S1.D.P5M.N1MG._T._Z.EUR.V.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_cia = ecb.get_data(datacode="MNA", key="Q.Y.I8.W0.S1.S1.D.P5M.N1MG._T._Z.EUR.V.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_cia.columns = ["Date", "EU_CIA"]
        eu_cia["Date"] = pd.to_datetime(QtoM(eu_cia["Date"]), format="%Y-%m-%d")
        eu_cia = pd.merge_asof(self.daterange, eu_cia, on="Date", direction="nearest")
        return eu_cia

    def export(self):
        """
        * Title: Exports of goods and services
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=Q.Y.I8.W1.S1.S1.D.P6._Z._Z._Z.EUR.V.NN
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_export = ecb.get_data(datacode="MNA", key="Q.Y.I8.W1.S1.S1.D.P6._Z._Z._Z.EUR.V.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_export.columns = ["Date", "EU_EXPORT"]
        eu_export["Date"] = pd.to_datetime(QtoM(eu_export["Date"]), format="%Y-%m-%d")
        eu_export = pd.merge_asof(self.daterange, eu_export, on="Date", direction="nearest")

    def import_(self):
        """
        * Title: Imports of goods and services
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=Q.Y.I8.W1.S1.S1.C.P7._Z._Z._Z.EUR.V.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_import = ecb.get_data(datacode="MNA", key="Q.Y.I8.W1.S1.S1.C.P7._Z._Z._Z.EUR.V.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_import.columns = ["Date", "EU_IMPORT"]
        eu_import["Date"] = pd.to_datetime(QtoM(eu_import["Date"]), format="%Y-%m-%d")
        eu_import = pd.merge_asof(self.daterange, eu_import, on="Date", direction="nearest")
        return eu_import

class volume_gdp_by_expenditure_category_in_previous_year_price(real_sector):
    ## National Account (volume in previous year price)
    ## National Account (current price)
    def __init__(self):
        super(volume_gdp_by_expenditure_category_in_previous_year_price, self).__init__()
        pass
    
    def gdp(self):
        """
        * Title: Gross domestic product at market prices
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=MNA.Q.Y.I8.W2.S1.S1.B.B1GQ._Z._Z._Z.IX.LR.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_gdp = ecb.get_data(datacode="MNA", key="Q.Y.I8.W2.S1.S1.B.B1GQ._Z._Z._Z.IX.LR.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_gdp.columns = ["Date", "EU_GDP"]
        eu_gdp["Date"] = pd.to_datetime(QtoM(eu_gdp["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_gdp = pd.merge_asof(self.daterange, eu_gdp, on="Date", direction="nearest")
        return eu_gdp

    def pfc(self):
        """
        * Title: Private final consumption 
        * URL: http://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=MNA.Q.Y.I8.W0.S1M.S1.D.P31._Z._Z._T.IX.LR.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_pfc = ecb.get_data(datacode="MNA", key="Q.Y.I8.W0.S1M.S1.D.P31._Z._Z._T.IX.LR.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pfc.columns = ["Date", "EU_PFC"]
        eu_pfc["Date"] = pd.to_datetime(QtoM(eu_pfc["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_pfc = pd.merge_asof(self.daterange, eu_pfc, on="Date", direction="nearest")
        return eu_pfc

    def gfc(self):
        """
        * Title: Government final consumption
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=MNA.Q.Y.I8.W0.S13.S1.D.P3._Z._Z._T.IX.LR.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_gfc = ecb.get_data(datacode="MNA", key="Q.Y.I8.W0.S13.S1.D.P3._Z._Z._T.IX.LR.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_gfc.columns = ["Date", "EU_GFC"]
        eu_gfc["Date"] = pd.to_datetime(QtoM(eu_gfc["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_gfc = pd.merge_asof(self.daterange, eu_gfc, on="Date", direction="nearest")
        return eu_gfc

    def gfcf(self):
        """
        * Title: Gross fixed capital formation
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=MNA.Q.Y.I8.W0.S1.S1.D.P51G.N11G._T._Z.IX.LR.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_gfcf = ecb.get_data(datacode="MNA", key="Q.Y.I8.W0.S1.S1.D.P51G.N11G._T._Z.IX.LR.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_gfcf.columns = ["Date", "EU_GFCF"]
        eu_gfcf["Date"] = pd.to_datetime(QtoM(eu_gfcf["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_gfcf = pd.merge_asof(self.daterange, eu_gfcf, on="Date", direction="nearest")
        return eu_gfcf

    def export(self):
        """
        * Title: Exports of goods and services
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=Q.Y.I8.W1.S1.S1.D.P6._Z._Z._Z.IX.LR.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_export = ecb.get_data(datacode="MNA", key="Q.Y.I8.W1.S1.S1.D.P6._Z._Z._Z.IX.LR.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_export.columns = ["Date", "EU_EXPORT"]
        eu_export["Date"] = pd.to_datetime(QtoM(eu_export["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_export = pd.merge_asof(self.daterange, eu_export, on="Date", direction="nearest")
        return eu_gfcf

    def import_(self):
        """
        * Title: Imports of goods and services
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=Q.Y.I8.W1.S1.S1.C.P7._Z._Z._Z.IX.LR.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_import = ecb.get_data(datacode="MNA", key="Q.Y.I8.W1.S1.S1.C.P7._Z._Z._Z.IX.LR.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_import.columns = ["Date", "EU_IMPORT"]
        eu_import["Date"] = pd.to_datetime(QtoM(eu_import["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_import = pd.merge_asof(self.daterange, eu_import, on="Date", direction="nearest")
        return eu_import

    def industrial_production(self):
        """
        * Title: Industrial production for the euro area
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=132.STS.M.I8.Y.PROD.NS0020.4.000
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_industrial_production = ecb.get_data(datacode="STS", key="M.I8.Y.PROD.NS0020.4.000", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_industrial_production.columns = ["Date", "EU_INDUSTRIAL_PRODUCTION"]
        eu_industrial_production["Date"] = pd.to_datetime(QtoM(eu_industrial_production["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_industrial_production = pd.merge_asof(self.daterange, eu_industrial_production, on="Date", direction="nearest")
        return eu_industrial_production

    def employment(self):
        """
        * Title: Employment (in thousands of persons)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=ENA.Q.Y.I8.W2.S1.S1._Z.EMP._Z._T._Z.PS._Z.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_employment = ecb.get_data(datacode="ENA", key="Q.Y.I8.W2.S1.S1._Z.EMP._Z._T._Z.PS._Z.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_employment.columns = ["Date", "EU_EMPLOYMENT"]
        eu_employment["Date"] = pd.to_datetime(QtoM(eu_employment["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_employment = pd.merge_asof(self.daterange, eu_employment, on="Date", direction="nearest")
        return eu_employment

    def unemployment(self):
        """
        * Title: Unemployment (in thousands of persons)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=LFSI.M.I8.S.UNEMPL.TOTAL0.15_74.T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_unemployment = ecb.get_data(datacode="LFSI", key="M.I8.S.UNEMPL.TOTAL0.15_74.T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_unemployment.columns = ["Date", "EU_UNEMPLOYMENT"]
        eu_unemployment["Date"] = pd.to_datetime(eu_unemployment["Date"], format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        return eu_unemployment

    def unemployment_rate(self):
        """
        * Title: Unemployment Rate
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=LFSI.M.I8.S.UNEHRT.TOTAL0.15_74.T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_unemployment_rate = ecb.get_data(datacode="LFSI", key="M.I8.S.UNEHRT.TOTAL0.15_74.T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_unemployment_rate.columns = ["Date", "EU_UNEMPLOYMENT_RATE"]
        eu_unemployment_rate["Date"] = pd.to_datetime(eu_unemployment_rate["Date"], format="%Y-%m-%d")
        return eu_unemployment_rate

    def labour_cost_index(self):
        """
        * Title: Labour cost index
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=LCI.Q.I8.Y.LCI_T.BTN
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_labour_cost_index = ecb.get_data(datacode="LCI", key="Q.I8.Y.LCI_T.BTN", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_labour_cost_index.columns = ["Date", "EU_LABOUR_COST_INDEX"]
        eu_labour_cost_index["Date"] = pd.to_datetime(QtoM(eu_labour_cost_index["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_labour_cost_index = pd.merge_asof(self.daterange, eu_labour_cost_index, on="Date", direction="nearest")
        return eu_labour_cost_index

    def hicp(self):
        """
        * Title: HICP - Overall index
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=ICP.M.U2.N.000000.4.INX
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_hicp = ecb.get_data(datacode="ICP", key="M.U2.N.000000.4.INX", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_hicp.columns = ["Date", "EU_HICP"]
        eu_hicp["Date"] = pd.to_datetime(eu_hicp["Date"], format="%Y-%m-%d")
        return eu_hicp

    def ppi(self):
        """
        * Title:Industrial producer prices (excl. construction) for the euro area [PPI]
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=STS.M.I8.N.PRIN.NS0020.4.000
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_ppi = ecb.get_data(datacode="STS", key="M.I8.N.PRIN.NS0020.4.000", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_ppi.columns = ["Date", "EU_PPI"]
        eu_ppi["Date"] = pd.to_datetime(eu_ppi["Date"], format="%Y-%m-%d")
        return eu_ppi

class fiscal_sector():
    def __init__(self, startdate=startdate, enddate=enddate, daterange=daterange):
        self.startdate = startdate
        self.enddate = enddate
        self.daterange = daterange
        
class general_government_operation(fiscal_sector):
    ## National Account (current price)
    def __init__(self):
        super(general_government_operation, self).__init__()
        pass

    def revenue(self):
        """
        * Title: Government total revenue (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.Q.N.I8.W0.S13.S1.P.C.OTR._Z._Z._Z.XDC_R_B1GQ_CY._Z.S.V.CY._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_gtr = ecb.get_data(datacode="GFS", key="Q.N.I8.W0.S13.S1.P.C.OTR._Z._Z._Z.XDC_R_B1GQ_CY._Z.S.V.CY._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_gtr.columns = ["Date", "EU_GOVERNMENT_TOTAL_REVENUE"]
        eu_gtr["Date"] = pd.to_datetime(QtoM(eu_gtr["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_gtr = pd.merge_asof(self.daterange, eu_gtr, on="Date", direction="nearest")
        return eu_gtr

    def expenditure(self):
        """
        * Title: Government total expenditure (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.Q.N.I8.W0.S13.S1.P.D.OTE._Z._Z._T.XDC_R_B1GQ_CY._Z.S.V.CY._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_gte = ecb.get_data(datacode="GFS", key="Q.N.I8.W0.S13.S1.P.D.OTE._Z._Z._T.XDC_R_B1GQ_CY._Z.S.V.CY._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_gte.columns = ["Date", "EU_GOVERNMENT_TOTAL_EXPENDITURE"]
        eu_gte["Date"] = pd.to_datetime(QtoM(eu_gte["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_gte = pd.merge_asof(self.daterange, eu_gte, on="Date", direction="nearest")
        return eu_gte

    def interest_expenditure(self):
        """
        * Title: Government interest expenditure (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.Q.N.I8.W0.S13.S1.C.D.D41._Z._Z._T.XDC_R_B1GQ_CY._Z.S.V.CY._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_gie = ecb.get_data(datacode="GFS", key="Q.N.I8.W0.S13.S1.C.D.D41._Z._Z._T.XDC_R_B1GQ_CY._Z.S.V.CY._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_gie.columns = ["Date", "EU_GOVERNMENT_INTEREST_EXPENDITURE"]
        eu_gie["Date"] = pd.to_datetime(QtoM(eu_gie["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_gie = pd.merge_asof(self.daterange, eu_gie, on="Date", direction="nearest")
        return eu_gie

    def investment_expenditure(self):
        """
        * Title: Government investment expenditure (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.Q.N.I8.W0.S13.S1.N.D.P51G._Z._Z._T.XDC_R_B1GQ_CY._Z.S.V.CY._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_gie = ecb.get_data(datacode="GFS", key="Q.N.I8.W0.S13.S1.N.D.P51G._Z._Z._T.XDC_R_B1GQ_CY._Z.S.V.CY._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_gie.columns = ["Date", "EU_GOVERNMENT_INVESTMENT_EXPENDITURE"]
        eu_gie["Date"] = pd.to_datetime(QtoM(eu_gie["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_gie = pd.merge_asof(self.daterange, eu_gie, on="Date", direction="nearest")
        return eu_gie

    def balance(self):
        """
        * Title: Government deficit(-) or surplus(+) (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.Q.N.I8.W0.S13.S1._Z.B.B9._Z._Z._Z.XDC_R_B1GQ_CY._Z.S.V.CY._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_balance = ecb.get_data(datacode="GFS", key="Q.N.I8.W0.S13.S1._Z.B.B9._Z._Z._Z.XDC_R_B1GQ_CY._Z.S.V.CY._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_balance.columns = ["Date", "EU_GOVERNMENT_BALANCE"]
        eu_balance["Date"] = pd.to_datetime(QtoM(eu_balance["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_balance = pd.merge_asof(self.daterange, eu_balance, on="Date", direction="nearest")
        return eu_balance

class general_government_debt(fiscal_sector):
    ## National Account (current price)
    def __init__(self):
        super(general_government_debt, self).__init__()
        pass

    def gross_outstanding_debt_total(self):
        """
        * Title: Government debt (consolidated) (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.A.N.I8.W0.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Yearly
        """
        eu_od = ecb.get_data(datacode="GFS", key="A.N.I8.W0.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_od.columns = ["Date", "EU_GOVERNMENT_OUT_STANDING_DEBT_TOTAL"]
        eu_od["Date"] = pd.to_datetime(eu_od["Date"], format="%Y") + pd.tseries.offsets.MonthBegin(-1)
        eu_od = pd.merge_asof(self.daterange, eu_od, on="Date", direction="nearest")
        return eu_od

    def gross_outstanding_debt_in_euro(self):
        """
        * Title: Government debt denominated in national currency and euro (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.A.N.I8.W0.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ.EUR.F.V.N._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Yearly
        """
        eu_od = ecb.get_data(datacode="GFS", key="A.N.I8.W0.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ.EUR.F.V.N._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_od.columns = ["Date", "EU_GOVERNMENT_OUT_STANDING_DEBT_IN_EURO"]
        eu_od["Date"] = pd.to_datetime(eu_od["Date"], format="%Y") + pd.tseries.offsets.MonthBegin(-1)
        eu_od = pd.merge_asof(self.daterange, eu_od, on="Date", direction="nearest")
        return eu_od

    def gross_outstanding_debt_no_euro(self):
        """
        * Title: Government debt denominated in currencies other than national currency and euro (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.A.N.I8.W0.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ.XNC.F.V.N._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Yearly
        """
        eu_od = ecb.get_data(datacode="GFS", key="A.N.I8.W0.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ.XNC.F.V.N._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_od.columns = ["Date", "EU_GOVERNMENT_OUT_STANDING_DEBT_NO_EURO"]
        eu_od["Date"] = pd.to_datetime(eu_od["Date"], format="%Y") + pd.tseries.offsets.MonthBegin(-1)
        eu_od = pd.merge_asof(self.daterange, eu_od, on="Date", direction="nearest")
        return eu_od

    def gross_outstanding_debt_resident(self):
        """
        * Title: Government debt held by residents (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.A.N.I8.W2.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Yearly
        """
        eu_od = ecb.get_data(datacode="GFS", key="A.N.I8.W2.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_od.columns = ["Date", "EU_GOVERNMENT_OUT_STANDING_DEBT_RESIDENTS"]
        eu_od["Date"] = pd.to_datetime(eu_od["Date"], format="%Y") + pd.tseries.offsets.MonthBegin(-1)
        eu_od = pd.merge_asof(self.daterange, eu_od, on="Date", direction="nearest")
        return eu_od

    def gross_outstanding_debt_mfi(self):
        """
        * Title: Government debt held by monetary financial institutions (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.A.N.I8.W2.S13.S12K.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Yearly
        """
        eu_od = ecb.get_data(datacode="GFS", key="A.N.I8.W2.S13.S12K.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_od.columns = ["Date", "EU_GOVERNMENT_OUT_STANDING_DEBT_MFI"]
        eu_od["Date"] = pd.to_datetime(eu_od["Date"], format="%Y") + pd.tseries.offsets.MonthBegin(-1)
        eu_od = pd.merge_asof(self.daterange, eu_od, on="Date", direction="nearest")
        return eu_od

    def gross_outstanding_debt_non_mfi(self):
        """
        * Title: Government debt held by financial institutions other than monetary financial institutions (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.A.N.I8.W2.S13.S12P.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Yearly
        """
        eu_od = ecb.get_data(datacode="GFS", key="A.N.I8.W2.S13.S12P.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_od.columns = ["Date", "EU_GOVERNMENT_OUT_STANDING_DEBT_NON_MFI"]
        eu_od["Date"] = pd.to_datetime(eu_od["Date"], format="%Y") + pd.tseries.offsets.MonthBegin(-1)
        eu_od = pd.merge_asof(self.daterange, eu_od, on="Date", direction="nearest")
        return eu_od

    def gross_outstanding_debt_non_fin_sector(self):
        """
        * Title: Government debt held by the non-financial sectors (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.A.N.I8.W2.S13.S1U.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Yearly
        """
        eu_od = ecb.get_data(datacode="GFS", key="A.N.I8.W2.S13.S1U.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_od.columns = ["Date", "EU_GOVERNMENT_OUT_STANDING_DEBT_NON_FIN_SECTOR"]
        eu_od["Date"] = pd.to_datetime(eu_od["Date"], format="%Y") + pd.tseries.offsets.MonthBegin(-1)
        eu_od = pd.merge_asof(self.daterange, eu_od, on="Date", direction="nearest")
        return eu_od

    def gross_outstanding_debt_non_resident(self):
        """
        * Title: Government debt held by non-residents (as % of GDP)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=325.GFS.A.N.I8.W1.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Yearly
        """
        eu_od = ecb.get_data(datacode="GFS", key="A.N.I8.W1.S13.S1.C.L.LE.GD.T._Z.XDC_R_B1GQ._T.F.V.N._T", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_od.columns = ["Date", "EU_GOVERNMENT_OUT_STANDING_DEBT_NON_RESIDENT"]
        eu_od["Date"] = pd.to_datetime(eu_od["Date"], format="%Y") + pd.tseries.offsets.MonthBegin(-1)
        eu_od = pd.merge_asof(self.daterange, eu_od, on="Date", direction="nearest")
        return eu_od

class financial_sector():
    def __init__(self, startdate=startdate, enddate=enddate, daterange=daterange):
        self.startdate = startdate
        self.enddate = enddate
        self.daterange = daterange
        
class analytical_accounts_of_the_banking_sector(financial_sector):
    ## National Account (current price)
    def __init__(self):
        super(analytical_accounts_of_the_banking_sector, self).__init__()
        pass

    def monetary_aggrate_m1(self):
        """
        * Title: Monetary aggregate M1 vis-a-vis euro area non-MFI excl. central gov. reported by MFI & central gov. & post office giro Inst. in the euro area (stock)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=BSI.M.U2.Y.V.M10.X.1.U2.2300.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_m1 = ecb.get_data(datacode="BSI", key="M.U2.Y.V.M30.X.1.U2.2300.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_m1.columns = ["Date", "EU_MONETARY_AGGRATE_M3"]
        eu_m1["Date"] = pd.to_datetime(eu_m1["Date"], format="%Y-%m-%d")
        return eu_m1

    def monetary_aggrate_m2(self):
        """
        * Title: Monetary aggregate M2 vis-a-vis euro area non-MFI excl. central gov. reported by MFI & central gov. & post office giro Inst. in the euro area (stock)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=BSI.M.U2.Y.V.M10.X.1.U2.2300.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_m2 = ecb.get_data(datacode="BSI", key="M.U2.Y.V.M20.X.1.U2.2300.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_m2.columns = ["Date", "EU_MONETARY_AGGRATE_M3"]
        eu_m2["Date"] = pd.to_datetime(eu_m2["Date"], format="%Y-%m-%d")
        return eu_m2

    def monetary_aggrate_m3(self):
        """
        * Title: Monetary aggregate M3 vis-a-vis euro area non-MFI excl. central gov. reported by MFI & central gov. & post office giro Inst. in the euro area (stock)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=BSI.M.U2.Y.V.M30.X.1.U2.2300.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_m3 = ecb.get_data(datacode="BSI", key="M.U2.Y.V.M30.X.1.U2.2300.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_m3.columns = ["Date", "EU_MONETARY_AGGRATE_M3"]
        eu_m3["Date"] = pd.to_datetime(eu_m3["Date"], format="%Y-%m-%d")
        return eu_m3

    def domestic_credit(self):
        """
        * Title: Total loans and securities vis-a-vis euro area non-MFI reported by MFI in the euro area (stock)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=BSI.M.U2.Y.U.AT2.A.1.U2.2000.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_dc = ecb.get_data(datacode="BSI", key="M.U2.Y.U.AT2.A.1.U2.2000.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_dc.columns = ["Date", "EU_DOMESTIC_CREDIT"]
        eu_dc["Date"] = pd.to_datetime(eu_dc["Date"], format="%Y-%m-%d")
        return eu_dc

    def credit_general_government(self):
        """
        * Title: Total loans and securities vis-a-vis euro area General Government reported by MFI in the euro area (stock)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=BSI.M.U2.Y.U.AT2.A.1.U2.2100.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_dc = ecb.get_data(datacode="BSI", key="M.U2.Y.U.AT2.A.1.U2.2100.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_dc.columns = ["Date", "EU_GOVERNMENT_CREDIT"]
        eu_dc["Date"] = pd.to_datetime(eu_dc["Date"], format="%Y-%m-%d")
        return eu_dc

    def credit_general_other_resident(self):
        """
        * Title: Total loans and securities vis-a-vis euro area non-MFI excl. general gov. reported by MFI in the euro area (stock)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=BSI.M.U2.Y.U.AT2.A.1.U2.2200.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_dc = ecb.get_data(datacode="BSI", key="M.U2.Y.U.AT2.A.1.U2.2200.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_dc.columns = ["Date", "EU_OTHER_RESIDENT_CREDIT"]
        eu_dc["Date"] = pd.to_datetime(eu_dc["Date"], format="%Y-%m-%d")
        return eu_dc

    def external_assets(self):
        """
        * Title: External assets reported by MFI in the euro area (stock)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=BSI.M.U2.Y.U.AXG.A.1.U4.0000.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_ea = ecb.get_data(datacode="BSI", key="M.U2.Y.U.AXG.A.1.U4.0000.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_ea.columns = ["Date", "EU_EXTERNAL_ASSETS"]
        eu_ea["Date"] = pd.to_datetime(eu_ea["Date"], format="%Y-%m-%d")
        return eu_ea

    def external_liabilities(self):
        """
        * Title: External liabilities reported by MFI in the euro area (stock)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=BSI.M.U2.Y.U.LXG.A.1.U4.0000.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_el = ecb.get_data(datacode="BSI", key="M.U2.Y.U.LXG.A.1.U4.0000.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_el.columns = ["Date", "EU_EXTERNAL_LIABILITIES"]
        eu_el["Date"] = pd.to_datetime(eu_el["Date"], format="%Y-%m-%d")
        return eu_el

class analytical_accounts_of_the_central_banks(financial_sector):
    ## National Account (current price)
    def __init__(self):
        super(analytical_accounts_of_the_banking_sector, self).__init__()
        pass

    def currency_in_circulation(self):
        """
        * Title: Currency in circulation reported by Eurosystem in the euro area (stock)
        * URL:https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=117.BSI.M.U2.N.C.L10.X.1.Z5.0000.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_cc = ecb.get_data(datacode="BSI", key="M.U2.N.C.L10.X.1.Z5.0000.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_cc.columns = ["Date", "EU_CURRENCY_IN_CIRCULATION"]
        eu_cc["Date"] = pd.to_datetime(eu_cc["Date"], format="%Y-%m-%d")
        return eu_cc

    def deposits_at_eurosystem_mfi(self):
        """
        * Title: Deposit liabilities vis-a-vis euro area MFI reported by Eurosystem in the euro area (stock)
        * URL:https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=117.BSI.M.U2.N.C.L20.A.1.U2.1000.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_cc = ecb.get_data(datacode="BSI", key="M.U2.N.C.L20.A.1.U2.1000.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_cc.columns = ["Date", "EU_DEPOSITS_AT_EUROSYSTEM_MFI"]
        eu_cc["Date"] = pd.to_datetime(eu_cc["Date"], format="%Y-%m-%d")
        return eu_cc

    def credit(self):
        """
        * Title: Total loans and securities vis-a-vis euro area non-MFI reported by Eurosystem in the euro area (stock)
        * URL:https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=117.BSI.M.U2.N.C.AT2.A.1.U2.2000.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_cc = ecb.get_data(datacode="BSI", key="M.U2.N.C.AT2.A.1.U2.2000.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_cc.columns = ["Date", "EU_CREDIT"]
        eu_cc["Date"] = pd.to_datetime(eu_cc["Date"], format="%Y-%m-%d")
        return eu_cc

    def credit_to_general_governemnt(self):
        """
        * Title: Total loans and securities vis-a-vis euro area non-MFI reported by Eurosystem in the euro area (stock)
        * URL:https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=117.BSI.M.U2.N.C.AT2.A.1.U2.2100.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_cc = ecb.get_data(datacode="BSI", key="M.U2.N.C.AT2.A.1.U2.2100.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_cc.columns = ["Date", "EU_CREDIT_TO_GENERAL_GOVERNMENT"]
        eu_cc["Date"] = pd.to_datetime(eu_cc["Date"], format="%Y-%m-%d")
        return eu_cc

    def credit_to_other_resident_sector(self):
        """
        * Title: Total loans and securities vis-a-vis euro area non-MFI reported by Eurosystem in the euro area (stock)
        * URL:https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=117.BSI.M.U2.N.C.AT2.A.1.U2.2200.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_cc = ecb.get_data(datacode="BSI", key="M.U2.N.C.AT2.A.1.U2.2200.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_cc.columns = ["Date", "EU_CREDIT_TO_OTHER_RESIDENT"]
        eu_cc["Date"] = pd.to_datetime(eu_cc["Date"], format="%Y-%m-%d")
        return eu_cc

    def external_assets(self):
        """
        * Title: External assets reported by Eurosystem in the euro area (stock)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=BSI.M.U2.N.C.AXG.A.1.U4.0000.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_ea = ecb.get_data(datacode="BSI", key="M.U2.N.C.AXG.A.1.U4.0000.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_ea.columns = ["Date", "EU_EXTERNAL_ASSETS"]
        eu_ea["Date"] = pd.to_datetime(eu_ea["Date"], format="%Y-%m-%d")
        return eu_ea

    def external_liabilities(self):
        """
        * Title: External liabilities reported by Eurosystem in the euro area (stock)
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=BSI.M.U2.N.C.LXG.A.1.U4.0000.Z01.E
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_el = ecb.get_data(datacode="BSI", key="M.U2.N.C.LXG.A.1.U4.0000.Z01.E", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_el.columns = ["Date", "EU_EXTERNAL_LIABILITIES"]
        eu_el["Date"] = pd.to_datetime(eu_el["Date"], format="%Y-%m-%d")
        return eu_el

class interest_rate(financial_sector):
    ## National Account (current price)
    def __init__(self):
        super(interest_rate, self).__init__()
        pass

    def one_year_interbank(self):
        """
        * Title: Euribor 1-year - Historical close, average of observations through period
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=143.FM.M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_el = ecb.get_data(datacode="FM", key="M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_el.columns = ["Date", "EU_ONE_YEAR_INTERBANK_RATE"]
        eu_el["Date"] = pd.to_datetime(eu_el["Date"], format="%Y-%m-%d")
        return eu_el

    def ten_year_government_banchmar_bond_yild(self):
        """
        * Title: Euro area 10-year Government Benchmark bond yield - Yield
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=143.FM.M.U2.EUR.4F.BB.U2_10Y.YLD
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_el = ecb.get_data(datacode="FM", key="M.U2.EUR.4F.BB.U2_10Y.YLD", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_el.columns = ["Date", "EU_TEN_YEART_BOND_RATE"]
        eu_el["Date"] = pd.to_datetime(eu_el["Date"], format="%Y-%m-%d")
        return eu_el

class external_sector():
    def __init__(self, startdate=startdate, enddate=enddate, daterange=daterange):
        self.startdate = startdate
        self.enddate = enddate
        self.daterange = daterange
        
class balance_of_payments(external_sector):
    ## National Account (current price)
    def __init__(self):
        super(balance_of_payments, self).__init__()
        pass

    def net_current_account(self):
        """
        * Title: Current account
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.Y.I8.W1.S1.S1.T.B.CA._Z._Z._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_ca = ecb.get_data(datacode="BP6", key="M.Y.I8.W1.S1.S1.T.B.CA._Z._Z._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_ca.columns = ["Date", "EU_CURRENT_ACCOUNT"]
        eu_ca["Date"] = pd.to_datetime(eu_ca["Date"], format="%Y-%m-%d")
        return eu_ca

    def exports_goods(self):
        """
        * Title: Goods
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.Y.I8.W1.S1.S1.T.C.G._Z._Z._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_eg = ecb.get_data(datacode="BP6", key="M.Y.I8.W1.S1.S1.T.C.G._Z._Z._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_eg.columns = ["Date", "EU_EXPORT_GOODS"]
        eu_eg["Date"] = pd.to_datetime(eu_eg["Date"], format="%Y-%m-%d")
        return eu_ca

    def exports_services(self):
        """
        * Title: Services
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.Y.I8.W1.S1.S1.T.C.S._Z._Z._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_eg = ecb.get_data(datacode="BP6", key="M.Y.I8.W1.S1.S1.T.C.S._Z._Z._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_es.columns = ["Date", "EU_EXPORT_SERVICES"]
        eu_es["Date"] = pd.to_datetime(eu_es["Date"], format="%Y-%m-%d")
        return eu_es

    def imports_goods(self):
        """
        * Title: Goods
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.Y.I8.W1.S1.S1.T.D.G._Z._Z._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_ig = ecb.get_data(datacode="BP6", key="M.Y.I8.W1.S1.S1.T.D.G._Z._Z._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_ig.columns = ["Date", "EU_IMPORT_GOODS"]
        eu_ig["Date"] = pd.to_datetime(eu_ig["Date"], format="%Y-%m-%d")
        return eu_ca

    def import_services(self):
        """
        * Title: Services
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.Y.I8.W1.S1.S1.T.D.S._Z._Z._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_is = ecb.get_data(datacode="BP6", key="M.Y.I8.W1.S1.S1.T.D.S._Z._Z._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_is.columns = ["Date", "EU_IMPORT_SERVICES"]
        eu_is["Date"] = pd.to_datetime(eu_is["Date"], format="%Y-%m-%d")
        return eu_is

    def net_primary_income(self):
        """
        * Title: Primary income
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.Y.I8.W1.S1.S1.T.B.IN1._Z._Z._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_npi = ecb.get_data(datacode="BP6", key="M.Y.I8.W1.S1.S1.T.B.IN1._Z._Z._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_npi.columns = ["Date", "EU_NET_PRIMARY_INCOME"]
        eu_npi["Date"] = pd.to_datetime(eu_npi["Date"], format="%Y-%m-%d")
        return eu_npi

    def net_secondary_income(self):
        """
        * Title: Secondary income
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.Y.I8.W1.S1.S1.T.B.IN2._Z._Z._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_nsi = ecb.get_data(datacode="BP6", key="M.Y.I8.W1.S1.S1.T.B.IN2._Z._Z._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_nsi.columns = ["Date", "EU_NET_SECONDARY_INCOME"]
        eu_nsi["Date"] = pd.to_datetime(eu_nsi["Date"], format="%Y-%m-%d")
        return eu_nsi

    def net_capital_account(self):
        """
        * Title: Capitial account
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.N.I8.W1.S1.S1.T.B.KA._Z._Z._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_nca = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S1.S1.T.B.KA._Z._Z._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_nca.columns = ["Date", "EU_NET_CAPTIAL_ACCOUNT"]
        eu_nca["Date"] = pd.to_datetime(eu_nca["Date"], format="%Y-%m-%d")
        return eu_nca

    def net_financial_account(self):
        """
        * Title: Total financial assets/liabilities
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.N.I8.W1.S1.S1.T.N.FA._T.F._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_nfa = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S1.S1.T.N.FA._T.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_nfa.columns = ["Date", "EU_NET_FINANCIAL_ACCOUNT"]
        eu_nfa["Date"] = pd.to_datetime(eu_nfa["Date"], format="%Y-%m-%d")
        return eu_nfa

    def direct_investment(self):
        """
        * Title: Direct Investment, Total financial assets/liabilities
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.N.I8.W1.S1.S1.T.N.FA.D.F._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_di = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S1.S1.T.N.FA.D.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_dia = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S1.S1.T.A.FA.D.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_dil = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S1.S1.T.L.FA.D.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_di.columns = ["Date", "EU_DIRECT_INVESTMENT"]
        eu_di["Date"] = pd.to_datetime(eu_di["Date"], format="%Y-%m-%d")
        eu_di["EU_DIRECT_INVESTMENT_ASSETS"],  eu_di["EU_DIRECT_INVESTMENT_LIABILITIES"] = eu_dia["OBS_VALUE"], eu_dil["OBS_VALUE"]
        return eu_di

    def porfolio_investment(self):
        """
        * Title: Portfolio Investment, Total financial assets/liabilities
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.N.I8.W1.S1.S1.T.N.FA.P.F._Z.EUR._T.M.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_pi = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S1.S1.T.N.FA.P.F._Z.EUR._T.M.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pia = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S1.S1.T.A.FA.P.F._Z.EUR._T.M.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pil = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S1.S1.T.L.FA.P.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pi.columns = ["Date", "EU_PORFOLIO_INVESTMENT"]
        eu_pi["Date"] = pd.to_datetime(eu_pi["Date"], format="%Y-%m-%d")
        eu_pi["EU_PORFOLIO_INVESTMENT_ASSETS"],  eu_pi["EU_PORFOLIO_INVESTMENT_LIABILITIES"] = eu_pia["OBS_VALUE"], eu_pil["OBS_VALUE"]
        return eu_pi

    def other_investment(self):
        """
        * Title: Other Investment, Total financial assets/liabilities
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.N.I8.W1.S1.S1.T.N.FA.O.F._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_pi = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S1.S1.T.N.FA.O.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pia = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S1.S1.T.A.FA.O.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pil = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S1.S1.T.L.FA.O.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pi.columns = ["Date", "EU_OTHER_INVESTMENT"]
        eu_pi["Date"] = pd.to_datetime(eu_pi["Date"], format="%Y-%m-%d")
        eu_pi["EU_OTHER_INVESTMENT_ASSETS"],  eu_pi["EU_OTHER_INVESTMENT_LIABILITIES"] = eu_pia["OBS_VALUE"], eu_pil["OBS_VALUE"]
        return eu_pi

    def financial_derivatives(self):
        """
        * Title: Financial Derivatives and Employee Stock Options, Financial derivatives and employee stock options
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_nfa = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_nfa.columns = ["Date", "EU_FINANCIAL_DERIVATIVES"]
        eu_nfa["Date"] = pd.to_datetime(eu_nfa["Date"], format="%Y-%m-%d")
        return eu_nfa

    def reserve_assets(self):
        """
        * Title: Reserve Assets, Total financial assets/liabilities
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.M.N.I8.W1.S121.S1.T.A.FA.R.F._Z.EUR.X1._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_nfa = ecb.get_data(datacode="BP6", key="M.N.I8.W1.S121.S1.T.A.FA.R.F._Z.EUR.X1._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_nfa.columns = ["Date", "EU_RESERVE_ASSETS"]
        eu_nfa["Date"] = pd.to_datetime(eu_nfa["Date"], format="%Y-%m-%d")
        return eu_nfa

class international_reserves_and_foreign_currency_liquidity(external_sector):
    ## National Account (current price)
    def __init__(self):
        super(balance_of_payments, self).__init__()
        pass

    def official_reserve_assets(self):
        """
        * Title: Official reserve assets
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=340.RA6.M.N.U2.W1.S121.S1.LE.A.FA.R.F._Z.EUR.X1._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_ora = ecb.get_data(datacode="RA6", key="M.N.U2.W1.S121.S1.LE.A.FA.R.F._Z.EUR.X1._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_ora.columns = ["Date", "EU_OFFICIAL_RESERVE_ASSETS"]
        eu_ora["Date"] = pd.to_datetime(eu_ora["Date"], format="%Y-%m-%d")
        return eu_ora

    def monetary_gold(self):
        """
        * Title: Monetary gold
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=340.RA6.M.N.U2.W1.S121.S1.LE.A.FA.R.F11._Z.EUR.XAU.M.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_mg = ecb.get_data(datacode="RA6", key="M.N.U2.W1.S121.S1.LE.A.FA.R.F11._Z.EUR.XAU.M.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_mg.columns = ["Date", "EU_MONETARY_GOLD"]
        eu_mg["Date"] = pd.to_datetime(eu_mg["Date"], format="%Y-%m-%d")
        return eu_mg

    def imf_reserve_position(self):
        """
        * Title: Reserve position in the IMF
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=340.RA6.M.N.U2.1C.S121.S121.LE.A.FA.R.FK._Z.EUR.XDR.M.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_img_rp = ecb.get_data(datacode="RA6", key="M.N.U2.1C.S121.S121.LE.A.FA.R.FK._Z.EUR.XDR.M.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_img_rp.columns = ["Date", "EU_IMF_RESERVE_POSITION"]
        eu_img_rp["Date"] = pd.to_datetime(eu_img_rp["Date"], format="%Y-%m-%d")
        return eu_img_rp

    def sdr(self):
        """
        * Title: Reserve position in the IMF
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=340.RA6.M.N.U2.W1.S121.S1N.LE.A.FA.R.F12.T.EUR.XDR.M.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_img_rp = ecb.get_data(datacode="RA6", key="M.N.U2.W1.S121.S1N.LE.A.FA.R.F12.T.EUR.XDR.M.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_img_rp.columns = ["Date", "EU_SDR"]
        eu_img_rp["Date"] = pd.to_datetime(eu_img_rp["Date"], format="%Y-%m-%d")
        return eu_img_rp

    def other_reserve_assets(self):
        """
        * Title: Other reserve assets
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=340.RA6.M.N.U2.W1.S121.S1.LE.A.FA.R.FR2._Z.EUR.X1._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_img_rp = ecb.get_data(datacode="RA6", key="M.N.U2.W1.S121.S1.LE.A.FA.R.FR2._Z.EUR.X1._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_img_rp.columns = ["Date", "EU_OTHER_RESERVE_ASSETS"]
        eu_img_rp["Date"] = pd.to_datetime(eu_img_rp["Date"], format="%Y-%m-%d")
        return eu_img_rp

    def other_foreign_currency_assets(self):
        """
        * Title: Other foreign currency assets (not included in reserve assets)
        * URL: http://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=340.RA6.M.N.U2.W0.S121.S1.LE.A.FA.RT.F._Z.EUR.X1._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_img_rp = ecb.get_data(datacode="RA6", key="M.N.U2.W0.S121.S1.LE.A.FA.RT.F._Z.EUR.X1._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_img_rp.columns = ["Date", "EU_FOREIGN_CURRENCY_ASSETS"]
        eu_img_rp["Date"] = pd.to_datetime(eu_img_rp["Date"], format="%Y-%m-%d")
        return eu_img_rp

    def predeterminated_short_term_net_drains_on_foreign_currency_assets(self):
        """
        * Title: Not applicable, Total financial assets/liabilities
        * URL: http://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=340.RA6.M.N.U2.W0.S121.S1.FP.FN._Z.RT.F.TS.EUR.X1.N.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_img_rp = ecb.get_data(datacode="RA6", key="M.N.U2.W0.S121.S1.FP.FN._Z.RT.F.TS.EUR.X1.N.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_img_rp.columns = ["Date", "EU_TOTAL_FINANCIAL_ASSETS"]
        eu_img_rp["Date"] = pd.to_datetime(eu_img_rp["Date"], format="%Y-%m-%d")
        return eu_img_rp

class merchandise_trade(external_sector):
    ## National Account (current price)
    def __init__(self):
        super(merchandise_trade, self).__init__()
        pass

    def merchandise_trade(self):
        """
        * Title: Total trade, Value (Community concept) (Export/Import)
        * URL1: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=133.TRD.M.I8.Y.X.TTT.J8.4.VAL
        * URL2: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=133.TRD.M.I8.Y.M.TTT.J8.4.VAL
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Monthly
        """
        eu_mte = ecb.get_data(datacode="TRD", key="M.I8.Y.X.TTT.J8.4.VAL", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_mti = ecb.get_data(datacode="TRD", key="M.I8.Y.M.TTT.J8.4.VAL", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_mte.columns = ["Date", "EU_MERCHANDISE_TRADE_EXPORT"]
        eu_mte["Date"] = pd.to_datetime(eu_mte["Date"], format="%Y-%m-%d")
        eu_mte["EU_MERCHANDISE_TRADE_IMPORT"] = eu_mti["OBS_VALUE"]
        return eu_mte

class international_investment_position(external_sector):
    ## National Account (current price)
    def __init__(self):
        super(international_investment_position, self).__init__()
        pass

    def total_net_international_investment_position(self):
        """
        * Title: Total financial assets/liabilities
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.Q.N.I8.W1.S1.S1.LE.N.FA._T.F._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_tniip = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.N.FA._T.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_tniip.columns = ["Date", "EU_TOTAL_FINANCIAL_ASSETS"]
        eu_tniip["Date"] = pd.to_datetime(QtoM(eu_tniip["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        return eu_tniip

    def direct_investment(self):
        """
        * Title: Direct Investment, Total financial assets/liabilities
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.Q.N.I8.W1.S1.S1.LE.N.FA.D.F._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_di = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.N.FA.D.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_dia = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.A.FA.D.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_dil = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.L.FA.D.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_di.columns = ["Date", "EU_DIRECT_INVESTMENT"]
        eu_dia.columns = ["Date", "EU_DIRECT_INVESTMENT_ASSETS"]
        eu_dil.columns = ["Date", "EU_DIRECT_INVESTMENT_LIABILITIES"]
        eu_di["Date"] = pd.to_datetime(QtoM(eu_di["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_dia["Date"] = pd.to_datetime(QtoM(eu_dia["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_dil["Date"] = pd.to_datetime(QtoM(eu_dil["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_di = pd.merge_asof(eu_di, eu_dia, on="Date")
        eu_di = pd.merge_asof(eu_di, eu_dil, on="Date")
        return eu_di

    def portfolio_investment(self):
        """
        * Title: Direct Investment, Total financial assets/liabilities
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.Q.N.I8.W1.S1.S1.LE.N.FA.P.F._Z.EUR._T.M.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_pi = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.N.FA.P.F._Z.EUR._T.M.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pia = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.A.FA.P.F5._Z.EUR._T.M.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pil = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.L.FA.P.F5._Z.EUR._T.M.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pida = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.A.FA.P.F3.T.EUR._T.M.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pidl = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.L.FA.P.F3.T.EUR._T.M.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_pi.columns = ["Date", "EU_PORTFOLIO_INVESTMENT"]
        eu_pia.columns = ["Date", "EU_EQUITY_AND_INVESTMENT_FUND_ASSETS"]
        eu_pil.columns = ["Date", "EU_EQUITY_AND_INVESTMENT_FUND_LIABILITIES"]
        eu_pida.columns = ["Date", "EU_DEBT_SECURITIES_aSSETS"]
        eu_pidl.columns = ["Date", "EU_DEBT_SECURITIES_LIABILITIES"]
        eu_pi["Date"] = pd.to_datetime(QtoM(eu_pi["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_pia["Date"] = pd.to_datetime(QtoM(eu_pia["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_pil["Date"] = pd.to_datetime(QtoM(eu_pil["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_pida["Date"] = pd.to_datetime(QtoM(eu_pil["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_pidl["Date"] = pd.to_datetime(QtoM(eu_pil["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_pi = pd.merge_asof(eu_pi, eu_pia, on="Date")
        eu_pi = pd.merge_asof(eu_pi, eu_pil, on="Date")
        eu_pi = pd.merge_asof(eu_pi, eu_pida, on="Date")
        eu_pi = pd.merge_asof(eu_pi, eu_pidl, on="Date")
        return eu_pi

    def other_investment(self):
        """
        * Title: Other Investment, Total financial assets/liabilities
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.Q.N.I8.W1.S1.S1.LE.N.FA.O.F._Z.EUR._T._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_oi = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.N.FA.O.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_oia = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.A.FA.O.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_oil = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.L.FA.O.F._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_oi.columns = ["Date", "EU_DIRECT_INVESTMENT"]
        eu_oia.columns = ["Date", "EU_DIRECT_INVESTMENT_ASSETS"]
        eu_oil.columns = ["Date", "EU_DIRECT_INVESTMENT_LIABILITIES"]
        eu_oi["Date"] = pd.to_datetime(QtoM(eu_oi["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_oia["Date"] = pd.to_datetime(QtoM(eu_oia["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_oil["Date"] = pd.to_datetime(QtoM(eu_oil["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        eu_oi = pd.merge_asof(eu_oi, eu_oia, on="Date")
        eu_oi = pd.merge_asof(eu_oi, eu_oil, on="Date")
        return eu_di

    def reserve_assetsc(self):
        """
        * Title: Reserve Assets, Total financial assets/liabilities
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.Q.N.I8.W1.S121.S1.LE.A.FA.R.F._Z.EUR.X1._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_ra = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S121.S1.LE.A.FA.R.F._Z.EUR.X1._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_ra.columns = ["Date", "EU_OTHER_INVESTMENT_ASSETS"]
        eu_ra["Date"] = pd.to_datetime(QtoM(eu_ra["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        return eu_ra

    def gross_external_debt(self):
        """
        * Title: Gross external debt
        * URL: https://sdw.ecb.europa.eu/quickview.do?SERIES_KEY=338.BP6.Q.N.I8.W1.S121.S1.LE.A.FA.R.F._Z.EUR.X1._X.N
        * Reference area: Euro area 19 (fixed composition) as of 1 January 2015 (I8)
        * Frequency: Quarterly
        """
        eu_ged = ecb.get_data(datacode="BP6", key="Q.N.I8.W1.S1.S1.LE.L.FA._T.FGED._Z.EUR._T._X.N", startdate=self.startdate, enddate=self.enddate)[["TIME_PERIOD", "OBS_VALUE"]]
        eu_ged.columns = ["Date", "EU_GROSS_EXTERNAL_DEBT"]
        eu_ged["Date"] = pd.to_datetime(QtoM(eu_ged["Date"]), format="%Y-%m") + pd.tseries.offsets.MonthBegin(-1)
        return eu_ged

if __name__ == "__main__":
    data, name_list = CPI_monthly()

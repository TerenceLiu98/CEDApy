import pandas as pd
import numpy as np
import re
import demjson
import requests
from fake_useragent import UserAgent

# TODO need add comments

url = {
    "eastmoney": "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
}

def gdp_quarterly():
    """
    ABS: absolute value (per 100 million CNY)
    YoY: year on year growth
    Data source: http://data.eastmoney.com/cjsj/gdp.html
    """
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable7519513",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "20",
        "_": "1622020352668"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Absolute_Value",
        "YoY_Rate",
        "Primary_Industry_ABS",
        "Primary_Industry_YoY_Rate",
        "Secondary_Industry_ABS",
        "Secondary_Industry_YoY_Rate",
        "Tertiary_Industry_ABS",
        "Tertiary_Industry_YoY_Rate",
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df["Absolute_Value"] = df["Absolute_Value"].astype(float)
    df["Secondary_Industry_ABS"] = df["Secondary_Industry_ABS"].astype(float)
    df["Tertiary_Industry_ABS"] = df["Tertiary_Industry_ABS"].astype(float)
    df["Absolute_Value"] = df["Absolute_Value"].astype(float)
    df["YoY_Rate"] = df["YoY_Rate"].astype(float) / 100
    df["Secondary_Industry_YoY_Rate"] = df["Secondary_Industry_YoY_Rate"].astype(
        float) / 100
    df["Tertiary_Industry_YoY_Rate"] = df["Tertiary_Industry_YoY_Rate"].astype(
        float) / 100
    return df


def ppi_monthly():
    """
    ABS: absolute value (per 100 million CNY)
    YoY: year on year growth
    Accum: Accumulation
    Data source: http://data.eastmoney.com/cjsj/ppi.html
    """
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable9051497",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "22",
        "_": "1622047940401"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "Current_Month_YoY_Rate",
        "Current_Month_Accum"
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df["Current_Month"] = df["Current_Month"].astype(float)
    df["Current_Month_YoY_Rate"] = df["Current_Month_YoY_Rate"].astype(
        float) / 100
    df["Current_Month_Accum"] = df["Current_Month_Accum"].astype(float)
    return df


def cpi_monthly():
    """
    Accum: Accumulation
    YoY: year on year growth
    MoM: month on month growth
    Data source: http://data.eastmoney.com/cjsj/cpi.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable2790750",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "19",
        "_": "1622020352668"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Notion_Monthly",
        "Notion_YoY_Rate",
        "Notion_MoM_Rate",
        "Notion_Accum",
        "Urban_Monthly",
        "Urban_YoY_Rate",
        "Urban_MoM_Rate",
        "Urban_Accum",
        "Rural_Monthly",
        "Rural_YoY_Rate",
        "Rural_MoM_Rate",
        "Rural_Accum",
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Notion_Monthly",
        "Notion_Accum",
        "Urban_Monthly",
        "Urban_Accum",
        "Rural_Monthly",
        "Rural_Accum"]] = df[["Notion_Monthly",
                              "Notion_Accum",
                              "Urban_Monthly",
                              "Urban_Accum",
                              "Rural_Monthly",
                              "Rural_Accum"]].astype(float)
    df[["Notion_YoY_Rate",
        "Notion_MoM_Rate",
        "Urban_YoY_Rate",
        "Urban_MoM_Rate",
        "Rural_YoY_Rate",
        "Rural_MoM_Rate"]] = df[["Notion_YoY_Rate",
                                 "Notion_MoM_Rate",
                                 "Urban_YoY_Rate",
                                 "Urban_MoM_Rate",
                                 "Rural_YoY_Rate",
                                 "Rural_MoM_Rate"]].astype(float) / 100
    return df


def pmi_monthly():
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    Data Source: http://data.eastmoney.com/cjsj/pmi.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable4515395",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "2",
        "ps": "200",
        "mkt": "21",
        "_": "162202151821"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Man_Industry_Index",
        "Man_Index_YoY_Rate",
        "Non-Man_Industry_Index",
        "Non-Man_Index_YoY_Rate",
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Man_Industry_Index", "Non-Man_Industry_Index"]] = \
        df[["Man_Industry_Index", "Non-Man_Industry_Index"]].astype(float)
    df[["Man_Index_YoY_Rate", "Non-Man_Index_YoY_Rate"]] = \
        df[["Man_Index_YoY_Rate", "Non-Man_Index_YoY_Rate"]].astype(float) / 100
    return df


def fai_monthly():  # fix asset investment
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    Data Source: http://data.eastmoney.com/cjsj/gdzctz.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable607120",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "12",
        "_": "1622021790947"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY_Rate",
        "MoM_Rate",
        "Current_Year_Accum"
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Current_Month", "Current_Year_Accum"]] = \
        df[["Current_Month", "Current_Year_Accum"]].astype(float)
    df[["YoY_Rate", "MoM_Rate"]] = \
        df[["YoY_Rate", "MoM_Rate"]].astype(float) / 100
    return df


def hi_old_monthly():  # house index old version (2008-2010)
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    Data Source: http://data.eastmoney.com/cjsj/house.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable1895714",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "10",
        "_": "1622022794457"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Housing_Prosperity_Index",
        "HPI_YoY_Rate",
        "Land_Development_Area_Index",
        "LDAI_YoY_Rate",
        "Sales_Price_Index",
        "SPI_YoY_Rate"
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Housing_Prosperity_Index",
        "Land_Development_Area_Index",
        "Sales_Price_Index"]] = df[["Housing_Prosperity_Index",
                                    "Land_Development_Area_Index",
                                    "Sales_Price_Index"]].astype(float)
    df[["HPI_YoY_Rate", "LDAI_YoY_Rate", "SPI_YoY_Rate"]] = \
        df[["HPI_YoY_Rate", "LDAI_YoY_Rate", "SPI_YoY_Rate"]].astype(float) / 100
    return df

# mkt=1&stat=2&city1=%E5%B9%BF%E5%B7%9E&city2=%E4%B8%8A%E6%B5%B7


# newly built commercial housing &  second-hand commercial housing
def hi_new_monthly(city1: str, city2: str):
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    Data Source: http://data.eastmoney.com/cjsj/newhouse.html
    """
    tmp_url = "http://data.eastmoney.com/dataapi/cjsj/getnewhousechartdata?"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params_nbch_MoM = {
        "mkt": "1",
        "stat": "2",
        "city1": "{}".format(city1),
        "city2": "{}".format(city2)
    }
    request_params_shch_MoM = {
        "mkt": "1",
        "stat": "3",
        "city1": "{}".format(city1),
        "city2": "{}".format(city2)
    }
    r_nbch_MoM = requests.get(
        tmp_url,
        params=request_params_nbch_MoM,
        headers=request_header)
    r_shch_MoM = requests.get(
        tmp_url,
        params=request_params_shch_MoM,
        headers=request_header)
    data_text_nbch_MoM = r_nbch_MoM.text
    data_text_shch_MoM = r_shch_MoM.text
    data_json_nbch_MoM = demjson.decode(data_text_nbch_MoM)
    data_json_shch_MoM = demjson.decode(data_text_shch_MoM)
    date_nbch = data_json_nbch_MoM['chart']['series']['value']
    data1_nbch_MoM = data_json_nbch_MoM['chart']['graphs']['graph'][0]['value']
    data2_nbch_MoM = data_json_nbch_MoM['chart']['graphs']['graph'][1]['value']
    data1_shch_MoM = data_json_shch_MoM['chart']['graphs']['graph'][0]['value']
    data2_shch_MoM = data_json_shch_MoM['chart']['graphs']['graph'][1]['value']
    df_MoM = pd.DataFrame({"Date": date_nbch,
                           "City1_nbch_MoM": data1_nbch_MoM,
                           "City1_shch_MoM": data1_shch_MoM,
                           "City2_nbch_MoM": data2_nbch_MoM,
                           "City2_shch_MoM": data2_shch_MoM})
    df_MoM["Date"] = pd.to_datetime(df_MoM["Date"], format="%m/%d/%Y")

    request_params_nbch_YoY = {
        "mkt": "2",
        "stat": "2",
        "city1": "{}".format(city1),
        "city2": "{}".format(city2)
    }
    request_params_shch_YoY = {
        "mkt": "2",
        "stat": "3",
        "city1": "{}".format(city1),
        "city2": "{}".format(city2)
    }
    r_nbch_YoY = requests.get(
        tmp_url,
        params=request_params_nbch_YoY,
        headers=request_header)
    r_shch_YoY = requests.get(
        tmp_url,
        params=request_params_shch_YoY,
        headers=request_header)
    data_text_nbch_YoY = r_nbch_YoY.text
    data_text_shch_YoY = r_shch_YoY.text
    data_json_nbch_YoY = demjson.decode(data_text_nbch_YoY)
    data_json_shch_YoY = demjson.decode(data_text_shch_YoY)
    date_nbch = data_json_nbch_YoY['chart']['series']['value']
    data1_nbch_YoY = data_json_nbch_YoY['chart']['graphs']['graph'][0]['value']
    data2_nbch_YoY = data_json_nbch_YoY['chart']['graphs']['graph'][1]['value']
    data1_shch_YoY = data_json_shch_YoY['chart']['graphs']['graph'][0]['value']
    data2_shch_YoY = data_json_shch_YoY['chart']['graphs']['graph'][1]['value']
    df_YoY = pd.DataFrame({"Date": date_nbch,
                           "City1_nbch_YoY": data1_nbch_YoY,
                           "City1_shch_YoY": data1_shch_YoY,
                           "City2_nbch_YoY": data2_nbch_YoY,
                           "City2_shch_YoY": data2_shch_YoY})
    df_YoY["Date"] = pd.to_datetime(df_YoY["Date"], format="%m/%d/%Y")
    df = df_YoY.merge(df_MoM, on="Date")
    return df


def ci_eei_monthly():  # Climate Index & Entrepreneur Expectation Index
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    Data Source: http://data.eastmoney.com/cjsj/qyjqzs.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable7709842",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "8",
        "_": "1622041485306"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Climate_Index",
        "CI_YoY_Rate",
        "CI_MoM_Rate",
        "Entrepreneur_Expectation_Index",
        "EEI_YoY_Rate",
        "EEI_MoM_Rate"
    ]
    df.replace('', np.nan, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Climate_Index", "Entrepreneur_Expectation_Index"]] = \
        df[["Climate_Index", "Entrepreneur_Expectation_Index"]].astype(float)
    df[["CI_YoY_Rate", "CI_MoM_Rate", "EEI_YoY_Rate", "EEI_MoM_Rate"]] = df[[
        "CI_YoY_Rate", "CI_MoM_Rate", "EEI_YoY_Rate", "EEI_MoM_Rate"]].astype(float) / 100
    return df


def ig_monthly():  # Industry Growth
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    Data Source: http://data.eastmoney.com/cjsj/gyzjz.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable4577327",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "0",
        "_": "1622042259898"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "IG_YoY_Rate",
        "IG_Accum_Rate",
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["IG_YoY_Rate", "IG_Accum_Rate"]] = \
        df[["IG_YoY_Rate", "IG_Accum_Rate"]].astype(float) / 100
    return df


def cgpi_monthly():  # Corporate Goods Price Index
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    Data Source: http://data.eastmoney.com/cjsj/qyspjg.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable7184534",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "9",
        "_": "1622042652353"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "General_Index",
        "General_Index_YoY_Rate",
        "Total_Index_MoM_Rate",
        "Agricultural_Product",
        "Agricultural_Product_YoY_Rate",
        "Agricultural_Product_MoM_Rate",
        "Mineral_Product",
        "Mineral_Product_YoY_Rate",
        "Mineral_Product_MoM_Rate",
        "Coal_Oil_Electricity",
        "Coal_Oil_Electricity_YoY_Rate",
        "Coal_Oil_Electricity_MoM_Rate"
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["General_Index",
        "Agricultural_Product",
        "Mineral_Product",
        "Coal_Oil_Electricity"]] = df[["General_Index",
                                       "Agricultural_Product",
                                       "Mineral_Product",
                                       "Coal_Oil_Electricity"]].astype(float)
    df[["General_Index_YoY_Rate",
        "Total_Index_MoM_Rate",
        "Agricultural_Product_YoY_Rate",
        "Agricultural_Product_MoM_Rate",
        "Coal_Oil_Electricity_YoY_Rate",
        "Coal_Oil_Electricity_MoM_Rate"]] = df[["General_Index_YoY_Rate",
                                                "Total_Index_MoM_Rate",
                                                "Agricultural_Product_YoY_Rate",
                                                "Agricultural_Product_MoM_Rate",
                                                "Coal_Oil_Electricity_YoY_Rate",
                                                "Coal_Oil_Electricity_MoM_Rate"]].astype(float) / 100
    return df


def cci_csi_cei_monthly():  # Consumer Confidence Index & Consumer Satisfaction Index & Consumer Expectation Index
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    Data Source: http://data.eastmoney.com/cjsj/xfzxx.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable1243218",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "4",
        "_": "1622043704818"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "CCI",
        "CCI_YoY_Rate",
        "CCI_MoM_Rate",
        "CSI",
        "CSI_YoY_Rate",
        "CSI_MoM_Rate",
        "CEI",
        "CEI_YoY_Rate",
        "CEI_MoM_Rate"
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["CCI", "CSI", "CEI"]] = \
        df[["CCI", "CSI", "CEI"]].astype(float)
    df[["CCI_YoY_Rate", "CCI_MoM_Rate",
        "CSI_YoY_Rate", "CSI_MoM_Rate",
        "CEI_YoY_Rate", "CEI_MoM_Rate"]] = \
        df[["CCI_YoY_Rate", "CCI_MoM_Rate",
            "CSI_YoY_Rate", "CSI_MoM_Rate",
            "CEI_YoY_Rate", "CEI_MoM_Rate"]].astype(float) / 100
    return df


def trscg_monthly():  # Total Retail Sales of Consumer Goods
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    Data Source: http://data.eastmoney.com/cjsj/xfp.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable3665821",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "5",
        "_": "1622044011316"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "TRSCG_YoY_Rate",
        "TRSCG_MoM_Rate",
        "TRSCG_Accum",
        "TRSCG_Accum_YoY_Rate"
    ]
    df.replace("", np.nan, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Current_Month", "TRSCG_Accum"]] = \
        df[["Current_Month", "TRSCG_Accum"]].astype(float)
    df[["TRSCG_YoY_Rate", "TRSCG_MoM_Rate", "TRSCG_Accum_YoY_Rate"]] = df[[
        "TRSCG_YoY_Rate", "TRSCG_MoM_Rate", "TRSCG_Accum_YoY_Rate"]].astype(float) / 100
    return df


def ms_monthly():  # monetary Supply
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    Data Source: http://data.eastmoney.com/cjsj/hbgyl.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable3818891",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "11",
        "_": "1622044292103"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "M2",
        "M2_YoY_Rate",
        "M2_MoM_Rate",
        "M1",
        "M1_YoY_Rate",
        "M1_MoM_Rate",
        "M0",
        "M0_YoY_Rate",
        "M0_MoM_Rate"
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["M0", "M1", "M2"]] = \
        df[["M0", "M1", "M2"]].astype(float)
    df[["M0_YoY_Rate", "M1_YoY_Rate", "M2_YoY_Rate",
        "M0_MoM_Rate", "M1_MoM_Rate", "M2_MoM_Rate"]] = \
        df[["M0_YoY_Rate", "M1_YoY_Rate", "M2_YoY_Rate",
            "M0_MoM_Rate", "M1_MoM_Rate", "M2_MoM_Rate"]].astype(float) / 100
    return df


def ie_monthly():  # Import & Export
    """
    Data Source: http://data.eastmoney.com/cjsj/hgjck.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable3818891",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "1",
        "_": "1622044292103"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month_Export",
        "Current_Month_Export_YoY_Rate",
        "Current_Month_Export_MoM_Rate",
        "Current_Month_Import",
        "Current_Month_Import_YoY_Rate",
        "Current_Month_Import_MoM_Rate",
        "Accumulation_Export",
        "Accumulation_Export_YoY_Rate",
        "Accumulation_Import",
        "Accumulation_Import_YoY_Rate"
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Current_Month_Export", "Current_Month_Import",
        "Accumulation_Export", "Accumulation_Import"]] = \
        df[["Current_Month_Export", "Current_Month_Import",
            "Accumulation_Export", "Accumulation_Import"]].astype(float)
    df[["Current_Month_Export_YoY_Rate",
        "Current_Month_Export_MoM_Rate",
        "Current_Month_Import_YoY_Rate",
        "Current_Month_Import_MoM_Rate",
        "Accumulation_Export_YoY_Rate",
        "Accumulation_Export_MoM_Rate"]] = df[["Current_Month_Export_YoY_Rate",
                                               "Current_Month_Export_MoM_Rate",
                                               "Current_Month_Import_YoY_Rate",
                                               "Current_Month_Import_MoM_Rate",
                                               "Accumulation_Export_YoY_Rate",
                                               "Accumulation_Export_MoM_Rate"]].astype(float) / 100
    return df


def stock_monthly():  # Import & Export
    """
    Data Source: http://data.eastmoney.com/cjsj/gpjytj.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "jQuery112308659690274138041_1622084599455",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "2",
        "_": "1622084599456"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("(") + 1:-1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "SH_Total_Stock_issue",
        "SZ_Total_Stock_Issue",
        "SH_Total_Market_Capitalization",
        "SZ_Total_Market_Capitalization",
        "SH_Turnover",
        "SZ_Turnover",
        "SH_Volume",
        "SZ_Volume",
        "SH_Highest",
        "SZ_Highest",
        "SH_lowest",
        "SZ_lowest"
    ]
    df.replace("", np.nan, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[list(df.columns[1:])] = df[list(df.columns[1:])].astype(float)
    return df


def fgr_monthly():  # Forex and Gold Reserve
    """
    Data Source: http://data.eastmoney.com/cjsj/gpjytj.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "tatable6260802",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "16",
        "_": "1622044863548"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Forex",
        "Forex_YoY_Rate",
        "Forex_MoM_Rate",
        "Gold",
        "Gold_YoY_Rate",
        "Gold_MoM_Rate"
    ]
    df.replace("", np.nan, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Forex", "Gold"]] = \
        df["Forex", "Gold"].astype(float)
    df[["Forex_YoY_Rate", "Gold_YoY_Rate",
        "Forex_MoM_Rate", "Gold_MoM_Rate"]] = \
        df["Forex_YoY_Rate", "Gold_YoY_Rate",
           "Forex_MoM_Rate", "Gold_MoM_Rate"].astype(float) / 100
    return df
# TODO: SPECIAL CASE


def ctsf_monthly():  # Client Transaction Settlement Funds
    """
    http://data.eastmoney.com/cjsj/banktransfer.html
    """
    tmp_url = "http://data.eastmoney.com/dataapi/cjsj/getbanktransferdata?"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "p": "1",
        "ps": "200"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("["):-11])
    df = pd.DataFrame(data_json)
    df.replace("", np.nan, inplace=True)
    df["StartDate"] = pd.to_datetime(df["StartDate"], format="%Y-%m-%d")
    df["EndDate"] = pd.to_datetime(df["EndDate"], format="%Y-%m-%d")
    df[list(df.columns)[2:]] = df[list(df.columns)[2:]].astype(float)
    return df

# TODO: SPECIAL CASE


def sao_monthly():  # Stock Account Overview
    """
    http://data.eastmoney.com/cjsj/gpkhsj.html
    """
    tmp_url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "callback": "datatable4006236",
        "type": "GPKHData",
        "js": "({data:[(x)],pages:(pc)})",
        "st": "SDATE",
        "sr": "-1",
        "token": "894050c76af8597a853f5b408b759f5d",
        "p": "1",
        "ps": "2000",
        "_": "1622079339035"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") + 6: -14])
    df = pd.DataFrame(data_json[0])
    df.columns = [
        "Date",
        "New_Investor",
        "New_Investor_MoM_Rate",
        "New_Investor_YoY_Rate",
        "Active_Investor",
        "Active_Investor_A_Share",
        "Active_Investor_B_share",
        "SHIndex_Close",
        "SHIndex_Rate",
        "SHSZ_Market_Capitalization",
        "SHSZ_Average_Capitalization"
    ]
    df.replace("-", np.nan, inplace=True)
    df.Date = pd.to_datetime(df.Date, format="%Y年%m月")
    df[list(df.columns[~df.columns.isin(["Date", "New_Investor_MoM_Rate", "New_Investor_YoY_Rate"])])] = df[list(
        df.columns[~df.columns.isin(["Date", "New_Investor_MoM_Rate", "New_Investor_YoY_Rate"])])].astype(float)
    df[["New_Investor_MoM_Rate", "New_Investor_YoY_Rate"]] = \
        df[["New_Investor_MoM_Rate", "New_Investor_YoY_Rate"]].astype(float) / 100
    return df


def fdi_monthly():  # Foreign Direct Investment
    """
    http://data.eastmoney.com/cjsj/fdi.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable1477466",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "15",
        "_": "1622044863548"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY_Rate",
        "MoM_Rate",
        "Accumulation",
        "Accum_YoY_Rate"
    ]
    df.replace("", np.nan, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Current_Month", "Accumulation"]] = \
        df[["Current_Month", "Accumulation"]].astype(float)
    df[["YoY_Rate", "MoM_Rate", "Accum_YoY_Rate"]] = \
        df[["YoY_Rate", "MoM_Rate", "Accum_YoY_Rate"]].astype(float) / 100
    return df


def gr_monthly():  # Government Revenue
    """
    http://data.eastmoney.com/cjsj/czsr.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable7840652",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "14",
        "_": "1622080618625"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY_Rate",
        "MoM_Rate",
        "Accumulation",
        "Accum_YoY_Rate"
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Current_Month", "Accumulation"]] = \
        df[["Current_Month", "Accumulation"]].astype(float)
    df[["YoY_Rate", "MoM_rate", "Accum_YoY_Rate"]] = \
        df[["YoY_Rate", "MoM_rate", "Accum_YoY_Rate"]].astype(float) / 100
    return df


def ti_monthly():  # Tax Income
    """
    http://data.eastmoney.com/cjsj/qgsssr.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable8280567",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "3",
        "_": "1622080669713"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY_Rate",
        "MoM_Rate"
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Current_Month"]] = \
        df[["Current_Month"]].astype(float)
    df[["YoY_Rate", "MoM_rate"]] = \
        df[["YoY_Rate", "MoM_rate"]].astype(float) / 100
    return df


def nl_monthly():  # New Loan
    """
    http://data.eastmoney.com/cjsj/xzxd.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable2533707",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "7",
        "_": "1622080800162"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY_Rate",
        "MoM_Rate",
        "Accumulation",
        "Accum_YoY_Rate"
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Current_Month", "Accumulation"]] = \
        df[["Current_Month", "Accumulation"]].astype(float)
    df[["YoY_Rate", "MoM_Rate", "Accum_YoY_Rate"]] =\
        df[["YoY_Rate", "MoM_Rate", "Accum_YoY_Rate"]].astype(float) / 100
    return df


def dfclc_monthly():  # Deposit of Foreign Currency and Local Currency
    """
    http://data.eastmoney.com/cjsj/wbck.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable2899877",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "18",
        "_": "1622081057370"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY_Rate",
        "MoM_Rate",
        "Accumulation"
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Current_Month", "Accumulation"]] = \
        df[["Current_Month", "Accumulation"]].astype(float)
    df[["YoY_Rate", "MoM_Rate"]] = \
        df[["YoY_Rate", "MoM_Rate"]].astype(float) / 100
    return df


def fl_monthly():  # Forex Loan
    """
    http://data.eastmoney.com/cjsj/whxd.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable636844",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "17",
        "_": "1622081336038"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY",
        "MoM",
        "Accumulation"
    ]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df[["Current_Month", "Accumulation"]] = \
        df[["Current_Month", "Accumulation"]].astype(float)
    df[["YoY_Rate", "MoM_Rate"]] = \
        df[["YoY_Rate", "MoM_Rate"]].astype(float) / 100
    return df


def drr_monthly():  # Deposit Reserve Ratio
    """
    http://data.eastmoney.com/cjsj/ckzbj.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable4285562",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "23",
        "_": "1622081448882"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Announcement Date",
        "Effective Date",
        "Large_Financial_institution_Before",
        "Large_Financial_institution_After",
        "Large_Financial_institution_Adj_Rate",
        "S&M_Financial_institution_Before",
        "S&M_Financial_institution_After",
        "S&M_Financial_institution_Adj_Rate",
        "Comment",
        "SHIndex_Rate",
        "SZIndex_Rate"
    ]
    df["Announcement Date"] = pd.to_datetime(
        df["Announcement Date"], format="%Y-%m-%d")
    df["Effective Date"] = pd.to_datetime(
        df["Effective Date"], format="%Y-%m-%d")
    df[["Large_Financial_institution_Before",
        "Large_Financial_institution_After",
        "Large_Financial_institution_Adj_Rate",
        "S&M_Financial_institution_Before",
        "S&M_Financial_institution_After",
        "S&M_Financial_institution_Adj_Rate"]] = df[["Large_Financial_institution_Before",
                                                     "Large_Financial_institution_After",
                                                     "Large_Financial_institution_Adj_Rate",
                                                     "S&M_Financial_institution_Before",
                                                     "S&M_Financial_institution_After",
                                                     "S&M_Financial_institution_Adj_Rate"]].astype(float) / 100
    return df


def interest_monthly():  # Interest
    """
    http://data.eastmoney.com/cjsj/yhll.html
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "datatable7591685",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "13",
        "_": "1622081956464"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Announcement Date",
        "Deposit_Benchmark_Interest_Rate_Before",
        "Deposit_Benchmark_Interest_Rate_After",
        "Deposit_Benchmark_Interest_Rate_Adj_Rate",
        "Loan_Benchmark_Interest_Rate_Before",
        "Loan_Benchmark_Interest_Rate_After",
        "Loan_Benchmark_Interest_Rate_Adj_Rate",
        "SHIndex_Rate",
        "SZIndex_Rate",
        "Effective Date"
    ]
    df = df[[
        "Announcement Date",
        "Effective Date",
        "Deposit_Benchmark_Interest_Rate_Before",
        "Deposit_Benchmark_Interest_Rate_After",
        "Deposit_Benchmark_Interest_Rate_Adj_Rate",
        "Loan_Benchmark_Interest_Rate_Before",
        "Loan_Benchmark_Interest_Rate_After",
        "Loan_Benchmark_Interest_Rate_Adj_Rate",
        "SHIndex_Rate",
        "SZIndex_Rate"
    ]]
    df[list(df.columns)] = df[list(df.columns)].astype(float) / 100
    return df

# TODO: SPECIAL CASE


def gdc_daily():  # gasoline, Diesel and Crude Oil
    """
    http://data.eastmoney.com/cjsj/oil_default.html
    """
    tmp_url = "http://datacenter-web.eastmoney.com/api/data/get?"
    ua = UserAgent(verify_ssl=False)
    request_header = {"User-Agent": ua.random}
    request_params = {
        "callback": "jQuery112302601302322321093_1622082348721",
        "type": "RPTA_WEB_JY_HQ",
        "sty": "ALL",
        "st": "date",
        "sr": "-1",
        "token": "894050c76af8597a853f5b408b759f5d",
        "p": "1",
        "ps": "50000",
        "source": "WEB",
        "_": "1622082348722"
    }
    r = requests.get(tmp_url, params=request_params, headers=request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"): -2])
    df = pd.DataFrame(data_json["result"]["data"])
    df.columns = ["Crude_Oil", "Date", "Gasoline", "Diesel"]
    df = df[["Date", "Gasoline", "Diesel", "Crude_Oil"]]
    df = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    return df


"""
if __name__ == "__main__":
"""

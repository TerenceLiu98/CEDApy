import pandas as pd
import numpy as np
import re
import demjson
import requests
from fake_useragent import UserAgent

url = {
    "eastmoney": "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx"
}

def cn_gdp_quarter():
    """
    ABS: absolute value (per 100 million CNY)
    YoY: year on year growth
    """
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Absolute_Value",
        "YoY",
        "Primary_Industry_ABS",
        "Primary_Industry_YoY",
        "Secondary_Industry_ABS",
        "Secondary_Industry_YoY",
        "Tertiary_Industry_ABS",
        "Tertiary_Industry_YoY",
    ]
    #df[(df['Date'] >= startdate) & (df['Date'] <= enddate)]
    return df

def cn_cpi_monthly():
    """
    Accum: Accumulation
    YoY: year on year growth
    MoM: month on month growth
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Notion_Monthly",
        "Notion_YoY",
        "Notion_MoM",
        "Notion_Accum",
        "Urban_Monthly",
        "Urban_YoY",
        "Urban_MoM",
        "Urban_Accum",
        "Rural_Monthly",
        "Rural_YoY",
        "Rural_MoM",
        "Rural_Accum",
    ]
    return df

def cn_pmi_monthly():
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    temp_df.columns = [
        "Date",
        "Man_Industry_Index",
        "Man_Index_YoY",
        "Non-Man_Industry_Index",
        "Non-Man_Index_YoY",
    ]
    return temp_df

def cn_fai_monthly(): # fix asset investment
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY",
        "MoM",
        "Current_Year_Accum"
    ]
    return df

def cn_hi_old_monthly(): # house index old version (2008-2010)
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Housing_Prosperity_Index",
        "HPI_YoY",
        "Land_Development_Area_Index",
        "LDAI_YoY",
        "Sales_Price_Index",
        "SPI_YoY"
    ]
    return df

def cn_hi_mew_monthly(): # house index old version (2008-2010)
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    http://data.eastmoney.com/dataapi/cjsj/getnewhousechartdata?mkt=1&stat=1&city1=%E5%8C%97%E4%BA%AC&city2=%E9%95%BF%E6%98%A5
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "cb": "datatable6451982",
        "type": "GJZB",
        "sty": "XFJLB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "2000",
        "mkt": "19",
        "pageNo": "1",
        "pageNum": "1",
        "_": "1603023435552",
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    data = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Housing_Prosperity_Index",
        "HPI_YoY",
        "Land_Development_Area_Index",
        "LDAI_YoY",
        "Sales_Price_Index",
        "SPI_YoY"
    ]
    return df

"""
if __name__ == "__main__":
""" 
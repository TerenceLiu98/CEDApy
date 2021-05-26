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

def cn_ppi_monthly():
    """
    ABS: absolute value (per 100 million CNY)
    YoY: year on year growth
    """
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "Current_Month_YoY",
        "Current_Month_Accum"
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

def cn_ci_eei_monthly(): # Climate Index & Entrepreneur Expectation Index
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Climate_Index",
        "CI_YoY",
        "CI_MoM",
        "Entrepreneur_Expectation_Index",
        "EEI_YoY",
        "EEI_MoM"
    ]
    return df

def cn_ig_monthly(): # Industry Growth
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "IG_YoY",
        "IG_Accum",
    ]
    return df

def cn_cgpi_monthly(): # Corporate Goods Price Index
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "General_Index",
        "General_Index_YoY",
        "Total_Index_MoM",
        "Agricultural_Product",
        "Agricultural_Product_YoY",
        "Agricultural_PRoduct_MoM",
        "Mineral_Product",
        "Mineral_Product_YoY",
        "Mineral_Product_MoM",
        "Coal_Oil_Electricity",
        "Coal_Oil_Electricity_YoY",
        "Coal_Oil_Electricity_MoM"
    ]
    return df

def cn_cci_csi_cei_monthly(): # Consumer Confidence Index & Consumer Satisfaction Index & Consumer Expectation Index
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "CCI",
        "CCI_YoY",
        "CCI_MoM",
        "CSI",
        "CSI_YoY",
        "CSI_MoM",
        "CEI",
        "CEI_YoY",
        "CEI_MoM"
    ]
    return df

def cn_trscg_monthly(): # Total Retail Sales of Consumer Goods
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "TRSCG_YoY",
        "TRSCG_MoM",
        "TRSCG_Accum",
        "TRSCG_Accum_YoY" 
    ]
    return df

def cn_ms_monthly(): # monetary Supply
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "M2",
        "M2_YoY",
        "M2_MoM",
        "M1",
        "M1_YoY",
        "M1_MoM",
        "M0",
        "M0_YoY",
        "M0_MoM"
    ]
    return df

def cn_ie_monthly(): # Import & Export
    """

    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month_Export",
        "Current_Month_Export_YoY",
        "Current_Month_Export_MoM",
        "Current_Month_Import",
        "Current_Month_Import_YoY",
        "Current_Month_Import_MoM",
        "Accumulation_Export",
        "Accumulation_Export_YoY",
        "Accumulation_Import",
        "Accumulation_Import_YoY",
    ]
    return df


def cn_ie_monthly(): # Import & Export
    """

    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month_Export",
        "Current_Month_Export_YoY",
        "Current_Month_Export_MoM",
        "Current_Month_Import",
        "Current_Month_Import_YoY",
        "Current_Month_Import_MoM",
        "Accumulation_Export",
        "Accumulation_Export_YoY",
        "Accumulation_Import",
        "Accumulation_Import_YoY",
    ]
    return df

def cn_fgr_monthly(): # Forex and Gold Reserve
    """

    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    tmp_url = url["eastmoney"]
    request_params = {
        "cb": "atatable6260802",
        "type": "GJZB",
        "sty": "ZGZB",
        "js": "({data:[(x)],pages:(pc)})",
        "p": "1",
        "ps": "200",
        "mkt": "16",
        "_": "1622044863548"
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Forex",
        "Forex_YoY",
        "Forex_MoM",
        "Gold",
        "Gold_YoY",
        "Gold_MoM"
    ]
    return df

def cn_ctsf_monthly(): # Client Transaction Settlement Funds
    """

    """
    tmp_url = "http://data.eastmoney.com/dataapi/cjsj/getbanktransferdata?"
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "p": "1",
        "ps": "200"
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("["):-11])
    df = pd.DataFrame(data_json)
    return df

# TODO: needs help (missing two tables)
def cn_sao_monthly(): # Stock Account Overview 
    """
    """
    tmp_url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?"
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "callback": "jQuery1123014377091065513636_1622046865705",
        "type": "GPKHData",
        "st": "HdDate",
        "sr": "-1",
        "sty": "Chart",
        "token": "894050c76af8597a853f5b408b759f5d",
        "ps": "2000",
        "_": "1622046865706"
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("(")+1:-1])
    df = pd.DataFrame(data_json)
    df.columns = [
        "Date",
        "New_Investor",
        "Active_Investor",
        "SHIndexClose"
    ]
    df.Date = pd.to_datetime(df.Date, format = "%Y年%m月")
    return df


"""
if __name__ == "__main__":
""" 
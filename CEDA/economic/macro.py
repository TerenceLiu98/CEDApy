import pandas as pd
import numpy as np
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

# mkt=1&stat=2&city1=%E5%B9%BF%E5%B7%9E&city2=%E4%B8%8A%E6%B5%B7

def cn_hi_new_monthly(city1:str, city2:str): # newly built commercial housing &  second-hand commercial housing
    """
    Man: manufacturing
    Non-Man: Non-manufacturing
    """
    tmp_url = "http://data.eastmoney.com/dataapi/cjsj/getnewhousechartdata?"
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params_nbch = {
        "mkt": "1",
        "stat": "2",
        "city1": "{}".format(city1),
        "city2": "{}".format(city2)
    }
    request_params_shch = {
        "mkt": "1",
        "stat": "3",
        "city1": "{}".format(city1),
        "city2": "{}".format(city2)
    }
    r_nbch = requests.get(tmp_url, params = request_params_nbch, headers = request_header)
    r_shch = requests.get(tmp_url, params = request_params_shch, headers = request_header)
    data_text_nbch = r_nbch.text
    data_text_shch = r_shch.text
    data_json_nbch = demjson.decode(data_text_nbch)
    data_json_shch = demjson.decode(data_text_shch)
    date_nbch = data_json_nbch['chart']['series']['value']
    data1_nbch = data_json_nbch['chart']['graphs']['graph'][0]['value']
    data2_nbch = data_json_nbch['chart']['graphs']['graph'][1]['value']
    data1_shch = data_json_shch['chart']['graphs']['graph'][0]['value']
    data2_shch = data_json_shch['chart']['graphs']['graph'][1]['value']
    df = pd.DataFrame({"Date": date_nbch, 
                       "City1":data1_nbch, 
                       "City2":data2_nbch,
                       "City1":data1_shch, 
                       "City2":data2_shch})
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
        "Accumulation_Import_YoY"
    ]
    return df


def cn_stock_monthly(): # Import & Export
    """
&type=GJZB&sty=ZGZB&js=(%5B(x)%5D)&p=1&ps=200&mkt=2&_=1622084599456
    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("(")+1:-1])
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
    return df

def cn_fgr_monthly(): # Forex and Gold Reserve
    """

    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
#TODO: SPECIAL CASE
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

# TODO: SPECIAL CASE
def cn_sao_monthly(): # Stock Account Overview 
    """

    """
    tmp_url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?"
    ua = UserAgent()
    request_header = {"User-Agent": ua.random}
    request_params = {
        "callback": "datatable4006236",
        "type": "GPKHData",
        "js" : "({data:[(x)],pages:(pc)})",
        "st": "SDATE",
        "sr": "-1",
        "token": "894050c76af8597a853f5b408b759f5d",
        "p": "1",
        "ps": "2000",
        "_": "1622079339035"
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{")+6 : -14])
    df = pd.DataFrame(data_json[0])
    df.columns = [
        "Date",
        "New_Investor",
        "New_Investor_MoM",
        "New_Investor_YoY",
        "Active_Investor",
        "Active_Investor_A_Share",
        "Active_Investor_B_share",
        "SHIndex_Close",
        "SHIndex_Rate",
        "SHSZ_Market_Capitalization",
        "SHSZ_Average_Capitalization"
    ]
    df.Date = pd.to_datetime(df.Date, format = "%Y年%m月")
    return df

def cn_fdi_monthly(): # Foreign Direct Investment
    """

    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY",
        "MoM",
        "Accumulation",
        "Accum_YoY"
    ]
    return df

def cn_gr_monthly(): # Government Revenue
    """

    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY",
        "MoM",
        "Accumulation",
        "Accum_YoY"
    ]
    return df

def cn_ti_monthly(): # Tax Income
    """

    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY",
        "MoM"
    ]
    return df


def cn_nl_monthly(): # New Loan
    """

    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY",
        "MoM",
        "Accumulation",
        "Accum_YoY"
    ]
    return df

def cn_dfclc_monthly(): # Deposit of Foreign Currency and Local Currency
    """

    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY",
        "MoM",
        "Accumulation"
    ]
    return df

def cn_fl_monthly(): # Forex Loan
    """

    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
    df = pd.DataFrame([item.split(",") for item in data_json["data"]])
    df.columns = [
        "Date",
        "Current_Month",
        "YoY",
        "MoM",
        "Accumulation"
    ]
    return df

def cn_drr_monthly(): # Deposit Reserve Ratio
    """

    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
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
    return df

def cn_interest_monthly(): # Interest
    """

    """
    tmp_url = url["eastmoney"]
    ua = UserAgent()
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
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -1])
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
    return df

#TODO: SPECIAL CASE
def cn_gdc_daily(): # gasoline, Diesel and Crude Oil
    """
    """
    tmp_url = "http://datacenter-web.eastmoney.com/api/data/get?"
    ua = UserAgent()
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
        "_":"1622082348722"
    }
    r = requests.get(tmp_url, params = request_params, headers = request_header)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{") : -2])
    df = pd.DataFrame(data_json["result"]["data"])
    df.columns = ["Crude_Oil", "Date", "Gasoline", "Diesel"]
    df = df[["Date", "Gasoline", "Diesel", "Crude_Oil"]]
    return df

"""
if __name__ == "__main__":
""" 
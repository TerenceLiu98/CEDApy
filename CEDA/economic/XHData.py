import ast
import requests
import pandas as pd

url = {
    "CNFIN": "https://api.cnfin.com/roll/charts/"
}

class XHData(object):
    def __init__(self):
        pass
    
    def download(self, id:int=None):
        tmp_url = url["CNFIN"] + "getContent?ids={}".format(id)
        r = requests.get(tmp_url)
        if r.ok:
            raw_data = r.json()
            data = pd.DataFrame(ast.literal_eval(raw_data["data"]["list"][0]["content"]))
            return data
        else:
            return ValueError("Something went wrong, try again later")

    
    def GDP(self):
        """
        quarterly
        """
        data = self.download(id=12006)
        data.columns = ["date", "data"]
        return data
    
    def Household_Consumption_SPLY(self):
        """
        quarterly
        """
        data = self.download(id=12073)
        data.columns = ["date", "data"]
        return data

    def Household_Consumption(self):
        """
        quarterly
        """
        data = self.download(id=12074)
        data.columns = ["date", "data"]
        return data

    def Per_capita_Disposable_Income(self):
        """
        quarterly
        """
        data = self.download(id=12071)
        data.columns = ["date", "data"]
        return data

    def Urban_Average_Salary_Annual(self):
        """
        quarterly
        """
        data = self.download(id=12070)
        data.columns = ["date", "data"]
        return data

    def Urban_Uneployment_Rate(self):
        """
        quarterly
        """
        data = self.download(id=12069)
        data.columns = ["date", "data"]
        return data

    def Government_Bound_Return_Rate_10_Year(self):
        """
        quarterly
        """
        data = self.download(id=12068)
        data.columns = ["date", "data"]
        return data

    def Government_Bound_Return_Rate_3_Year(self):
        """
        quarterly
        """
        data = self.download(id=12067)
        data.columns = ["date", "data"]
        return data

    def Government_Bound_Return_Rate_1_Year(self):
        """
        quarterly
        """
        data = self.download(id=12066)
        data.columns = ["date", "data"]
        return data

    def LPR_1_Year(self):
        """
        Monthly
        """
        data = self.download(id=12065)
        data.columns = ["date", "data"]
        return data

    def SHIBOR_3_Month(self):
        """
        Daily
        """
        data = self.download(id=12064)
        data.columns = ["date", "data"]
        return data

    def SHIBOR_2_Week(self):
        """
        Daily
        """
        data = self.download(id=12063)
        data.columns = ["date", "data"]
        return data

    def SHIBOR_1_Day(self):
        """
        Daily
        """
        data = self.download(id=12063)
        data.columns = ["date", "data"]
        return data

    def Foreign_Exchange_Options(self):
        data = self.download(id=12060)
        data.columns = ["date", "data"]
        return data     

    def Foreign_Exchange_Swaps(self):
        data = self.download(id=12059)
        data.columns = ["date", "data"]
        return data  

    def Foreign_Exchange_Forward(self):
        data = self.download(id=12058)
        data.columns = ["date", "data"]
        return data       

    def Foreign_Exchange_Spot(self):
        data = self.download(id=12057)
        data.columns = ["date", "data"]
        return data       

    def Loan_to_Deposit(self):
        data = self.download(id=12056)
        data.columns = ["date", "data"]
        return data         

    def RMB_Deposits(self):
        data = self.download(id=12055)
        data.columns = ["date", "data"]
        return data     

    def RMB_Loan(self):
        data = self.download(id=12054)
        data.columns = ["date", "data"]
        return data  

    def M0_SPLY(self):
        data = self.download(id=12053)
        data.columns = ["date", "data"]
        return data  

    def M1_SPLY(self):
        data = self.download(id=12052)
        data.columns = ["date", "data"]
        return data  

    def M2_SPLY(self):
        data = self.download(id=12051)
        data.columns = ["date", "data"]
        return data  

    def M0(self):
        data = self.download(id=12050)
        data.columns = ["date", "data"]
        return data  

    def M1(self):
        data = self.download(id=12049)
        data.columns = ["date", "data"]
        return data  

    def M2(self):
        data = self.download(id=12048)
        data.columns = ["date", "data"]
        return data  

    def Total_Retail_Sales_of_Consumer_Goods_LP(self):
        data = self.download(id=12047)
        data.columns = ["date", "data"]
        return data  

    def Total_Retail_Sales_of_Consumer_Goods_SPLY(self):
        data = self.download(id=12046)
        data.columns = ["date", "data"]
        return data  

"""
import json
import requests
from tqdm import tqdm

urls, titles = [], []
for i in tqdm(range(5000, 20000)):
    url = "https://api.cnfin.com/roll/charts/getContent?ids={}".format(i)
    r = requests.get(url)
    if r.ok:
        data = r.json()
        if data["data"] == "图表数据不存在":
            pass
        else:
            urls.append(url)
            titles.append(json.loads(data["data"]["list"][0]["modelCode"])["title"]["text"])
"""


            


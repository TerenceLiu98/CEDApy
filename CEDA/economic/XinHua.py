import ast
import json
import requests
import pandas as pd
from tqdm import tqdm
from pygtrans import Translate

def translate(text:str=None):
    client = Translate()
    text = client.translate(text, target="en")
    return text.translatedText

url = {
    "CNFIN": "https://api.cnfin.com/roll/charts/"
}

class XHData(object):
    def __init__(self, country:str=None):
        self.country = country
        pass

    
    def toc(self):
        urls, tid, titles, titles_en = [], [], [], []
        if self.country == "CN":
            for i in tqdm(range(12005, 12100)):
                url = "https://api.cnfin.com/roll/charts/getContent?ids={}".format(i)
                r = requests.get(url)
                if r.ok:
                    data = r.json()
                    if data["data"] == "图表数据不存在":
                        pass
                    else:
                        urls.append(url)
                        tid.append(i)
                        title = json.loads(data["data"]["list"][0]["modelCode"])["title"]["text"]
                        titles.append(title)
                        titles_en.append(translate(text=title))
        elif self.country == "USA":
            for i in tqdm(range(6361, 6394)):
                url = "https://api.cnfin.com/roll/charts/getContent?ids={}".format(i)
                r = requests.get(url)
                if r.ok:
                    data = r.json()
                    if data["data"] == "图表数据不存在":
                        pass
                    else:
                        urls.append(url)
                        tid.append(i)
                        title = json.loads(data["data"]["list"][0]["modelCode"])["title"]["text"]
                        titles.append(title)
                        titles_en.append(translate(text=title))
        elif self.country == "UK":
            for i in tqdm(range(6539, 6566)):
                url = "https://api.cnfin.com/roll/charts/getContent?ids={}".format(i)
                r = requests.get(url)
                if r.ok:
                    data = r.json()
                    if data["data"] == "图表数据不存在":
                        pass
                    else:
                        urls.append(url)
                        tid.append(i)
                        title = json.loads(data["data"]["list"][0]["modelCode"])["title"]["text"]
                        titles.append(title)
                        titles_en.append(translate(text=title))

        elif self.country == "Japan":
            for i in tqdm(range(6394, 6425)):
                url = "https://api.cnfin.com/roll/charts/getContent?ids={}".format(i)
                r = requests.get(url)
                if r.ok:
                    data = r.json()
                    if data["data"] == "图表数据不存在":
                        pass
                    else:
                        urls.append(url)
                        tid.append(i)
                        title = json.loads(data["data"]["list"][0]["modelCode"])["title"]["text"]
                        titles.append(title)
                        titles_en.append(translate(text=title))

        return pd.DataFrame({"urls":urls, "id":tid, "title_zh":titles, "title_en":titles_en})
    
    def download_data(self, iid:int=None):
        tmp_url = url["CNFIN"] + "getContent?ids={}".format(iid)
        r = requests.get(tmp_url)
        if r.ok:
            raw_data = r.json()
            data = pd.DataFrame(ast.literal_eval(raw_data["data"]["list"][0]["content"]))
            data.columns = ["date", "data"]
            return data
        else:
            return ValueError("Something went wrong, try again later")

if __name__ == "__main__":
    xhdata = XHData(country="CN")
    toc = xhdata.toc()
    data = xhdata.download_data(iid=12006) # GDP

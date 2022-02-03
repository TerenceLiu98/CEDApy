from lxml import html
import requests
import pandas as pd

url = {
    "EPU-China": "https://economicpolicyuncertaintyinchina.weebly.com",
    "EPU-HKSAR": "https://economicpolicyuncertaintyinchina.weebly.com/epu-in-hong-kong.html",
    "EPU-MACAUSAR": "https://economicpolicyuncertaintyinchina.weebly.com/epu-in-macao.html",
    "EPU": "https://www.policyuncertainty.com/"
}

def country_list():
    country_list = ["Global", "USA", "Australia", "Belgium", 
            "Brazil", "Canada", "Chile", "China", 
            "Colombia", "Croatia", "Denmark", "France", 
            "Germany", "Greece", "HKSAR", "MACAUSAR", 
            "India", "Ireland", "Italy", "Japan", 
            "Korea", "Mexico", "Netherlands", "Pakistan", 
            "Russia", "Singapore", "Spain", "Sweden", "UK"]
    annotations = "Disambiguation: the word 'Korea' in here stands for 'South Korea'"
    return country_list, annotations

class EPUData(object):
    def __init__(self, country:str=None):
        self.country = country
    
    def download(self):
        if self.country == "China":
            r = requests.get(url["EPU-China"])
            webpage = html.fromstring(r.content)
            urls = pd.Series(webpage.xpath("//a/@href"))
            urls_data = urls[urls.str.contains("xlsx")]
            urls_cite = urls[urls.str.contains("pdf")]
            urls_data = [url["EPU-China"] + i for i in urls_data]
            urls_cite = [url["EPU-China"] + i for i in urls_cite]
            output_data = []
            for i in range(0, len(urls_data)):
                output_data.append(pd.read_excel(urls_data[i]))
            
            return {"data":output_data, "reference":urls_cite}

        elif self.country == "HKSAR":
            r = requests.get(url["EPU-HKSAR"])
            webpage = html.fromstring(r.content)
            urls = pd.Series(webpage.xpath("//a/@href"))
            urls_data = urls[urls.str.contains("xlsx")]
            urls_cite = urls[urls.str.contains("pdf")]
            urls_data = [url["EPU-China"] + i for i in urls_data]
            urls_cite = [url["EPU-China"] + i for i in urls_cite]
            output_data = []
            for i in range(0, len(urls_data)):
                output_data.append(pd.read_excel(urls_data[i]))
            
            return {"data":output_data, "reference":urls_cite}

        elif self.country == "MACAUSAR":
            r = requests.get(url["EPU-MACAUSAR"])
            webpage = html.fromstring(r.content)
            urls = pd.Series(webpage.xpath("//a/@href"))
            urls_data = urls[urls.str.contains("xlsx")]
            urls_cite = urls[urls.str.contains("pdf")]
            urls_data = [url["EPU-China"] + i for i in urls_data]
            urls_cite = [url["EPU-China"] + i for i in urls_cite]
            output_data = []
            for i in range(0, len(urls_data)):
                output_data.append(pd.read_excel(urls_data[i]))
            
            return {"data":output_data, "reference":urls_cite}
        
        else:
            r = requests.get(url["EPU"] + self.country.lower() + "_monthly.html")
            webpage = html.fromstring(r.content)
            urls = pd.Series(webpage.xpath("//a/@href"))
            urls_data = urls[urls.str.contains("xlsx")]
            urls_cite = urls[urls.str.contains("pdf")]
            urls_data = [url["EPU"] + i for i in urls_data]
            urls_cite = [url["EPU"] + i for i in urls_cite]
            output_data = []
            for i in range(0, len(urls_data)):
                try:
                    tmp_data = pd.read_excel(urls_data[i])
                    output_data.append(tmp_data)
                except Exception as e:
                    pass
            
            return {"data":output_data, "reference":urls_cite}

import requests
import pandas as pd
from bs4 import BeautifulSoup

url = {
    "ECB": "https://sdw.ecb.europa.eu/",
    "ECB-API": "http://sdw-wsrest.ecb.europa.eu/service/data/"
}

class ECBData(object):
    def __init__(self) -> None:
        pass

    def toc(self):
        r = requests.get(url["ECB"] + "browse.do?node=9689727")
        dataset_list = BeautifulSoup(r.text, "html.parser").find_all("div", {"id": "currentMaximizeNode0"})
        uls = dataset_list[0].find_all("ul")
        lis = [li for ul in uls for li in ul.find_all("li")]
        li_text = [li.text.strip() for li in lis]
        name, metadata = [], []
        for i in range(0, len(li_text)):
            name.append(li_text[i].split("-")[0])
            metadata.append(li_text[i].split("-")[1])

        li_urls = [url["ECB"] + li.a.get("href") for li in lis]
        toc = pd.DataFrame({"name": name, "metadata":metadata, "url":li_urls})
        return toc

    
    def download_data(self, datasetname:str=None):
        tmp_url = url["ECB-API"] + "{}?format=csvdata".format(datasetname)
        data = pd.read_csv(tmp_url)
        return data
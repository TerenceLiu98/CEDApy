import requests
import pandas as pd
from bs4 import BeautifulSoup

url = {
    "BOJ": "https://www.stat-search.boj.or.jp"
}

class BOJData(object):
    def __init__(self) -> None:
        pass

    def toc(self):
        tmp_url = url["BOJ"] + "/index_en.html"
        r = requests.get(tmp_url)
        main_statistics_table = BeautifulSoup(r.text, "html.parser").find_all('div', {"class": "clearfix"})[1]
        uls = main_statistics_table.find_all("ul")
        lis = [li for ul in uls for li in ul.find_all("li", {"class": "icoSimpleRightArrowForMainTime-series mainTimeSeriesName"})]
        li_text = [li.text.strip() for li in lis]
        li_urls = [url["BOJ"] + li.a.get("href") for li in lis] 
        toc = pd.DataFrame({"title": li_text, "url":li_urls})
        return toc
    
    def _download(self, down_url:str=None):
        r = requests.get(down_url)
        table = BeautifulSoup(r.text, "html.parser").find_all("table")
        data = pd.read_html(str(table))[0]
        header = ["time"] +  list(data.loc[0][1:])
        data.columns = header
        data = data[1:]
        return data
    
    def download_data(self, query:str=None):
        toc = self.toc()
        if query == None:
            return ValueError("rex is invalid.")
        else:
            data = toc[toc["title"].str.contains(query)].reset_index(drop=True)
            if data.empty:
                return ValueError("No related dataset, check the query again")
            else:
                output = []
                for i in range(0, len(data)):
                    output.append(self._download(down_url=data.loc[i]["url"]))
                
                return output





        
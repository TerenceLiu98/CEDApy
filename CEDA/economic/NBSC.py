"""
NBSC's api information:

url: "https://data.stats.gov.cn/english/easyquery.htm"
params: id=zb&dbcode=hgnd&wdcode=ab&m=getTree
"""

import os
import time
import pickle
import random
import requests
import pandas as pd
from tqdm import tqdm
from fake_useragent import UserAgent
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class NBSCData(object):
    def __init__(self, language:str="en"):

        self.dbcode = []
        self.nid = []
        self.pid = []
        self.name = []
        self.wdcode= []

        if language == "cn":
            self.url = "https://data.stats.gov.cn/easyquery.htm"
            self.BASE_DIR = os.path.dirname(__file__)
            self.__TREE_PATH__ = os.path.join(self.BASE_DIR, "NBSCTree", "data.pkl")
        elif language == "en":
            self.url = "https://data.stats.gov.cn/english/easyquery.htm"
            self.BASE_DIR = os.path.dirname(__file__)
            self.__TREE_PATH__ = os.path.join(self.BASE_DIR, "NBSCTree", "data_en.pkl")

    def generate_header(self):
        ua = UserAgent()
        header = {'User-Agent':str(ua.chrome)}
        return header


    def tree_generation(self, rid="zb", mode:str="fast"):
        """
        inspired by a blog: https://www.cnblogs.com/wang_yb/p/14636575.html
        """
        parent = []
        r = requests.post("{}?id={}&dbcode=hgnd&wdcode=zb&m=getTree".format(self.url, rid), headers=self.generate_header(), verify=False)
        data = r.json()

        for i in range(0, len(data)):
            node = data[i]
            print("[+] Downloading {} ...".format(node["name"]))
            if node["isParent"]:
                parent.append(node["id"])
                node["children"] = self.tree_generation(rid=node["id"])
            if i % 100 == 0:
                print("[-] Due to the web scraping policy, sleep for 2 seconds")
                time.sleep(1)
            if mode == "slow":
                if i % 1000 == 0:
                    print("[-] Due to the web scraping policy, sleep for 10 seconds")
                    time.sleep(10)    

        return data  
    

    def toc(self, nodes):
        """
        inspired by a blog: https://www.cnblogs.com/wang_yb/p/14636575.html
        """
        for i in range(0, len(nodes)):
            node = nodes[i]
            if node["isParent"]:
                self.toc(node["children"])
            else:
                self.dbcode.append(node["dbcode"])
                self.nid.append(node["id"])
                self.name.append(node["name"])
                self.pid.append(node["pid"])
                self.wdcode.append(node["wdcode"])
        
        data = pd.DataFrame({"dbcode":self.dbcode, "nid":self.nid, 
                                "name":self.name, "pid":self.pid, "wdcode":self.wdcode})
        return data
    

    
    def download_data(self, nid:str=None, sj="1978-", period:str="monthly"):

        if period == "monthly":
            dbcode="hgyd"
        elif period == "quarterly":
            dbcode="hgjd"
        elif period == "annual":
            dbcode="hgnd"

        params = {
        "m": "QueryData",
        "dbcode": dbcode,
        "rowcode": "zb",
        "colcode": "sj",
        "wds": "[]",
        "dfwds": '[{"wdcode":"zb","valuecode":"'
        + nid
        + '"},{"wdcode":"sj","valuecode":"'
        + '"}]',
        "sj": sj
        }
        r = requests.get(self.url, params=params, verify=False, headers=self.generate_header())
        if r.ok:
            data = r.json()["returndata"]["datanodes"]
            date, value = [], []
            for i in range(0, len(data)):
                date.append(data[i]["wds"][1]["valuecode"])
                value.append(data[i]["data"]["data"])
            
            output = pd.DataFrame({"date":date, "value":value})
            return output

if __name__ == "__main__":
    nbsc = NBSCData(language="en")
    nodes = nbsc.tree_generation()
    toc = nbsc.toc(nodes=nodes)
    toc[toc["name"].str.contains("GDP")]
    data = nbsc.download_data(nid="A0203")

            
            
            



                
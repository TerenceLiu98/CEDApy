import pandas as pd
import numpy as np
import io
import demjson
import requests
from fake_useragent import UserAgent


url = {
    "eurostat": "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/",
    "ecb": "https://sdw-wsrest.ecb.europa.eu/service/data/"
}

class ecb_data(object):
    def __init__(self, url=url["ecb"]):
        self.url = url

    def codebook(self):
        return "please follow the ECB's codebook: https://sdw.ecb.europa.eu/browse.do?node=9691101"

    def get_data(self,
                 datacode="ICP", 
                 key="M.U2.N.000000.4.ANR", 
                 startdate="2000-01-01", 
                 enddate="2020-01-01"):
        """
        """
        tmp_url = self.url + "{}/".format(datacode) + "{}".format(key)
        ua = UserAgent()
        request_header = {"User-Agent": ua.random, 'Accept': 'text/csv'}
        request_params = {
            "startPeriod": "{}".format(startdate),
            "endPeriod": "{}".format(enddate)
        }
        r = requests.get(tmp_url, params = request_params, headers = request_header)
        data_text = r.content
        df = pd.read_csv(io.StringIO(data_text.decode('utf-8')))
        return df

class eurostat_data(object):
    def __init__(self, url=url["eurostat"]):
        self.url = url

    def codebook(self):
        return "please follow the EuroStat's codebook: \nhttps://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&dir=dic"
        
    def get_data(self,
                 datasetcode="nama_10_gdp", 
                 precision="1",
                 unit="CP_MEUR",
                 na_item="B1GQ",
                 time="2020"):
        """
        """
        tmp_url = self.url + "{}".format(datasetcode)
        ua = UserAgent()
        request_header = {"User-Agent": ua.random, 'Accept': 'text/csv'}
        request_params = {
            "precision": "{}".format(precision),
            "unit": "{}".format(unit),
            "na_item": "{}".format(na_item),
            "time": "{}".format(time)
        }
        r = requests.get(tmp_url, params = request_params, headers = request_header)
        data_text = r.text
        data_json = demjson.decode(data_text)
        value = data_json['value']
        abb = data_json['dimension']['geo']['category']['index']
        abb = {abb[k]:k for k in abb}
        geo = data_json['dimension']['geo']['category']['label']
        geo_list = [abb[int(k)] for k in list(value.keys())]
        geo = [geo[k] for k in geo_list]
        df = pd.DataFrame({"Geo":geo, "{}".format(na_item): list(value.values())})
        return df
import io
import os
import ssl
import time
import json
import tqdm
import requests
import numpy as np
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import dateutil.parser as dparser
from fake_useragent import UserAgent

ssl._create_default_https_context = ssl._create_unverified_context

# Main Economic Indicators: https://alfred.stlouisfed.org/release?rid=205
url = {
    "fred_econ": "https://fred.stlouisfed.org/graph/fredgraph.csv?",
    "fred_series": "https://fred.stlouisfed.org/series/",
    "philfed":
    "https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/",
    "chicagofed": "https://www.chicagofed.org/~/media/publications/",
    "OECD": "https://stats.oecd.org/sdmx-json/data/DP_LIVE/"
}


def get_tag(id: str) -> list:
    tmp_url = url["fred_series"] + id
    r = requests.get(tmp_url)
    tags = []
    tags_series = BeautifulSoup(r.text, "html.parser").find_all(
        "div", {"class": "series-tag-cloud"})
    for i in tqdm.tqdm(range(0, len(tags_series))):
        subtable = tags_series[i].find_all("a")
        for j in tqdm.tqdm(range(0, len(subtable)), leave=False):
            tags.append((" ".join(subtable[j].text.split())))
    return tags


def get_metadata(id: str = None) -> dict:
    tmp_url = url["fred_series"] + id
    r = requests.get(tmp_url)
    metadata = {
        "name": (" ".join(
            BeautifulSoup(r.text, "html.parser").find_all(
                'div', {"class": "page-title"})[0].span.text.split())),
        "id":
        id,
        "update_time":
        datetime.strftime(dparser.parse(
            BeautifulSoup(r.text, "html.parser").find_all(
                'div',
                {"class": "pull-left meta-col"})[0].find_all('span')[3].text,
            fuzzy=True),
                          format="%Y-%m-%d"),
        "units":
        BeautifulSoup(r.text, "html.parser").find_all(
            'div', {"class": "pull-left meta-col"
                    })[1].find_all('span')[0].text.split("        ")[0],
        "frequency":
        BeautifulSoup(r.text,
                      "html.parser").find_all('div',
                                              {"class": "pull-left meta-col"})
        [2].find_all('span')[0].text.split("            ")[1].split("    ")[1],
        "tags":
        get_tag(id)
    }
    return metadata


def date_transform(df, format_origin, format_after):
    return_list = []
    for i in range(0, len(df)):
        return_list.append(
            datetime.strptime(df[i], format_origin).strftime(format_after))
    return return_list


class FredData(object):

    def __init__(self, country: str = "usa"):
        self.country = country

    __annotations__ = {
        "name": "Main Economic Indicators",
        "url": "https://fred.stlouisfed.org/tags/series?t=mei"
    }

    def get_id(self, url: str) -> list:
        id_list = []
        r = requests.get(url)
        table = BeautifulSoup(r.text, "html.parser").find_all("table")
        for i in range(0, len(table)):
            subtable = table[i].find_all("a")
            for j in range(0, len(subtable)):
                id_list.append(subtable[j].get("href").split("/")[-1])
        return id_list

    def extract_id(self):
        id_list = []
        for i in tqdm.tqdm(range(1, 100)):
            tmp_url = "https://fred.stlouisfed.org/tags/series?ob=pv&od=desc&t=mei%3B{}&pageID={}".format(
                self.country, str(i))
            id_list.append(self.get_id(tmp_url))
            if i > 20:
                r = requests.get(tmp_url)
                if "No series" in r.text:
                    break
                else:
                    continue

        id_list = [item for sublist in id_list for item in sublist]
        id_list = list(set(id_list))
        return id_list

    def toc(self):
        sid = self.extract_id()
        name = []
        for i in range(0, len(sid)):
            name.append(get_metadata(id=sid[i])["name"])
            time.sleep(2)
            
        toc = pd.DataFrame({"name": name, "id": sid})
        return toc

    def download_data(self, sid: str = None):
        data = pd.read_csv(url["fred_econ"] + "id={}".format(sid))
        return data


if __name__ == "__main__":
    usa = FredData(country="usa")
    usa_list = usa.extract_id()
    china = FredData(country="china")
    china_list = china.extract_id()
    japan = FredData(country="japan")
    japan_list = japan.extract_id()
    eu = FredData(country="eu")
    eu_list = eu.extract_id()

import pandas as pd

url = {
    "ECB": "http://sdw-wsrest.ecb.europa.eu/service/data/"
}

class ECBData(object):
    def __init__(self) -> None:
        pass
    def get_data(dataset:str=None):
        tmp_url = url["ECB"] + "{}?format=csvdata".format(dataset)
        data = pd.read_csv(tmp_url)
        return data
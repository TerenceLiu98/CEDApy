import pandas as pd

class EurostatData(object):

    """
    for more information: https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=BulkDownload_Guidelines.pdf
    """

    def __init__(self, language:str="en"):
        self.language = language
        self.url = "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/"
        self.toc_url = "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&file=table_of_contents_{}.txt".format(language)

    __annotations__ = {"name": "eurostat",
                       "url": "https://ec.europa.eu/eurostat"}
    
    def toc(self) -> pd.DataFrame:
        """
        the return value includes 8 columns:
        'title'
        'code'
        'type'
        'last update of data'
        'last table structure change'
        'data start'
        'data end'
        'values'
        """
        toc = pd.read_csv(self.toc_url, sep="\t")
        return toc

    def search_toc(self, query:str=None):
        """
        fuzzy search in the "title"
        """
        toc = self.toc()
        if query == None:
            return ValueError("rex is invalid.")
        else:
            return toc[toc["title"].str.contains(query)].reset_index(drop=True)

    def download_data(self, datasetcode:str=None, geo:str=None, unit:str=None):
        url = self.url + "BulkDownloadListing?sort=1&file=data%2F" + datasetcode + ".tsv.gz"
        data = pd.read_csv(url, sep = "\t", compression="gzip")
        data = data.drop(data.columns[0], axis=1).join(data[data.columns[0]].str.split(",", expand=True))
        columns_list = list(data.columns)[:-3] + ["unit", "na_item", "geo"]
        data.columns = columns_list
        columns_list = columns_list[-3:] + columns_list[:-3]
        data = data[columns_list]
        if geo != None and unit != None:
            data = data.loc[(data["geo"] == geo) & (data["unit"] == unit)]
            for i in range(4, len(list(data.columns))):
                data[data.columns[i]] = data[data.columns[i]].astype(str).str.extract(r'(\d+.\d+)').astype("float")
            return data

        elif geo != None and unit == None:
            data = data.loc[(data["geo"] == geo)]
            for i in range(4, len(list(data.columns))):
                data[data.columns[i]] = data[data.columns[i]].astype(str).str.extract(r'(\d+.\d+)').astype("float")
            return data

        elif geo == None and unit != None:
            data = data.loc[(data["geo"] == geo)]
            for i in range(4, len(list(data.columns))):
                data[data.columns[i]] = data[data.columns[i]].astype(str).str.extract(r'(\d+.\d+)').astype("float")
            return data
        
        elif geo == None and unit == None:
            for i in range(4, len(list(data.columns))):
                data[data.columns[i]] = data[data.columns[i]].astype(str).str.extract(r'(\d+.\d+)').astype("float")
            return data

    def download_dic(self, category:str=None):
        url = self.url + "BulkDownloadListing?sort=1&file=dic%2F{}".format(self.language) + "%2F" + category + "dic"
        return pd.read_csv(url, sep="\t")



if __name__ == "__main__":
    eu = EurostatData(language="en")
    
    
        






    
    

    

import requests
import xmltodict
import pandas as pd

url = {
    "OECD":"https://stats.oecd.org/SDMX-JSON/data/",
    "OECD-Key": "https://stats.oecd.org/RestSDMX/sdmx.ashx/GetKeyFamily/all",
    "OECD-Schema": "http://stats.oecd.org/restsdmx/sdmx.ashx/GetSchema/"
}

class OECDData(object):
    def __init__(self, language:str="en"):
        self.language = language

    def toc(self) -> pd.DataFrame:
        tmp_url = url["OECD-Key"]
        r = requests.get(tmp_url)
        xpars = xmltodict.parse(r.text)
        KeyFamily = xpars['message:Structure']['message:KeyFamilies']['KeyFamily']
        FamilyID, FamilyName = [], []

        for key in KeyFamily:
            key_id = key["@id"]
            key_name = key["Name"]
            if isinstance(key_name, list):
                if self.language == "en":
                    key_name = key_name[0]["#text"]
                else:
                    key_name = key_name[1]["#text"]
            elif isinstance(key_name, dict):
                key_name = key_name["#text"]
            FamilyID.append(key_id)
            FamilyName.append(key_name)
            
        toc = pd.DataFrame({"FamilyID":FamilyID, "FamilyName":FamilyName})
        return toc


    def search_toc(self, query:str=None) ->pd.DataFrame:
        toc = self.toc()
        if query == None:
            return ValueError("rex is invalid.")
        else:
            return toc[toc["FamilyName"].str.contains(query)].reset_index(drop=True)
    
    def tos(self, dataset:str=None) -> dict:
        if dataset == None:
            return ValueError("ID is missing")
        else:
            tmp_url = url["OECD-Schema"] + dataset
            r = requests.get(tmp_url, timeout=10)
            xpars = xmltodict.parse(r.text)
            location = xpars['xs:schema']['xs:simpleType'][0]["xs:restriction"]["xs:enumeration"]
            transact = xpars['xs:schema']['xs:simpleType'][1]["xs:restriction"]["xs:enumeration"]
            measures = xpars['xs:schema']['xs:simpleType'][2]["xs:restriction"]["xs:enumeration"]
            frequencies = xpars['xs:schema']['xs:simpleType'][3]["xs:restriction"]["xs:enumeration"]

            code, fullname, transaction, fulltransaction  = [], [], [], []
            measure_list, full_measure, frequency_list, full_frequency = [], [], [], []

            for loc in location:
                locate = loc["@value"]
                name = loc["xs:annotation"]["xs:documentation"]
                if isinstance(name, list):
                    if self.language == "en":
                        name = name[0]["#text"]
                    else:
                        name = name[1]["#text"]
                elif isinstance(name, dict):
                        name = name["#text"]
                code.append(locate)
                fullname.append(name)

            for tran in transact:
                trans = tran["@value"]
                fulltrans = tran["xs:annotation"]["xs:documentation"]
                if isinstance(fulltrans, list):
                    if self.language == "en":
                        fulltrans = fulltrans[0]["#text"]
                    else:
                        fulltrans = fulltrans[1]["#text"]
                elif isinstance(fulltrans, dict):
                        fulltrans = fulltrans["#text"]
                transaction.append(trans)
                fulltransaction.append(fulltrans)

            for measure in measures:
                meas = measure["@value"]
                full_meas = measure["xs:annotation"]["xs:documentation"]
                if isinstance(full_meas, list):
                    if self.language == "en":
                        full_meas = full_meas[0]["#text"]
                    else:
                        full_meas = full_meas[1]["#text"]
                elif isinstance(full_meas, dict):
                        full_meas = full_meas["#text"]
                measure_list.append(meas)
                full_measure.append(full_meas)

            for frequency in frequencies:
                freq = frequency["@value"]
                full_freq = frequency["xs:annotation"]["xs:documentation"]
                if isinstance(full_freq, list):
                    if self.language == "en":
                        full_freq = full_freq[0]["#text"]
                    else:
                        full_freq = full_freq[1]["#text"]
                elif isinstance(full_freq, dict):
                        full_freq = full_freq["#text"]
                frequency_list.append(freq)
                full_frequency.append(full_freq)
            
            data = {
                "code":code,
                "fullname": fullname,
                "transaction_code": transaction,
                "transaction": fulltransaction,
                "measurement_code": measure_list,
                "measurement": full_measure,
                "frequency code": frequency_list,
                "frequency": full_frequency 
            }
            
            return data
    
    def download_data(self, dataset:str=None, query:str=None):
        tmp_url = url["OECD"] + "{}/".format(dataset) + query + "/all"
        r = requests.get(tmp_url)
        data =r.json()
        return data
        

if __name__ == "__main__":
    oecd = OECDData()
    oecd_toc = oecd.toc()
    oecd_tos = oecd.tos(dataset="QNA")
    data = oecd.download_data(dataset="QNA", query="QNA/CAN.B1_GE.CQRSA.Q")

                  

            
            









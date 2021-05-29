import requests

def config(http:str, https:str, auth:bool, user:str, passwd:str):
    if auth == False:
        proxies = {
            "http": "{}".format(http),
            "https": "{}".format(https)
        }
        return proxies
    if auth == True:
        proxies = {
            "http": "http://{}:{}@{}".format(user, passwd, http),
            "https": "https://{}:{}@{}".format(user, passwd, https),
        }
        return proxies
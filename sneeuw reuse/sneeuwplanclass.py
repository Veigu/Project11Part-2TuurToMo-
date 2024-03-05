import requests
import json


class Main():
    def __init__(self, zoutvoorraad, winter_budget):
        self.__zoutvoorraad = zoutvoorraad
        self.__winter_budget = winter_budget

    def getWeerbericht(self):
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast?lat=50.8798438&lon=4.7005176&appid=3dceda10dca633928a81220368dd3e1e&units=metric")
        response = response.json()
        return response

    def get_zoutvoorraad(self):
        return int(self.__zoutvoorraad)

    def get_winterbudget(self):
        return int(self.__winter_budget)

    def set_zoutvoorraad(self, value):
        self.__zoutvoorraad = value

    def get_winterbudget(self, value):
        self.__winter_budget = value
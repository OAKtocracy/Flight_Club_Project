import requests
import os

SHEETY_PUT_ENDPOINT = 'https://api.sheety.co/37a1f98088a6742b2fe5b4ce1a345ac1/flightDeals/prices/'
api_key = os.environ.get("api_key")

class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self, sheet_data):
        self.data_list = sheet_data
        self.api_key = api_key

    def update_iata_data(self):
        for row in self.data_list:
            sheety_put_ep = f"{SHEETY_PUT_ENDPOINT}{row['id']}"
            sheety_put_parameter = {'price': {'iataCode': row['iataCode']}}
            sheety_put = requests.put(url=sheety_put_ep, json=sheety_put_parameter)
            sheety_put.raise_for_status()

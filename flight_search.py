import requests
import datetime
from flight_data import FlightData
import os

sheety_get_ep = 'https://api.sheety.co/37a1f98088a6742b2fe5b4ce1a345ac1/flightDeals/prices'
sheety_get_request = requests.get(sheety_get_ep)
sheety_data = sheety_get_request.json()['prices']


tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
tomorrow_date = tomorrow.strftime('%d/%m/%Y')
six_months = tomorrow + datetime.timedelta(days=180)
six_months_date = six_months.strftime('%d/%m/%Y')

tequila_api_key = os.environ.get("teq_api_key")


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.affilid = 'abdulhafeezflightsearch'
        self.tequila_flight_location_endpoint = 'https://api.tequila.kiwi.com/locations/query'
        self.tequila_api_key = tequila_api_key
        self.tequila_header = {'apikey': self.tequila_api_key}
        self.tequila_check_flight_get_api = 'https://api.tequila.kiwi.com/v2/search'

    def get_iata_data(self, city_data):
        # this function will return the IATA names from tequila for the cities in Sheet data
        iata_data_dict = {}
        for city in city_data:
            tequila_location_get_parameter = {'term': city,
                                              'location_types': 'city',
                                              'limit': 100}
            tequila_get_request = requests.get(url=self.tequila_flight_location_endpoint,
                                               params=tequila_location_get_parameter,
                                               headers=self.tequila_header)
            tequila_get_request.raise_for_status()
            print(tequila_get_request.status_code)
            iata_data_dict[tequila_get_request.json()['locations'][0]['name']] = tequila_get_request.json()['locations'][0]['code']
        return iata_data_dict

    def check_flight(self, from_city, to_city, currency):
        tequila_check_flight_parameters = {'fly_from': from_city,
                                           'fly_to': to_city,
                                           'date_from': tomorrow_date,
                                           'date_to': six_months_date,
                                           'curr': currency,
                                           }
        check_flight_get = requests.get(url=self.tequila_check_flight_get_api, params=tequila_check_flight_parameters,
                                        headers=self.tequila_header)

        check_flight = check_flight_get.json()['data'][0]

        flight = FlightData(
            depart_date=check_flight['local_departure'].split('T')[0],
            return_date=check_flight['route'][0]['local_arrival'].split('T')[0],
            depart_city=check_flight['cityFrom'],
            dest_city=check_flight['cityTo'],
            depart_airp=check_flight['flyFrom'],
            dest_airp=check_flight['flyTo'],
            price=check_flight['price'])

        return flight

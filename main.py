from data_manager import DataManager
import flight_search
from notification_manager import NotificationManager
import functools


sheet_data = flight_search.sheety_data

cities = [_['city'] for _ in sheet_data]    # isolate the cities from the sheet data


f_search = flight_search.FlightSearch()
iata_search = f_search.get_iata_data(cities)         # search IATA codes for cities

for item in sheet_data:
    item['iataCode'] = iata_search[item['city']]

data_sheet = DataManager(sheet_data)
data_sheet.update_iata_data()


for dest in sheet_data:
    flight_details = f_search.check_flight(from_city="LON", to_city=dest['iataCode'], currency="GBP")

    flight_details_price = functools.reduce(lambda sub, ele: sub * 10 + ele, flight_details.price)

    if flight_details_price < dest["lowestPrice"]:
        text = NotificationManager()
        text.print_message(
            message=f"Low price alert! Only £{flight_details.price} to fly from"
                    f"{flight_details.from_city}-{flight_details.from_iata}"
                    f"to {flight_details.to_city}-{flight_details.to_iata},"
                    f"from {flight_details.from_date} to {flight_details.return_date}.")

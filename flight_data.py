class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, depart_city, depart_airp, dest_city, dest_airp, price, depart_date, return_date):
        self.from_city = depart_city,
        self.from_iata = depart_airp,
        self.to_city = dest_city,
        self.to_iata = dest_airp,
        self.price = price,
        self.from_date = depart_date,
        self.return_date = return_date

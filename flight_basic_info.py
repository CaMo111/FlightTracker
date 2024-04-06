import flightradar24
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from typing import Tuple
import math
import geopy.distance

import complex_state_method_refined

fr = flightradar24.Api()

'''
distances ✓
time ✓
    --> what time does the flight board?
    --> what time does the flight arrive
    --> 
plane information ✓
airports ✓
baggage delays
terminal + gate info
pilot info
map plotting (GUI)
'''

#OpenSky REST API could be of use
#time for planes is in UNIX TIME STAMP

'''
flight_info looks like this
a dictionary with result and _api 
{result: {request: 'somewhat useless shit', response: ['item', 'page', 'timestamp', 'data', 'aircraftInfo', 'aircraftImages'])}, {'_api': useless shit}}

To implement features;
    handle gates and baggage delays
    flight info
    flight type
    passenger count

'''

# dict_keys(['result', '_api'])
#print(flight_info.keys())
# a list of result: and _api:
#implement it so that it has common flights already going
#either input direct flight code
#or search and choose by use of webscraper then transfer that into flight information
# this is what where we get data from:
# print(flight_info['result']['response']['data'][0])
#       --> this contains the following information;
            #['identification', 'status', 'aircraft', 'owner', 'airline', 'airport', 'time'])
            #airport seems to have most crucial info where from and too 
            # maybe use of 'time' will help answer qeustions of if its on time

#print(flight_info['result']['response']['data'][0]['airport'])

class flight_path_info():
    def __init__(self, flightcode, icao24):
        self.ID = flightcode
        self.flight_info = fr.get_flight(self.ID)
        self.icao24 = icao24

        self.state_stamp = complex_state_method_refined.complex_state_vector_method(self.icao24)
        self.state_stamp.get_aircraft_details()

    def run_down_info(self, *args, **kwargs):
        
        self.origin_airport_name = self.flight_info['result']['response']['data'][0]['airport']['origin']['name']
        self.origin_airport_coords = (self.flight_info['result']['response']['data'][0]['airport']['origin']['position']['latitude'], self.flight_info['result']['response']['data'][0]['airport']['origin']['position']['longitude'])
        self.origin_airport_country = self.flight_info['result']['response']['data'][0]['airport']['origin']['position']['country']['name']
        self.og_city = self.flight_info['result']['response']['data'][0]['airport']['origin']['position']['region']['city']

        self.dest_airport_name = self.flight_info['result']['response']['data'][0]['airport']['destination']['name']
        self.dest_aiport_coords = (self.flight_info['result']['response']['data'][0]['airport']['destination']['position']['latitude'], self.flight_info['result']['response']['data'][0]['airport']['destination']['position']['longitude'])
        self.dest_airport_country = self.flight_info['result']['response']['data'][0]['airport']['destination']['position']['country']['name']
        self.dest_city = self.flight_info['result']['response']['data'][0]['airport']['destination']['position']['region']['city']

    def print_flight_rundown_info(self):

        print(f'Leaving from {self.origin_airport_name}, at {self.origin_airport_coords} from {self.origin_airport_country}, {self.og_city}.')
        print("\n")
        print(f'The destination is {self.dest_airport_name}. The coords are at {self.dest_aiport_coords}; in {self.dest_airport_country}, {self.dest_city}')
        print("\n")
        try:
            print(f"The plane is currently on lattitude {self.state_stamp.latitude} and longitude {self.state_stamp.longitude}. It is currently {self.state_stamp.altitude} metres high, travelling at a velocity of {self.state_stamp.velocity} metres a second.")
        except:
            print("iaco func fucked up")

'''
idinp = input(str("enter ID "))
icao24inp = input(str("enter icao24: "))
flight = flight_path_info(idinp, icao24inp)
flight.run_down_info()
'''
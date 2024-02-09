import flightradar24
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from typing import Tuple
import math
import geopy.distance
from mpl_toolkits.basemap import Basemap 
import matplotlib.pyplot as plt
import numpy as np
from itertools import chain
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import complex_state_method
from PyQt5.QtWidgets import QApplication, QSizePolicy, QWidget, QMainWindow, QMenu, QVBoxLayout, QSpinBox



fr = flightradar24.Api()

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
        self.state_stamp = complex_state_method.get_complex_aircraft_info(self.icao24)

        if self.state_stamp != None:
            self.callsign = self.state_stamp['Callsign']
            self.current_latitude = self.state_stamp['Latitude']
            self.current_longitude = self.state_stamp['Longitude']
            self.geo_altitude = self.state_stamp['Geo Altitude']
            self.ongroundbool = self.state_stamp['On Ground']
            self.velocity = self.state_stamp['Velocity']
            self.bearing = self.state_stamp['True Track']

    def run_down_info(self):
        input_id  = self.ID
        icao24_input = self.icao24

        path_instance = flight_path_info(input_id, icao24_input)
        
        path_instance.origin_airport_name = path_instance.flight_info['result']['response']['data'][0]['airport']['origin']['name']
        path_instance.origin_airport_coords = (path_instance.flight_info['result']['response']['data'][0]['airport']['origin']['position']['latitude'], path_instance.flight_info['result']['response']['data'][0]['airport']['origin']['position']['longitude'])
        path_instance.origin_airport_country = path_instance.flight_info['result']['response']['data'][0]['airport']['origin']['position']['country']['name']
        path_instance.og_city = path_instance.flight_info['result']['response']['data'][0]['airport']['origin']['position']['region']['city']

        path_instance.dest_airport_name = path_instance.flight_info['result']['response']['data'][0]['airport']['destination']['name']
        path_instance.dest_aiport_coords = (path_instance.flight_info['result']['response']['data'][0]['airport']['destination']['position']['latitude'], path_instance.flight_info['result']['response']['data'][0]['airport']['destination']['position']['longitude'])
        path_instance.dest_airport_country = path_instance.flight_info['result']['response']['data'][0]['airport']['destination']['position']['country']['name']
        path_instance.dest_city = path_instance.flight_info['result']['response']['data'][0]['airport']['destination']['position']['region']['city']

        #print(path_instance.flight_info['result']['response']['data'][0]['time'], "\n")
        print(f'Leaving from {path_instance.origin_airport_name}, at {path_instance.origin_airport_coords} from {path_instance.origin_airport_country}, {path_instance.og_city}.')
        print("\n")
        print(f'The destination is {path_instance.dest_airport_name}. The coords are at {path_instance.dest_aiport_coords}; in {path_instance.dest_airport_country}, {path_instance.dest_city}')
        print("\n")
        if path_instance.state_stamp != None:
            print(f"The plane is currently on lattitude {path_instance.current_latitude} and longitude {path_instance.current_longitude}. It is currently {path_instance.geo_altitude} metres high, travelling at a velocity of {path_instance.velocity} metres a second.")
        else:
            print(None)

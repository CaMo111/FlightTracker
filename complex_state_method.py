#import opensky_api
import requests
import json
#from pyopensky.rest import REST
 
'''
Going to use REST API client since we are not authenticated through OPENSKY
as a user lulw

flightradar24 api; airports too and from
opensky_api; complex information as in state vector of where plane currently is 
googles distance_matrix api; calculate travel times and distances for multiple destinations

map usage should be contextily

Created a class instance of API client
Create an instance of the API client. If you do not provide username
and password requests will be anonymous which imposes some limitations.

Python scripts to load and visualize OpenSky Network and FlightRadar air traffic data

Distance Matrix API - Google --> Get the travel distance and time for a
 matrix of origins and destinations.
 This can be used to calculate how far from and to, as well as the time it would 
 take to get between the state vector and the destination or departure airports.

  Live ADS-B Data API

    Rest API
    Representational State Transfer (REST()) --> About communication, client to server;
        'restful' web service is a service that uses rest API's to communicate
        Request send from client to server --> Me sending the Icao24 code to opensky data base
        Response sent from server back to the client. --> client sending information about state vector back to me.
'''
class complex_state_method():

    def __init__(self, input_code):
        self.input_code = input_code

    def call_for_state_vector(self):
        url = f"https://opensky-network.org/api/states/all?icao24={self.input_code}&time=0"

        response = requests.get(url)
        data = response.json()
        #print(data)

        if data["states"]:
            aircraft = data["states"][0]

            # get relevant information
            icao = aircraft[0]
            callsign = aircraft[1]
            origin_country = aircraft[2]
            time_position = aircraft[3]
            last_contact = aircraft[4]
            longitude = aircraft[5]
            latitude = aircraft[6]
            altitude = aircraft[7]
            on_ground = aircraft[8]
            velocity = aircraft[9]
            true_track = aircraft[10]
            vertical_rate = aircraft[11]
            sensors = aircraft[12]
            baro_alt = aircraft[13]
            squawk = aircraft[14]
            spi = aircraft[15]
            position_source = aircraft[16]
    
            return {
                'ICAO24': icao,
                # Unique identifier for the aircraft
                'Callsign': callsign,
                # Callsign of the aircraft
                'Latitude': latitude,
                # Latitude of the aircraft's current position
                'Longitude': longitude,
                # Longitude of the aircraft's current position
                'Geo Altitude': altitude,
                # Altitude above sea level in meters
                'On Ground': on_ground,
                # Boolean indicating whether the aircraft is on the ground or not
                'Velocity': velocity,
                # Velocity of the aircraft in meters per second
                'True Track': true_track,
                # Heading of the aircraft in degrees from North
                'Origin': origin_country,
                # Origin country 
            }
        else:
            print("kys")
            
# Call the function with the icao24 identifier "icao24"
    
flight = complex_state_method('a0e250')
flight.call_for_state_vector()


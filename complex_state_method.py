import opensky_api
import requests
import json
 
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

'''

def get_complex_aircraft_info(input_code):
    # Create an instance of the OpenSkyApi class with the provided username and password
    # right now i dont have an account so i cant even collect the state snap shot
    # kms
    api = opensky_api.OpenSkyApi()
    input_code = input_code.lower()
    # Get the states for the aircraft with the specified icao24 identifier
    states = api.get_states(icao24=input_code)

    # Check if there are any states returned
    if states.states:
        # If there are states, select the first one
        sv = states.states[0]
        # Return the state information as a dictionary
        return {
            'ICAO24': sv.icao24,
            # Unique identifier for the aircraft
            'Callsign': sv.callsign,
            # Callsign of the aircraft
            'Latitude': sv.latitude,
            # Latitude of the aircraft's current position
            'Longitude': sv.longitude,
            # Longitude of the aircraft's current position
            'Geo Altitude': sv.geo_altitude,
            # Altitude above sea level in meters
            'On Ground': sv.on_ground,
            # Boolean indicating whether the aircraft is on the ground or not
            'Velocity': sv.velocity,
            # Velocity of the aircraft in meters per second
            'True Track': sv.true_track,
            # Heading of the aircraft in degrees from North
        }
    else:
        # If there are no states returned, return None
        return None
# Call the function with the icao24 identifier "icao24"


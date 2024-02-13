from flight_basic_info import flight_path_info
import json 
import requests
from haversine import haversine, Unit
#This python file is for calculating flight time between og departure to
#destination.

#as well as this it will calculate the time between its
# state vector location to destination and departure.

'''
 flight travel time is directly correlated to distance.
 This is because flights are mostly directlines between
 source and destination. Thus, you can use the Google API
 Distance matrix to calculate distance between points,
 then divide by the averagespeed of commercial flights,
 which is ~550mph. then, you get your flight time.

 plan changed --> google api for some reason didn't work with the place ID requests so instead using
 haversine module to collect distance and time manually. Its fine though it does the same thing
 and now i've generated place ID which i guess is good anyway?

 
'''

class traversal_time():
    matrix_api_key = "AIzaSyC1nPitf9YZMZGjYYjoa-8h406otFv7QZc"

    def __init__(self, flight_path: flight_path_info):
        self.path_instance = flight_path
        self.path_instance.run_down_info()
        #matrix_api_key = "AIzaSyC1nPitf9YZMZGjYYjoa-8h406otFv7QZc"

#this will call the flight path info with two pieces of information

    def calculate_time(self):
 
        state_vector_placeurl = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={self.path_instance.state_stamp.latitude},{self.path_instance.state_stamp.longitude}&key=AIzaSyC1nPitf9YZMZGjYYjoa-8h406otFv7QZc"
        flight_placeid_statevector_request = requests.get(state_vector_placeurl)
        dictionary_output = flight_placeid_statevector_request.json()
        state_vector_place_id = dictionary_output['results'][0]['place_id']

        dest_coords_placeurl = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={self.path_instance.dest_aiport_coords[0]},{self.path_instance.dest_aiport_coords[1]}&key=AIzaSyC1nPitf9YZMZGjYYjoa-8h406otFv7QZc"
        og_coords_placeurl = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={self.path_instance.origin_airport_coords[0]},{self.path_instance.origin_airport_coords[1]}&key=AIzaSyC1nPitf9YZMZGjYYjoa-8h406otFv7QZc"

        dest_place_req = requests.get(dest_coords_placeurl)
        dest_place_req_output = dest_place_req.json()
        dest_place_id = dest_place_req_output['results'][0]['place_id']
        og_place_req = requests.get(og_coords_placeurl)
        og_place_req_output = og_place_req.json()
        og_place_id = og_place_req_output['results'][0]['place_id']

        self.place_id_dictionary = {
            'state_vector_placeid' : state_vector_place_id,

            'destination_placeid' : dest_place_id,

            'origin_placeid' : og_place_id
        }


        self.coordinate_dictionary = {
            'state_vector_coords' : (self.path_instance.state_stamp.latitude, self.path_instance.state_stamp.longitude),
            'dest_coords' : self.path_instance.dest_aiport_coords,
            'og_coords' : self.path_instance.origin_airport_coords
        }

        state_vector_to_dest_distance = haversine(self.coordinate_dictionary['state_vector_coords'], self.path_instance.dest_aiport_coords)
        og_to_dest_distance = haversine(self.path_instance.origin_airport_coords, self.path_instance.dest_aiport_coords)
        og_to_state_vector_distance = haversine(self.path_instance.origin_airport_coords, self.coordinate_dictionary['state_vector_coords'])

        print(state_vector_to_dest_distance, og_to_dest_distance, og_to_state_vector_distance)

        self.time_travelled = (og_to_state_vector_distance / self.path_instance.state_stamp.velocity_kmh)
        self.total_travel_time = (og_to_dest_distance / 900)
        self.time_remaining = (state_vector_to_dest_distance / self.path_instance.state_stamp.velocity_kmh)

        print(self.time_remaining)

idinp = input(str("enter ID "))
icao24inp = input(str("enter icao24: "))
flight = flight_path_info(idinp, icao24inp)
flight_times = traversal_time(flight)
flight_times.calculate_time()
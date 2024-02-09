import flight_basic_info
import json 
import requests
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

 origin and dest must use place ID since coordinates will snap to closest road.
 
'''

matrix_api_key = "AIzaSyC1nPitf9YZMZGjYYjoa-8h406otFv7QZc"

#this will call the flight path info with two pieces of information
idinp = input(str("enter ID "))
icao24inp = input(str("enter icao24: "))
path_instance = flight_basic_info.flight_path_info(idinp,icao24inp)

#flight_basic_info.run_down_info()

placeurl = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={path_instance.current_latitude},{path_instance.current_longitude}&key=AIzaSyC1nPitf9YZMZGjYYjoa-8h406otFv7QZc"

flight_placeid_statevector_request = requests.get(placeurl)
#print(flight_placeid_statevector_request)
dictionary_output = flight_placeid_statevector_request.json()

state_vector_place_id = dictionary_output['results'][0]['place_id']
#print(dictionary_output['results'][0]['place_id'])
#print(dictionary_output.keys())
print(state_vector_place_id)

path_instance.run_down_info()

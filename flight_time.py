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
path_instance.run_down_info()

 
state_vector_placeurl = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={path_instance.state_stamp.latitude},{path_instance.state_stamp.longitude}&key=AIzaSyC1nPitf9YZMZGjYYjoa-8h406otFv7QZc"
flight_placeid_statevector_request = requests.get(state_vector_placeurl)
dictionary_output = flight_placeid_statevector_request.json()
state_vector_place_id = dictionary_output['results'][0]['place_id']

dest_coords_placeurl = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={path_instance.dest_aiport_coords[0]},{path_instance.dest_aiport_coords[1]}&key=AIzaSyC1nPitf9YZMZGjYYjoa-8h406otFv7QZc"
og_coords_placeurl = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={path_instance.origin_airport_coords[0]},{path_instance.origin_airport_coords[1]}&key=AIzaSyC1nPitf9YZMZGjYYjoa-8h406otFv7QZc"

dest_place_req = requests.get(dest_coords_placeurl)
dest_place_req_output = dest_place_req.json()
dest_place_id = dest_place_req_output['results'][0]['place_id']
og_place_req = requests.get(og_coords_placeurl)
og_place_req_output = og_place_req.json()
og_place_id = og_place_req_output['results'][0]['place_id']

place_id_dictionary = {
    'state_vector_placeid' : state_vector_place_id,

    'destination_placeid' : dest_place_id,

    'origin_placeid' : og_place_id
}

print(place_id_dictionary)

#now we have PLACE ID we can simply use matrix api to calculate distance between place id 

state_vector_to_finaldest_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations=place_id:{place_id_dictionary['destination_placeid']}&origins=place_id:{place_id_dictionary['state_vector_placeid']}&units=imperial&key=AIzaSyC1nPitf9YZMZGjYYjoa-8h406otFv7QZc"
state_vector_to_finaldest_req = requests.get(state_vector_to_finaldest_url)
state_vector_to_finaldest_output = state_vector_to_finaldest_req.json()
print(state_vector_to_finaldest_output)

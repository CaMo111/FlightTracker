import requests
import time

class complex_state_vector_method():

    def __init__(self, icao24input):
        self.icao24 = icao24input.lower()

    def get_aircraft_details(self): 
        url = f"https://opensky-network.org/api/states/all?icao24={self.icao24}&time=0"
        try:
            response = requests.get(url)
            data = response.json()
            #print(data)

            if data["states"]:
                aircraft = data["states"][0]

                # get relevant information
                self.icao = aircraft[0]
                self.callsign = aircraft[1]
                self.origin_country = aircraft[2]
                self.time_position = aircraft[3]
                self.last_contact = aircraft[4]
                self.longitude = aircraft[5]
                self.latitude = aircraft[6]
                self.altitude = aircraft[7]
                self.on_ground = aircraft[8]
                self.velocity = aircraft[9]
                self.true_track = aircraft[10]
                self.vertical_rate = aircraft[11]
                self.sensors = aircraft[12]
                self.baro_alt = aircraft[13]
                self.squawk = aircraft[14]
                self.spi = aircraft[15]
                self.position_source = aircraft[16]
                self.velocity_kmh = (self.velocity * 3.6)

                print(f" \n The plane is currently on lattitude {self.latitude} and longitude {self.longitude}. \nIt is currently {self.altitude} metres high, travelling at a velocity of {self.velocity} metres a second. \n \n Complex State Vector Information:")

                return {
                'ICAO24': self.icao,
                # Unique identifier for the aircraft
                'Callsign': self.callsign,
                # Callsign of the aircraft
                'Latitude': self.latitude,
                # Latitude of the aircraft's current position
                'Longitude': self.longitude,
                # Longitude of the aircraft's current position
                'Geo Altitude': self.altitude,
                # Altitude above sea level in meters
                'On Ground': self.on_ground,
                # Boolean indicating whether the aircraft is on the ground or not
                'Velocity': self.velocity,
                # Velocity of the aircraft in meters per second
                'Velocity_kmh': self.velocity_kmh,
                # Velocity of aircraft in kmh
                'True Track': self.true_track,
                # Heading of the aircraft in degrees from North
                'Origin': self.origin_country,
                # Origin country 
                'time_pos' : self.time_position,
                #Unix timestamp (seconds) for the last position update. Can be null if no position report was received by OpenSky within the past 15s.
                'last_contact': self.last_contact,
                #Unix timestamp (seconds) for the last update in general. This field is updated for any new, valid message received from the transponder.
                'vertical_rate' : self.vertical_rate,
                # Vertical rate in m/s. A positive value indicates that the airplane is climbing, a negative value indicates that it descends. Can be null.
                'sensors' : self.sensors,
                # IDs of the receivers which contributed to this state vector. Is null if no filtering for sensor was used in the request
                'baro_altitude': self.baro_alt,
                # Barometric altitude in meters. Can be null.
                'transponder code': self.squawk,
                #The transponder code aka Squawk. Can be null.
                'special purpose indicator': self.spi,
                # Whether flight status indicates special purpose indicator.
                'position_source' : self.position_source
                # Origin of this state’s position. 0 = ADS-B; 1 = ASTERIX; 2 = MLAT; 3 = FLARM
            }

            else:
                print("No information available for the provided ICAO 24-bit address.")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")


icao24inp = input(str("enter icao24: "))
flight = complex_state_vector_method(icao24inp)
print(flight.get_aircraft_details())
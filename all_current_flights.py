#file that retreives db of all active flights
import requests

def generate_all_flights_vectors():
    url = "https://opensky-network.org/api/states/all?icao24"
    response = requests.get(url)
    data = response.json()
    #print(data)
    res = []

    twoD_Array = data['states']

    for lsts in twoD_Array:
        if lsts[8] == False:
            if lsts[6] != None and lsts[5] != None:
                res.append(lsts[5:7])
                res.append(lsts[0])

    #these are all long, lat, iacocode
    #print(res)
    return res
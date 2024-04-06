from flask import Flask, render_template
import folium
import all_current_flights
'''
app = Flask(__name__)

@app.route('/')
def main():
    return 'Hello main!'

if __name__ == '__main__':
    app.run()
'''
def create_app():
    app = Flask(__name__)
    return app

app = create_app()

@app.route("/")
def index():
    map = folium.Map(location=[0,0], zoom_start=3
                     )
    
    twod_array = all_current_flights.generate_all_flights_vectors()

    for location_info in twod_array:
        print(location_info)
        lat = location_info[1]
        lon = location_info[0]
        iaco_code = location_info[2]
        folium.Marker([lat, lon], popup=f"IACO: {iaco_code}").add_to(map)

    return map._repr_html_()

if __name__ == "__main__":
    app.run()
import streamlit as st
import requests
import math
import pickle


model = pickle.load(open("estimator.pkl", "rb"))


st.image("innomatics-research-labs-logo-squared.png")
st.title("Estimation Time of Arrival")


options1 = ['Rainy', 'Foggy', 'Clear']
options2 = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# getting latitude and longitude using area, city, and country name
def get_lat_long(area_name, city_name, country_name):
    url = f"https://nominatim.openstreetmap.org/search?q={area_name},{city_name},{country_name}&format=json"
    request_header = {
        'Content-Type': 'text/html; charset=UTF-8',
        'User-Agent': 'Chrome/101.0.0.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    response = requests.get(url, headers=request_header)
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = data[0]['lat']
            lng = data[0]['lon']
            return float(lat), float(lng)
        else:
            return None, None
    else:
        st.error(f"Error: {response.status_code}")
        return None, None

# calculating distance using latitude and longitudes
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371 
    return r * c


start_area = st.text_input("Enter the starting area name: ")
end_area = st.text_input("Enter the destination area name: ")
city_name = "Hyderabad"
country_name = "India"


start_lat, start_long = get_lat_long(start_area, city_name, country_name)
end_lat, end_long = get_lat_long(end_area, city_name, country_name)

if start_lat and start_long and end_lat and end_long:
    st.write(f"Starting Latitude: {start_lat}, Longitude: {start_long}")
    st.write(f"Destination Latitude: {end_lat}, Longitude: {end_long}")

    
    distance = haversine(start_lat, start_long, end_lat, end_long)
    st.write(f"Approximate Distance: {round(distance)} km")
else:
    st.warning("Please ensure both starting and destination areas are valid.")


traffic_density = st.slider("Enter traffic density:", min_value=1, max_value=10, value=5)


weather = st.selectbox("Please provide weather condition:", options1)
day = st.selectbox("Enter the day:", options2)
hour = st.selectbox("Enter the hour:", range(24))


day_of_week = options2.index(day) + 1
weather_numerical = 1 if weather == "Rainy" else 2 if weather == "Foggy" else 3


if st.button("Submit") and start_lat and start_long and end_lat and end_long:
    time = model.predict([[distance, traffic_density, weather_numerical, day_of_week, hour]])
    st.write(f"The Estimated time is {time[0]:.2f} minutes")

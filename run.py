# Import required libraries
from geopy.geocoders import Nominatim
import requests


def get_location(city, country):
    """
    This function returns a string of the form City, Country
    """
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="VictoriasApp")

    # Get location
    location = geolocator.geocode(f"{city}, {country}")

    latitude = location.latitude
    longitude = location.longitude
    return latitude, longitude


print('Dear user, in order to obtain the weather information, \
please enter the city and country of your choice.')

city = input('City: ')
country = input('Country: ')

print(f"You have entered the following location: {city}, {country}")

city_country = get_location(city, country)
print(city_country)
# # Path: run.py
# def get_weather(latitude, longitude):
#     """
#     This function returns the weather for a given latitude and longitude
#     """
#     # Initialize DarkSky API
#     darksky = DarkSky(API_KEY)

#     # Get weather
#     weather = darksky.get_forecast(latitude, longitude)
#     return weather

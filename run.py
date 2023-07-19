# Import required libraries
from geopy.geocoders import Nominatim
import requests
from datetime import date
from termcolor import colored

# Defining Welcome message function


def welcome():
    """
    This function prints a welcome message to the user
    """
    print(colored('Welcome to Victoria\'s Weather App!', 'green'))
    print(colored('This app will provide you with the weather \
    information you need.', 'green'))
    print(colored('Please enter the city and country of your choice.', 'green'))
    print(colored('Enjoy!', 'green'))


def get_location(city, country):
    """
    This function returns a string of the form City, Country
    """
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="VictoriasApp")

    # Get location
    location = geolocator.geocode(f"{city}, {country}")

    latitude = str(location.latitude)
    longitude = str(location.longitude)
    return latitude, longitude


print('Dear user, in order to obtain the weather information, \
please enter the city and country of your choice.')

city = input('City: ')
country = input('Country: ')

print(f"You have entered the following location: {city}, {country}")

city_country = get_location(city, country)
print(city_country)

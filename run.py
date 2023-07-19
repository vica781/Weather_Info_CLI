# Import required libraries
from geopy.geocoders import Nominatim
import requests
from datetime import date
from termcolor import colored


# Defining Welcome message function
def welcome_nessage():
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


# Defining get_weather function
def get_weather(latitude, longitude):
    """
    This function returns the current weather information
    """
    # Define constants
    BASE_URL = 'https://api.open-meteo.com/v1/forecast?'
    # Define parts of the URL
    LATITUDE_PART = 'latitude='
    LONGITUDE_PART = '&longitude='
    # Define closing part of the URL
    CLOSING_PART = '&hourly=temperature_2m,relativehumidity_2m, \
    surface_pressure, visibility&daily=sunrise,sunset,uv_index_max, \
    precipitation_probability_max, \
    winddirection_10m_dominant&windspeed_unit=ms&timezone=GMT'
    # Define URL
    URL = BASE_URL + LATITUDE_PART + latitude + \
        LONGITUDE_PART + longitude + CLOSING_PART
    # Get data from API
    response = requests.get(URL)
    # Check if the response is successful
    if response.status_code == 200:
        # Print success message
        print('Success! Everything is okay. I got the data!')
        # Get data
        data = response.json()
        # Get current date
    else:
        # Print error message
        print('Oops! Something went wrong. Please try again later.')
        # Return None
        data = None
    return data


print('Dear user, in order to obtain the weather information, \
please enter the city and country of your choice.')

city = input('City: ')
country = input('Country: ')

print(f"You have entered the following location: {city}, {country}")

city_country = get_location(city, country)
print(city_country)

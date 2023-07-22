# Import required libraries
from geopy.geocoders import Nominatim
import requests
import datetime
from termcolor import colored


# Defining Welcome message function
def welcome_message():
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


# Define constants
BASE_URL = 'https://api.open-meteo.com/v1/forecast?'
# Define parts of the URL
LATITUDE_PART = 'latitude='
LONGITUDE_PART = '&longitude='
# Define closing part of the URL
CLOSING_PART = '&hourly=temperature_2m,relativehumidity_2m,\
precipitation_probability,surface_pressure,visibility,windspeed_10m,\
winddirection_10m,windgusts_10m&daily=temperature_2m_max,temperature_2m_min,\
sunrise,sunset,uv_index_max,\
precipitation_probability_max&windspeed_unit=ms&timezone=GMT'


# Defining get_weather function
def get_weather(latitude, longitude):
    """
    This function returns the current weather information
    """
    global LATITUDE_PART, LONGITUDE_PART, CLOSING_PART
    # Define URL
    url = BASE_URL + LATITUDE_PART + latitude + \
        LONGITUDE_PART + longitude + CLOSING_PART

    # Get data from API
    response = requests.get(url)
    # Check if the response is successful
    # If successful, get data
    # 200 is the HTTP status code for "OK" used for data communication \
    # on the web (https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)

    if response.status_code == 200:
        # Print success message
        print('Success! Everything is okay. I got the data!')
        # Get data
        data = response.json()
        # Get current date
    else:
        # Print error message
        print('Oops! Something went wrong. Please try again later.')
        # Return None if the response is enything other then successful
        data = None
    return data


# Defining print_weather function
def print_weather(data):
    """
    This function prints the weather information
    """
    # calculate index for current hour and current date
    now = str(datetime.datetime.now()).split()
    now_time = now[0] + 'T' + now[1][:2] + ':00'
    hourly_index = data['hourly']['time'].index(now_time)
    daily_index = data['daily']['time'].index(
        str(datetime.datetime.now()).split()[0])

    if data is not None:
        # Hourly requests
        # Get current temperature
        current_temperature = data['hourly']['temperature_2m'][hourly_index]
        # Get current humidity
        current_humidity = data['hourly']['relativehumidity_2m'][hourly_index]
        # Get current precipitation probability
        current_precipitation_probability = data['hourly'][
            'precipitation_probability'][hourly_index]
        # Get current pressure
        current_pressure = data['hourly']['surface_pressure'][hourly_index]
        # Get current visibility
        current_visibility = data['hourly']['visibility'][hourly_index]
        # Get curreent windspeed
        current_windspeed = data['hourly']['windspeed_10m'][hourly_index]
        # Get current wind direction
        current_winddirection = data['hourly'][
            'winddirection_10m'][hourly_index]
        # Get current wind gusts
        current_windgusts = data['hourly']['windgusts_10m'][hourly_index]

        # Daily requests
        # Get current sunrise
        current_sunrise = data['daily']['sunrise'][daily_index]
        # Get current sunset
        current_sunset = data['daily']['sunset'][daily_index]
        # Get current UV index
        current_uv_index = data['daily']['uv_index_max'][daily_index]
        # Get current precipitation probability
        current_precipitation_probability = data['daily']['precipitation_probability_max'][daily_index]
        # Get current wind direction
        # current_wind_direction = data['daily']['winddirection_10m_dominant'][daily_index]
        # Get current wind speed
        # current_wind_speed = data['daily']['windspeed_10m'][daily_index]
        # Print current temperature
        print(
            f"The current temperature is {current_temperature} degrees Celsius")
        # Print current humidity
        print(f"The current humidity is {current_humidity} %")
        # Print current pressure
        print(f"The current pressure is {current_pressure} hPa")
        # Print current visibility
        print(f"The current visibility is {current_visibility} m")
        # Print current sunrise
        print(f"The current sunrise is at {current_sunrise}")
        # Print current sunset
        print(f"The current sunset is at {current_sunset}")
        # Print current UV index
        print(f"The current UV index is {current_uv_index}")
        # Print current precipitation probability
        print(
            f"The current precipitation probability is {current_precipitation_probability} %")
        # Print current wind direction
        # print(
        #     f"The current wind direction is {current_wind_direction} degrees")
        # # Print current wind speed
        # print(f"The current wind speed is {current_wind_speed} m/s")
    else:
        # Print error message
        print('Oops! Something went wrong. Please try again later.')
        # Return None if the response is enything other then successful
        data = None


# Call welcome message function
welcome_message()
city = input('City: ')
country = input('Country: ')
# Call get_location function
latitude, longitude = get_location(city, country)
# Call get_weather function
data = get_weather(latitude, longitude)

print('Dear user, in order to obtain the weather information, \
please enter the city and country of your choice.')

# city = input('City: ')
# country = input('Country: ')

# city_country = get_location(city, country)
# print(city_country)

print(f"You have entered the following location: {city}, {country}")
print('Please wait while I am getting the weather information for you...')
print('This may take a few seconds...')
print('Thank you for your patience!')
print(f'Here is the weather information for {city}, {country}:')
print_weather(data)

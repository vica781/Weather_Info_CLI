# Import required libraries
from geopy.geocoders import Nominatim
import requests
import datetime
from termcolor import colored
import readchar
import os
import time

MENU = [
    'a. Weather information for the location of your choice',
    'b. Go here if you want to learn about the Weather Components and Units',
    'c. Previous Searches Display',
    'd. Information about this app',
    'e. Exit'
]


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
BANNER_INPUT = """
.----..-. .-..----..----..-.  .-.    .---. .-.    .----. .-. .-..----.     
| {_  | | | || {_  | {}  }\ \/ /    /  ___}| |   /  {}  \| { } || {}  \   
| {__ \ \_/ /| {__ | .-. \ }  {     \     }| `--.\      /| {_} ||     /   
`----' `---' `----'`-' `-' `--'      `---' `----' `----' `-----'`----'     
.-. .-.  .--.   .----.     .--.      .----..-..-.   .-. .-..----..----.     
| {_} | / {} \ { {__      / {} \    { {__  | || |   | | | || {_  | {}  }   
| { } |/  /\  \.-._} }   /  /\  \   .-._} }| || `--.\ \_/ /| {__ | .-. \   
`-' `-'`-'  `-'`----'    `-'  `-'   `----' `-'`----' `---' `----'`-' `-'    
.-.   .-..-. .-..-..-. .-. .---. 
| |   | ||  `| || ||  `| |/   __}
| `--.| || |\  || || |\  |\  {_ }
`----'`-'`-' `-'`-'`-' `-' `---' 
"""
BANNER_INTRO = """            					
    .        .      /				
      \      |     .				
             oo  /
        \ ,oOOO__== --__ =-
.____ -__. OoOO(`  )).                   _
____. __  OOO(o    )). __ . __--    .+(`  )`.
)        oOOO(o      '`.          :(   .    )
        .+(`(      .   ))    .--  `.  (    ) )
       ((    (..__.:'-'   .=(   )   ` _`  ) )
`.     `(       ) )       (   .  )     (   )  ._
  )      ` __.:'   )     (   (   ))     `-'.:(`  )
)  )  ( )       --'       `- __.'         :(      ))
.-'  (_.'          .')                    `(    )  ))
--..,___.--,--'`,---..-.--+--.,,-,,..._.--..-._.-a:f--.
"""
BANNER_RAIN = """
      __I__
   .-'"  .  "'-.
 .'  / . ' . \  '.
/_.-..-..-..-..-._\ .---------------------------------.
         #  _,,_   ( I hear it might rain people today )
         #/`    `\ /'---------------------------------'
         / / 6 6\ \
         \/\  Y /\/       /\-/\
         #/ `'U` \       /a a  \               _
       , (  \   | \     =\ Y  =/-~~~~~~-,_____/ )
       |\|\_/#  \_/       '^--'          ______/
       \/'.  \  /'\         \           /
        \    /=\  /         ||  |---'\  \
        /____)/____)       (_(__|   ((__|
"""


def key_pressed():
    """
    This function waits for a key to be pressed
    """
    print('Press any key to continue...')
    key = readchar.readkey()
    return


def clear_screen():
    """
    This function clears the screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    return


# Defining Welcome message function
def welcome_message():
    """
    This function prints a welcome message to the user
    """
    print(colored('Welcome to Victoria\'s Weather App!'.upper(), 'green'))
    print(colored(BANNER_INTRO, 'yellow'))
    print(colored('This app will provide you with the weather \
information for the location of your choice.', 'green'))
#     print(colored('In order to obtain the weather information, \
# please enter the city and country.', 'yellow'))
    print(colored('Enjoy!', 'green'))


lines = BANNER_INPUT.split()

# Define name_input function


def name_input():
    """
    This function asks for the user's name
    """
    # Print banner
    for line in BANNER_INPUT.splitlines():
        for character in line:
            print(colored(character, 'yellow'), end='', flush=True)
            # delay printing of each character by 0.05 seconds
            # time.sleep(.009)
        print('')  # print a new line
        time.sleep(0.5)  # delay printing of each line by 0.5 seconds

    # Ask for name
    name = input("""Choose a name - it must be at least 3 characters long, 
but no longer than 10 characters, include only letters, 
no numbers or special characters: """)
    # Check if the name is valid
    while len(name) < 3 or len(name) > 10 or not name.isalpha():
        print(colored('Oops! Something went wrong. Please try again.', 'red'))
        name = input('Choose a name - it must be at least 3 characters long,\
\nbut no longer than 10 characters, include only letters,\
\nno numbers or special characters: ')
    print()
    print()
    # Print welcome message
    print(colored(f"Hello,{name}! {'come rain or shine'.upper()},\
\nI wish you to be on a {'cloud nine'.upper()} \
\nand everything you do {'to be a breeze!'.upper()}", 'green'))
    return name


# Defining get_location function
def get_location(city, country):
    """
    This function returns a string of the form City, Country
    """
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="VictoriasApp")
    # Get location
    location = geolocator.geocode(f"{city}, {country}")
    if location is None:
        # Print error message
        print(colored('Oops! Something went wrong.\
 Please try again later.', 'red'))
        exit()
    # Get latitude and longitude
    latitude = str(location.latitude)
    longitude = str(location.longitude)
    return latitude, longitude


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
        # Get data in JSON format
        data = response.json()
        # Return data
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
        # Get current maximum temperature
        current_temperature_max = data['daily'][
            'temperature_2m_max'][daily_index]
        # Get current minimum temperature
        current_temperature_min = data['daily'][
            'temperature_2m_min'][daily_index]
        # Get current sunrise
        current_sunrise = data['daily']['sunrise'][daily_index]
        # Get current sunset
        current_sunset = data['daily']['sunset'][daily_index]
        # Get current UV index
        current_uv_index = data['daily']['uv_index_max'][daily_index]
        # Get current precipitation probability
        current_precipitation_probability = data['daily'][
            'precipitation_probability_max'][daily_index]

        # Print hourly requests
        # Print current temperature
        print(
            f"The current temperature is {current_temperature}\u00b0 C")
        # Print current humidity
        print(f"The current relative humidity is {current_humidity} %")
        # Print current precipitation probability
        print(
            f"The current precipitation probability is {current_precipitation_probability} %")
        # Print current surface pressure
        print(f"The current surface pressure is {current_pressure} hPa")
        # Print current visibility
        print(f"The current visibility is {current_visibility} km")
        # Print current windspeed
        print(f"The current windspeed is {current_windspeed} m/s")
        # Print current wind direction
        print(f"The current wind direction is {current_winddirection}")
        # Print current wind gusts
        print(f"The current wind gusts are {current_windgusts} m/s")

        # Print daily requests
        # Print daily maximum temperature
        print(
            f"The daily maximum temperature is {current_temperature_max}\u00b0 C")
        # Print daily minimum temperature
        print(
            f"The daily minimum temperature is {current_temperature_min}\u00b0 C")
        # Print sunrise
        print(f"The sunrise is at {current_sunrise}")
        # Print sunset
        print(f"The sunset is at {current_sunset}")
        # Print UV index
        print(f"The UV index is {current_uv_index}")
        # Print precipitation probability
        print(
            f"The maximum daily precipitation probability is {current_precipitation_probability} %")
    else:
        # Print error message
        print('Oops! Something went wrong. Please try again later.')
        # Return None if the response is enything other then successful
        data = None


def main():
    # Call welcome message function
    welcome_message()
    print()
    # Call key_pressed function
    key_pressed()
    # Call clear_screen function
    clear_screen()
    # Call name_input function
    name = name_input()
    print()
    key_pressed()
    clear_screen()
    # Ask for city and country
    print(colored(f'Hello, {name}! In order to obtain the weather information, \
please enter the city and country of your choice.', 'green'))
    print()
    print()
    city = input('City: ')
    country = input('Country: ')
    # Call get_location function
    latitude, longitude = get_location(city, country)
    # TODO - add a check if the location is valid
    print()
    print()
    # Print weather information
    print(colored(f"You have entered the following location: \
{city}, {country}", 'yellow'))
    print()
    print()

    print('Please wait while I am getting the weather information for you...')
    print('This may take a few seconds...')
    print('Thank you for your patience!')
    print()
    print()
    # Call get_weather function
    data = get_weather(latitude, longitude)
    # Print success message
    print(colored('Success! Everything is okay. I got the data!', 'blue'))
    print()
    key_pressed()
    clear_screen()

    print(
        colored(f'Here is the weather information for {city}, {country}:', 'cyan'))
    # Call print_weather function
    print_weather(data)

    print()
    key_pressed()
    clear_screen()

    # Menu section
    while True:
        clear_screen()
        print('\n M E N U\n\n'.center(80, '-'))
        for item in MENU:
            print(item + '\n')

            menu_choices = ''
            while menu_choices == '':
                menu_choices = input(colored('Please, choose where you want to go; enter a, b, c, d, or e:'
                                             ' \n\n', 'green')).lower().strip()
                if menu_choices == 'a':
                    result = input(colored('Do you want to see the weather \
information for another location? Enter yes or no: ', 'green')).lower().strip()
                    if result == 'yes':
                        clear_screen()
                        print(colored('Please wait while I am getting the weather \
information for you...', 'green'))
                        print(colored('This may take a few seconds...', 'green'))
                        print(colored('Thank you for your patience!', 'green'))
                        print()
                        print()
                        # Ask for city and country
                        print(colored(f'Hello, {name}! In order to obtain the weather information, \
please enter the city and country of your choice.', 'green'))
                        print()
                        print()
                        city = input('City: ')
                        country = input('Country: ')
                        # Call get_location function
                        latitude, longitude = get_location(city, country)
                        # TODO - add a check if the location is valid
                        print()
                        print()
                        # Print weather information
                        print(colored(f"You have entered the following location: \
{city}, {country}", 'yellow'))
                        print()
                        print()

                        print(
                            'Please wait while I am getting the weather information for you...')
                        print('This may take a few seconds...')
                        print('Thank you for your patience!')

                    print()
                    key_pressed()
                    clear_screen()
                    break
                elif menu_choices == 'b':
                    clear_screen()
                    print(colored('Weather Components and Units', 'yellow'))
                    print()
                    print()
                    print(colored('Temperature', 'cyan'))
                    print()
                    print(colored('Temperature is a physical quantity \
expressed in degrees. It is measured with a thermometer \
calibrated in one or more temperature scales. \
The most commonly used scales are the Celsius scale (formerly called centigrade) \
(°C), Fahrenheit scale (°F), and Kelvin scale (K). \
The kelvin (K) is the unit of temperature in the International System of Units \
(SI), in which temperature is one of the seven fundamental base quantities. \
The Kelvin scale is widely used in science and technology.', 'green'))
                    print()
                    print(colored('Humidity', 'cyan'))
                    print()
                    print(colored('Humidity is the concentration of water vapour \
present in the air. Water vapour, the gaseous state of water, \
is generally invisible to the human eye. \
Humidity indicates the likelihood for precipitation, dew, \
or fog to be present. The amount of water vapour needed to achieve saturation \
increases as the temperature increases. As the temperature of a parcel of air \
becomes lower it will eventually reach the saturation point without \
adding or losing water mass. The differences in the amount of water vapour \
needed to achieve saturation increases as the temperature increases. \
As the temperature of a parcel of air becomes lower it will eventually \
reach the saturation point without adding or losing water mass. \
The amount of water vapour contained within a parcel of air can vary \
significantly. For example, a parcel of air near saturation may contain \
10 g of water per cubic metre of air at 30 °C, \
but only 2.5 g of water per cubic metre of air at 8 °C.', 'green'))
                    print()
                    print(colored('Precipitation Probability', 'cyan'))
                    print()
                    print(colored('Precipitation probability is the likelihood \
of precipitation occurring at a given location within a given time period. \
It is often expressed either as the probability of precipitation \
occurring at any point in the area or as the probability of precipitation \
occurring at a single point in the area. \
Precipitation probability is predicted by a complex set of equations \
based on observations of humidity, wind speed, wind direction, \
and thermal gradients. Measurements of these variables are used to \
calculate the probability of precipitation. \
Precipitation probability is often expressed as a percentage. \
For example, a 60% chance of precipitation means that there is a 60% \
chance that precipitation will occur at any point in the area.', 'green'))
                    print()
                    print(colored('Pressure', 'cyan'))
                    print()
                    print(colored('Surface pressure is the atmospheric pressure \
at a location on the surface of the Earth. It is directly proportional \
to the mass of air over that location.', 'green'))
                    print()
                    print(colored('Visibility', 'cyan'))
                    print()
                    print(colored('Visibility is a measure of the distance \
at which an object or light can be clearly discerned. \
It is reported within surface weather observations and METAR code either \
in meters or statute miles, depending upon the country. \
Visibility affects all forms of traffic: roads, sailing and aviation. \
Meteorological visibility refers to transparency of air: in dark, \
meteorological visibility is still the same as in daylight for the same air. \
The visibility distance is measured horizontally, in the direction of \
the gaze, and in conditions meteorologists call standard meteorological \
visibility, meaning conditions are assumed to be standard for a given \
location and are the same everywhere within an area. \
The meteorological visibility is reported as horizontal visibility \
in the UK, and vertical visibility in the US. \
Visibility is primarily a safety concern; poor visibility, \
such as fog, can be the cause of accidents.', 'green'))
                    print()
                    print(colored('Windspeed', 'cyan'))
                    print()
                    print(colored('Wind speed, or wind flow velocity, \
is a fundamental atmospheric quantity caused by air moving from \
high to low pressure, usually due to changes in temperature. \
Wind speed is now commonly measured with an anemometer. \
Wind speed affects weather forecasting, aircraft and maritime operations, \
construction projects, growth and metabolism rate of many plant species, \
and countless other implications.', 'green'))
                    print()
                    print(colored('Wind direction', 'cyan'))
                    print()
                    print(colored('Wind direction is reported by the direction \
from which it originates. For example, a northerly wind blows from the north \
to the south. Wind direction is usually reported in cardinal directions \
or in azimuth degrees. Wind direction is measured in degrees clockwise \
from due north. Therefore, a wind blowing from the north has a wind direction \
of 0°; a wind blowing from the east has a wind direction of 90°; \
a wind blowing from the south has a wind direction of 180°; \
and a wind blowing from the west has a wind direction of 270°.', 'green'))
                    print()
                    print(colored('Wind gusts', 'cyan'))
                    print()
                    print(colored('A wind gust is a sudden, \
brief increase in the speed of the wind, \
usually lasting less than 20 seconds. \
It is of a more transient character than a squall, \
which lasts minutes, or a cyclone, \
which can last for hours or longer. \
A gust is a separate event, whereas a squall is a whole range of conditions. \
Gusts are usually reported in knots or m/s. \
Wind gusts generally occur near the trailing edge of a rain shower \
or thunderstorm, and are associated with downdrafts or microbursts. \
Gusts can also be associated with the cold front or the warm \
sector associated with a tropical cyclone. \
Wind gusts can be recorded when a station is experiencing calm conditions, \
when the wind suddenly picks up and then dies down again.', 'green'))
                    print()
                    print(colored('Temperature Maximum', 'cyan'))
                    print()
                    print(colored('The maximum temperature is the highest \
temperature recorded between sunrise and sunset, \
regardless of the time of observation. \
The minimum temperature is the lowest temperature recorded \
from sunset to sunrise, regardless of the time of observation. \
The maximum and minimum temperatures are usually recorded during \
the 24-hour period from midnight to midnight.', 'green'))
                    print()
                    print(colored('Sunrise', 'cyan'))
                    print()
                    print(colored('Sunrise is the moment when the upper limb \
of the Sun appears on the horizon in the morning. \
The term can also refer to the entire process of the Sun \
crossing the horizon and its accompanying atmospheric effects.', 'green'))
                    print()
                    print(colored('Sunset', 'cyan'))
                    print()
                    print(colored('Sunset or sundown is the daily \
disappearance of the Sun below the horizon due to Earth\'s rotation. \
As viewed from the Equator, the equinox Sun sets exactly due west \
in both Spring and Autumn. As viewed from the middle latitudes, \
the local summer Sun sets to the northwest for the Northern Hemisphere, \
but to the southwest for the Southern Hemisphere.', 'green'))
                    print()
                    print(colored('UV Index', 'cyan'))
                    print()
                    print(colored('The UV index is an international standard \
measurement of the strength of ultraviolet (UV) radiation from the Sun \
at a particular place on a particular day. \
It is primarily used in daily forecasts aimed at the general public. \
The UV index is designed as an open-ended linear scale, \
directly proportional to the intensity of UV radiation \
that causes sunburn on human skin. \
For example, if a light-skinned individual (without sunscreen) \
begins to sunburn in 30 minutes at UV index 6, \
then that individual should expect to sunburn in about 15 minutes \
at UV index 12, and should expect to sunburn in about 60 minutes \
at UV index 3. The purpose of the UV index is to help people \
effectively protect themselves from UV radiation, \
which has health benefits in moderation but causes sunburn at high levels.', 'green'))
                    print()
                    print(colored('Precipitation Probability Maximum', 'cyan'))
                    print()
                    print(colored('Precipitation probability is the likelihood \
of precipitation occurring at a given location within a given time period. \
It is often expressed either as the probability of precipitation \
occurring at any point in the area or as the probability of precipitation \
occurring at a single point in the area. \
Precipitation probability is predicted by a complex set of equations \
based on observations of humidity, wind speed, wind direction, \
and thermal gradients. Measurements of these variables are used to \
calculate the probability of precipitation. \
Precipitation probability is often expressed as a percentage. \
For example, a 60% chance of precipitation means that there is a 60% \
chance that precipitation will occur at any point in the area.', 'green'))
                    print()
                    print(colored('Windspeed Unit', 'cyan'))
                    print()
                    print(colored('The metre per second (symbol: m/s) \
is an SI derived unit of both speed (scalar) and velocity (vector \
quantity which specifies both magnitude and a specific direction), \
defined by distance in metres divided by time in seconds.', 'green'))
                    print()
                    break
                elif menu_choices == 'c':
                    clear_screen()
                    print(colored('Previous Searches Display', 'yellow'))
                    print()
                    print()
                    print(colored('This feature is not available yet. \
Please try again later.', 'red'))
                    print()
                    print()
                    break
                elif menu_choices == 'd':
                    clear_screen()
                    print(colored('Information about this app', 'yellow'))
                    print()
                    print()
                    print(colored('This app was created by Victoria \
as a third project for the Full Stack Software Development course \
at the Code Institute.', 'green'))
                    print()
                    print()
                    break
                elif menu_choices == 'e':
                    clear_screen()
                    print(colored('Thank you for using Victoria\'s Weather App! \
See you soon!', 'green'))
                    print()
                    print()


# Call main function
if __name__ == '__main__':
    main()

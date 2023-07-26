# Import required libraries
from geopy.geocoders import Nominatim
import requests
import datetime
from termcolor import colored
import readchar
import os
import time
import sys

MENU = [
    'a. Get Weather information',
    'b. Weather Components Explained',
    'c. Display Search History',
    'd. Instructions',
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

# BANNERS FOR THE APP - ASCII ART
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

# AUXILIARY FUNCTIONS


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


# WELCOME SCREEN FUNCTION
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
    print()
    # Call key_pressed function
    key_pressed()
    # Call clear_screen function
    clear_screen()


# USER NAME INPUT
def name_input():
    """
    This function asks for the user's name
    """
    # Print banner
    for line in BANNER_INPUT.splitlines():
        for character in line:
            print(colored(character, 'yellow'), end='', flush=True)
            # delay printing of each character by 0.003 seconds
            time.sleep(.003)
        print('')  # print a new line
        time.sleep(0.5)  # delay printing of each line by 0.5 seconds

    # Ask for name
    name = input("""Choose a name - it must be at least 3 characters long, 
but no longer than 10 characters, include only letters, 
no numbers or special characters: """)
    # Check if the name is valid
    while len(name) < 3 or len(name) > 10 or not name.isalpha():
        print(colored('Oops! Something went wrong. \
        The input is not valid. Please try again.', 'red'))
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

# WEATHER INFO APP
# Locator Function


def get_location(name):
    """
    This function returns longitude and latitude from an input: City, Country
    """

    # Ask for city and country
    print(colored(f'Hello, {name}! In order to obtain the weather information, \
please enter the city and country of your choice.', 'green'))
    print()
    print()
    city = input('City: ')
    country = input('Country: ')
    # Call get_location function
    print()
    print()
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="VictoriasApp")
    # Get location coordinates
    location = geolocator.geocode(f"{city}, {country}")
    if location is None:
        # Print error message
        print(colored('Oops! Something went wrong.\
 Please try again later.', 'red'))
        exit()
    # Get latitude and longitude
    latitude = str(location.latitude)
    longitude = str(location.longitude)
    # Get the location from geopy library
    location_details = geolocator.reverse(f'{latitude}, {longitude}')
    print(f"You've entered city: {city}, and country {country}!")
    print(f"That gave this result:\n{location_details.raw['display_name']}")
    # TODO: ask user if that's right result and if not, go back to a new
    return latitude, longitude, city, country


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
def print_weather(latitude, longitude, city, country):
    """
    This function prints the weather information
    """

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


# WEATHER COMPONENTS INFO EXPLAINED
def weather_components():
    """
    This function prints the weather components information
    """
    # Define menu
    components_menu = [
        'a. Temperature',
        'b. Humidity',
        'c. Precipitation',
        'd. Surface Pressure',
        'e. Visibility',
        'f. Wind',
        'g. UV Index',
        'h. Sunrise and Sunset'
    ]

    # You can get the info about
    while True:
        clear_screen()
        # Print menu
        print('\n W E A T H E R   C O M P O N E N T S\n\n'.center(80, '-'))
        for item in components_menu:
            print(item + '\n')
        print('i. Back to Main Menu\n')

        # Ask for user input
        while True:
            selection = input('Please, \
choose the weather component you want to know more about by \
entering a, b, c, d, e, f, g, h, or i: ').lower().strip()

            if selection == "a":
                print(colored('Temperature is a physical quantity \
expressed in degrees. It is measured with a thermometer \
calibrated in one or more temperature scales. \
The most commonly used scales are the Celsius scale (formerly called centigrade) \
(°C), Fahrenheit scale (°F), and Kelvin scale (K). \
The kelvin (K) is the unit of temperature in the International System of Units \
(SI), in which temperature is one of the seven fundamental base quantities. \
The Kelvin scale is widely used in science and technology.', 'green'))
                print()
                break
            elif selection == "b":
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
                break
            elif selection == "i":
                return
            elif selection in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
                print(f"You've chosen {selection}")
                break
            else:
                print('Invalid input. Try again:')
                break


# PREVIOUS SEARCHES DISPLAY
def pass_searches():
    pass


# INSTRUCTIONS
def instructions():
    pass


# MAIN FUNCTION
def main():
    # Call clear_screen function
    clear_screen()
    # Call welcome message function
    welcome_message()
    # Call name_input function
    name = name_input()
    key_pressed()
    clear_screen()

    # Menu section
    # TODO: validation
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
                clear_screen()
                latitude, longitude, city, country = get_location(name)
                # Print weather information
                print_weather(latitude, longitude, city, country)
                print()
                key_pressed()
                clear_screen()
                break
            elif menu_choices == 'b':
                weather_components()
                clear_screen()
                print(colored('Weather Components and Units', 'yellow'))
                print()
                break
            elif menu_choices == 'c':
                pass_searches()
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
                instructions()
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
                sys.exit()


# Call main function
if __name__ == '__main__':
    main()

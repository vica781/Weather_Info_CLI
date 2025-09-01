# Import required libraries
from geopy.geocoders import Nominatim
import requests
import datetime
from termcolor import colored
import readchar
import os
import time
import sys
from banners import *
import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable

# Define scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Define credentials
CREDS = Credentials.from_service_account_file(
    'CREDS.json')

# Define scope with credentials
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# Define gspread client
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Define spreadsheet
SHEET = GSPREAD_CLIENT.open('weather')

# Define worksheet
SEARCH_HISTORY = SHEET.worksheet('search_data')


# Define menu
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

# Define the HEADER
HEADER = "VICTORIA'S WEATHER INFO APP"

# Define the function to print the HEADER


def print_header():
    """
    This function prints the HEADER
    """
    print(colored(HEADER.center(80, '='), 'yellow'))
    # print(colored('===================================', 'yellow'))


# AUXILIARY FUNCTIONS


def key_pressed():
    """
    This function waits for a key to be pressed
    """
    # Argument readkey() is used to read a keypress from the user
    print(colored('Press any key to continue...', 'blue', 'on_white'))
    key = readchar.readkey()
    # Return the key pressed
    return


def clear_screen():
    """
    This function clears the screen
    """
    # Argument os.name is used to determine the name of the operating system
    os.system('cls' if os.name == 'nt' else 'clear')
    print_header()


# WELCOME SCREEN FUNCTION
def welcome_message():
    """
    This function prints a welcome message to the user
    """
    # Call clear_screen function to clear the screen before printing the header
    clear_screen()
    # Argument colored() is used to change the color of the text
    print(colored('\nWelcome to Victoria\'s Weather App!'.upper(), 'green'))
    print(colored(BANNER_INTRO, 'yellow'))
    print(colored('This app will provide you with the weather \
information for the location of your choice. Enjoy!', 'green'))
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
            # delay printing of each character by 0.01 seconds
            time.sleep(.01)
        print('')  # print a new line
        time.sleep(0.04)  # delay printing of each line by 0.01 seconds

    # Ask for name
    name = input('\nCHOOSE a NAME and then PRESS ENTER to continue. \
    \nThe name must be at least 3 characters long, \
    \nbut no longer than 10 characters, include only letters, \
    \nno numbers or special characters: ')
    # Check if the name is valid
    while len(name) < 3 or len(name) > 10 or not name.isalpha():
        print(colored('Oops! Something went wrong. The input is not valid. '
                      '\nPlease, check the format and try again.', 'red'))
        name = input('Choose a name - it must be at least 3 characters long,\
\nbut no longer than 10 characters, include only letters,\
\nno numbers or special characters: ')
    print()
    # Print welcome message
    print(colored(f"Hello,{name}! {'come rain or shine'.upper()},\
\nI wish you to be on a {'cloud nine'.upper()} \
\nand everything you do {'to be a breeze!'.upper()}", 'green'))
    print()
    return name

# WEATHER INFO APP
# Locator Function


def get_location(name):
    """
    This function returns longitude and latitude from an input: City, Country
    """
    # context parameter is used
    # to determine if the user is entering the location for the first time
    # or not in order to adapt the message accordingly

    context = "initial"
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="VictoriasApp")

    while True:  # Loop indefinitely until the user enters a valid location
        # Ask for city and country
        if context == "initial":  # if the user is entering
            # the location for the first time
            prompt_msg = f'\n\n{name}, in order to obtain the weather \
information, \nplease enter the city and country of your choice.'
        elif context == "error":  # if the user has entered an invalid location
            prompt_msg = f'{name}, it seems there was an error with your \
previous input. \nPlease enter the city and country of your choice again.'
        else:  # if the user desided to change the location
            prompt_msg = f'{name}, to change the location and get weather \
information for a different \nlocation, please enter the new city and country.'

        print(colored(prompt_msg, 'green'))
        print()
        print()
        city = input('City: ')
        country = input('Country: ')
        print()
        print()

        # Get location coordinates
        location = geolocator.geocode(f"{city}, {country}")

        if location is not None:
            # Get latitude and longitude
            latitude = str(location.latitude)
            longitude = str(location.longitude)
            # Get the location from geopy library
            location_details = geolocator.reverse(f'{latitude}, {longitude}')
            print(f"You've entered city: {city}, and country {country}!")
            print(f'That gave this'
                  f'result:\n{location_details.raw["display_name"]}')

            while True:  # Keep asking until the user confirms the location
                conformation = input('Is this the location you want '
                                     'to use? (y/n): ').lower().strip()
                if conformation == 'y':

                    # ADD SEARCH TO THE SPREADSHEET (user name,
                    # date, time, city, country)

                    # Get the the current date
                    current_date = datetime.datetime.now().strftime('%d-%m-%Y')
                    # Get the current time
                    current_time = datetime.datetime.now().strftime('%H:%M:%S')
                    # Get maximum daily temperature
                    current_temperature_max = get_weather(
                        latitude, longitude)['daily']['temperature_2m_max'][0]

                    # Append the search data to the spreadsheet
                    search_data = [name, current_date,
                                   current_time,
                                   city, country,
                                   current_temperature_max
                                   ]

                    SEARCH_HISTORY.append_row(search_data)

                    return latitude, longitude, city, country
                elif conformation == 'n':
                    context = 'change'
                    break  # This will break the inner loop
                    # and prompt user to enter a new location
                else:
                    print('Invalid input. Please, enter (Y)es or (N)o.')

        else:
            # Print error message
            # and continue with the next iteration of the loop
            print(colored('Oops! Something went wrong.'
                          '\nThe location you entered has not been found.'
                          '\nPlease, check the spelling '
                          'and try again.', 'red'))
            print()
            context = 'error'


# Defining get_weather function
def get_weather(latitude, longitude):
    """
    This function returns the current weather information
    """
    # Define global variables
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
    # Arguments latitude, longitude, city and country are used
    # to get parameters of a location

    print()
    print()
    # Print message to the user
    print('Please wait while I am getting the weather information for you...')
    print('This may take a few seconds...')
    print('Thank you for your patience!')
    print()
    print()

    # Call get_weather function
    data = get_weather(latitude, longitude)
    # Print success message
    print(colored('Success! Everything is okay. I got the data!', 'yellow'))
    print()
    key_pressed()
    clear_screen()
    print(colored(f'Here is the weather '
                  f'information for {city}, {country}:', 'cyan'))
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
        if current_precipitation_probability > 50:
            print(colored(BANNER_RAIN, 'blue'))
            print(colored('It might rain today.'
                          'Take an umbrella with you!', 'blue'))
            print(colored('Press any key to see full'
                          'weather information.', 'blue'))
            print()
            key_pressed()
            clear_screen()
            print(colored(f'Here is the weather information '
                          f'for {city}, {country}:', 'cyan'))
        elif current_temperature_max > 30 \
                and current_precipitation_probability < 30:
            print(colored(BANNER_SUN, 'yellow'))
            print(colored('It is going to be a hot day today. '
                          'Don\'t forget to put on sunscreen!', 'yellow'))
            key_pressed()
            clear_screen()
            print(colored(f'Here is the weather information for '
                          f'{city}, {country}:', 'cyan'))

        # PRINT WEATHER INFORMATION OF HOURLY REQUESTS

        # Print current temperature
        print(f'The current temperature is {current_temperature}\u00b0C')
        # Print current humidity
        print(f'The current relative humidity is {current_humidity} %')
        # Print current precipitation probability
        print(f'The current precipitation '
              f'probability is {current_precipitation_probability} %')
        # Print current surface pressure
        print(f'The current surface pressure is {current_pressure} hPa')
        # Print current visibility
        print(f'The current visibility is {current_visibility} km')
        # Print current windspeed
        print(f'The current windspeed is {current_windspeed} m/s')
        # Print current wind direction
        print(f'The current wind direction is {current_winddirection}')
        # Print current wind gusts
        print(f'The current wind gusts are {current_windgusts} m/s')

        # PRINT WEATHER INFORMATION OF DAILY REQUESTS

        # Print daily maximum temperature
        print(f'The daily maximum temperature '
              f'is {current_temperature_max}\u00b0C')
        # Print daily minimum temperature
        print(f'The daily minimum temperature '
              f'is {current_temperature_min}\u00b0C')
        # Print sunrise
        print(f'The sunrise is at {current_sunrise}')
        # Print sunset
        print(f'The sunset is at {current_sunset}')
        # Print UV index
        print(f'The UV index is {current_uv_index}')
        # Print precipitation probability
        print(f'The maximum daily precipitation '
              f'probability is {current_precipitation_probability} %')
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
    clear_screen()
    print('W E A T H E R   C O M P O N E N T S'.center(80, '_'))
    print()

    # Load weather components from a file
    with open('weather_components.txt', 'r') as file:
        weather_components = file.readlines()
    counter = 0
    for line in weather_components:
        counter += 1
        print(line, end='')
        if counter % 17 == 0:
            print('\n')
            key_pressed()
            clear_screen()
    print(colored('\n\nThis is the end of the weather components explanation.'
                  '\nYou can now go back to the main menu.', 'green'))
    print()
    key_pressed()
    return

# INSTRUCTIONS


def instructions():
    """
    This function prints the instructions
    """
    clear_screen()
    print('I N S T R U C T I O N S'.center(80, '_'))

    # Load instructions from a file
    with open('instructions.txt', 'r') as file:
        instructions = file.readlines()
    counter = 0
    for line in instructions:
        counter += 1
        print(line, end='')
        if counter % 17 == 0:
            print('\n')
            key_pressed()
            clear_screen()
    print(colored('\n\nThis is the end of the instructions.'
                  '\nYou can now go back to the main menu.', 'green'))
    print('\n\n')
    key_pressed()
    return


def past_searches():
    """
    This function displays the search history from the spreadsheet
    as a table and shows a message if the were no previous searches.
    """
    # Get all the values from the search_data worksheet
    clear_screen()
    all_search_data = SEARCH_HISTORY.get_all_values()

    # Check if any data is present in the search history
    if len(all_search_data) == 1:

        print(colored('\n\nThere were no searches conducted yet. '
                      '\nPlease use option "a" from the menu to get weather'
                      '\ninformation for a location of your choice.', "red"))

        print('\n\n')
        key_pressed()
        return

    # Create a new prettytable instance
    table = PrettyTable()
    # Set the field names (header row)
    table.field_names = all_search_data[0]
    # Add rows to the table (skip the header row)
    for row in all_search_data[1:]:
        table.add_row(row)

    # Clear the screen once again and print the header
    clear_screen()

    # Display the search history header
    print('S E A R C H   H I S T O R Y'.center(80, '_'))
    print()

    # Display the table
    print(table)

    print(colored('\n\nThis is the end of the search history.'
                  '\nYou can now go back to the main menu.', 'green'))
    print('\n')
    key_pressed()
    return


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

    # MENU SECTION

    while True:
        clear_screen()
        print('M E N U'.center(80, '_'))
        print()
        for item in MENU:
            print(item + '\n')

        menu_choices = ''
        while menu_choices == '':
            menu_choices = input(
                colored('Please, CHOOSE where you want to go and then\n'
                        'Press ENTER to continue;\nenter a, b, c, d, or e: ',
                        'green')).lower().strip()
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
                print()
                break
            elif menu_choices == 'c':
                past_searches()
                clear_screen()
                print()
                break
            elif menu_choices == 'd':
                instructions()
                clear_screen()
                print()
                break
            elif menu_choices == 'e':
                clear_screen()
                print(colored('Thank you for using Victoria\'s '
                              'Weather App! See you soon!', 'green'))
                print(colored(BANNER_EXIT, 'yellow'))
                sys.exit()


# Call main function
if __name__ == '__main__':
    main()

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# WEATHER INFO APP

![Am I Responsive Image](./assets/readme_files/amiresponsive.png)

[View the live project here](https://millionaire-kindof.herokuapp.com/)

## Table of contents

1. [Introduction](#Introduction)
2. [UX](#UX)
   1. [Ideal User Demographic](#Ideal-User-Demographic)
   2. [User Stories](#User-Stories)
   3. [Development Planes](#Development-Planes)
   4. [Design](#Design)
3. [Features](#Features)
   1. [Existing Features](#Existing-Features)
   2. [Features to Implement in the future](#Features-to-Implement-in-the-future)
4. [Issues and Bugs](#Issues-and-Bugs)
5. [Technologies Used](#Technologies-Used)
   1. [Main Languages Used](#Main-Languages-Used)
   2. [Libraries And Modules Used](#Libraries-And-Modules-Used)
   3. [Frameworks And Programs Used](#Frameworks-And-Programs-Used)
6. [Testing](#Testing)
   1. [Testing.md](TESTING.md)
7. [Deployment](#Deployment)
   1. [Deploying on Heroku](#Deploying-On-Heroku)
8. [Credits](#Credits)
   1. [Code](#Code)
   2. [Contents](#Contents)
9. [Acknowledgements](#Acknowledgements)

---

## Introduction

The game Who Wants To Be A Millionaire Kind Of is the 3rd Portfolio Project at the Code Institute. It is an hommage to the famous TV game that conquered the world. In this version, the questions are related to the Movies and TV.

The purpose of this project is to build a command-line application in Python that allows the user to manage a common dataset about a particular domain.

[Back to the top ⇧](#Who-Wants-To-Be-A-Millionaire-Kind-Of)

## UX

### Ideal User Demographic

There are two types of ideal users:

- New User
- Current User

### User-Stories

#### New User Goals

- As a new user, I want easily navigate through the application.
- As a new user, I want easily consult and find the rules.
- As a new user, I want to test my knowledge about the movies and TV.
- As a new user, I want to have learn something while having fun.

#### Current User Goals

- As a current user, I want a game similar to the Who Wants To Be A Millionaire TV game.
- As a frequent user, I want to test my knowledge about the movies and TV.
- As a frequent user, I want have questions with a progressive difficulty.
- As a frequent user, I want to improve my knowledge and score.

[Back to the top ⇧](#Who-Wants-To-Be-A-Millionaire-Kind-Of)

### Development-Planes

To build a command-line application to give the user an experience similar to the one of the Who Wants To Be A Millionaire TV game, with the questions about movies.

#### Strategy

Strategy incorporates user needs as well as product objectives. This application will focus on the following target audience, divided into three main categories

- Audience

  - New Users
  - Current Users

- Demographic

  - All ages

- Psychographic:
  - Movie fan
  - Quiz fan
  - Problem solver

The application is supposed to enable the user to:

- Play the Who Wants To Be A Millionaire
- Insert a player name
- Answer to a series of randomly selected questions from the database
- Experience a progressive difficulty level
- Be aware of the points gained, threshold points and won points
- Know when answers wrongly and learn the correct answer
- Enter the high score databes if there are some points won at the game end
- Restart the game if wanted with a new set of questions
- Read the instructions about the game
- See the high scores from the database

The Developer/Administrator needs to receive: \* Player's Name

#### Scope

After defining goals of the game, we are delineating the necessary features:

- Required functionalities
  - Intro screen display
  - Question database loader
  - How to play the game instructions display
  - High scores display
  - Global Menu
  - Quiz starter
  - Quiz questions generator
  - Points/Threshold display
  - Question display and guess
  - Answer validator
  - Correct answer displayed if wrongly answered or congratulatory message if answered correctly
  - On game end - displayed a new screen with appropriate messages, points and the high scores saved to Google Sheet
  - On application exit - displayed a new screen with Thank you note

#### Structure

A flowchart made in [LUCID](https://lucid.app.com/ "Link to Lucid") demonstrates the game's structure.

<details>
<summary>Flowchart Image</summary>

![Flowchart](./assets/readme_files/flowchart.svg)

</details>

#### Skeleton

Being the game in fact a terminal application, the skeleton plane would be somwhat in between the presented flowchart and the design. Therefore, the relative details will follow in the next section.

[Back to the top ⇧](#Who-Wants-To-Be-A-Millionaire-Kind-Of)

### Design

The overall design of this command line application is quite simple. The developer at first decided to use different colours and ASCII text art. But, upon the deployment on Heroku, and some feedback from the testers, the developer opted for a more simpler design and less colourful in order to keep the best possible visibility of the application - beign a quiz game based on a lot of text that needs to be read.

For more engaging design, the devlopper has decided use a few screens at the intro, end game, end quiz, display high scores, etc. ASCII art is used for a games 'LOGO' that repeat itself throughout the application. For the passages from the screens, the developer opted for a simple keypress detection.

The interactive parts of the application are the user name insertion, the menu and the answering to the questions, which require a valid input and pressing of the 'Enter' key.

[Back to the top ⇧](#Who-Wants-To-Be-A-Millionaire-Kind-Of)

## Features

### Existing Features

- **Different info screens**

  - These are presented in different moment of the game. Practically every feature is related to these screens, e.g.:

  1. Intro Screen

  ![Intro Screen](./assets/readme_files/intro_screen.png)

  2. End Screen

  ![End Screen](./assets/readme_files/end_screen.png)

- **Question database loader**

  - At the beginning of the application the json files are loaded with the data stored locally, but produced by the API https://the-trivia-api.com/. At first, the developer copied the data recevied into the code of another Python file that was imported to the main file. After organizing the data in json files, the developer integrated the code into main file. The three json files contain different difficulety level questions, and each 15 different ones.

  ![JSON Files](./assets/readme_files/json_files.png)

- **How to play the game instructions display**

  - The instructions are read from the corresponding txt file and displayed on screen. They appear after the intro screen and later when chosen from the menu.

  ![How To Play Instructions Screen](./assets/readme_files/how_to_play_screen.png)

- **Player's Name Input**

  - After the instructions, the next screen requires user to enter they name. The valid input corresponds to a string containing only letters and of minimum 3 characters length.

  ![Player's Name Input](./assets/readme_files/insert_name_screen.png)

- **Menu**

  - Menu is the central feature of the application. It gives to the user four possibilities to proceed: start quiz, show the instructions, show the high scores, or exit from the application.

  ![Menu](./assets/readme_files/menu_screen.png)

- **Quiz function**

  - This functionality immediately generates 15 randomly selected questions, 5 of each level, through the dedicated Class. There are controllers which guarantee that the questions woudn't be repeated and the shuffler for the answers, so they appear every time in a different order. Once that is over, the quiz starts with the first question. On the displayed screen, there are information about the point value of the question and the threshold (points guaranteed) if they were reached. Then appears the question and four answeres given with the letters a, b, c, and d as a choice. There's fifth option given to the user, that of q if they wish to quit the game with the so far accumulated points. If the wrong answer is given, the quiz ends and the points fall to the threshold. If none is reached, the quiz ends with 0 points, relative screen, and no high score saved. If the quiz ends with some points or the million is reached, different screens are presented and the score is saved in the high scores Google Sheet (name, points, date). After the end quiz screen, Menu returns.

  ![Quiz Question Screen](./assets/readme_files/question_screen.png)
  ![End Quiez Screen](./assets/readme_files/end_quiz_screen.png)

- **High Scores Display**

  - This function first fetches the data from the high scores Google Sheet and then presents them in order of the points received. So, the most successful scores come first.

  ![High Scores Screen](./assets/readme_files/high_scores_screen.png)

- **Game Exit**

  - If this choice is made, the game finishes with the thank you note to the user.

  ![Game End Screen](./assets/readme_files/end_screen.png)

- **Slow print function**

  - This feature is present in almost every screen in the application. It gives the user the impression of an animation. In fact, it consists of the printing the characters of the string on by one with a time delay.

  ![Slow Print Function](./assets/readme_files/slow_print.gif)

[Back to the top ⇧](#Who-Wants-To-Be-A-Millionaire-Kind-Of)

### Features to Implement in the future

- The auxiliary features from the original TV game
  There are three auxiliary features in the original TV game: call a friend, ask the audience, and 50:50 options. Because of lack of time, the developer couldn't make it to implement these features. The complex algorithm for randomization with 80% of probabilty for the right answer of the first two features would have to wait for some other moment.
- The use of API for the questions
  The developer used the static JSON copy of the question from an API that had some limitations. Before the end of the project, the developer found one other API without the same limitations and without need of authentication to access the database, but didn't want to include it the final project. That was because the data structure was sligthly different and the developer didn't have time to properly test the API's reliability.

[Back to the top ⇧](#Who-Wants-To-Be-A-Millionaire-Kind-Of)

## Issues and Bugs

Several issues were encountered during developement but the most troublesome are listed below.

- **Validation Errors**
  In different moments of the development, the validation bugs happened. First one was the unrecognized choice of a letter when written as capital letter. That was immediately corrected by validating same letters, being capital or lower. Afterwards, with the username, the developer didn't take into consideration the possibility of user entering characters that weren't letters. That bug was pointed out by the mentor and surfaced again in the testing phase of the colleagues on Slack. That bug was also corrected.

- **Quiz continuing even if quit selected**
  There was a bug because of which the quiz continued although the user selected to quit. The error was due to selection of the possibilities of gaining only threshold points (as in choosing the wrong answer), whilst in quitting, the user can save all the points they won. That was also corrected.

- **Different display issues on Herokue**
  When deployed on Heroku, the application had issues with the visibility of the ASCII art, and some selected colours were barely visible. That was pointed out by some colleagues from Slack in the testing phase. The developer decided to generate new ASCII art texts and select the plain colours to garantee the visibility of the text.

### Unfixed Bugs

There are no known unfixed bugs.

[Back to the top ⇧](#Who-Wants-To-Be-A-Millionaire-Kind-Of)

## Technologies Used

### Main Languages Used

- Python3

### Libraries And Modules Used

- **json** - JSON encoder and decoder module
- **getch** - The module that gets a character from user input, with no output
- **os** - This module provides a portable way of using operating system dependent functionality
- **random** - Random variable generators module.
- **time** - This module provides various functions to manipulate time values.
- **datetime** - Concrete date/time and related types module.
- **sys** - This module provides access to some objects used or maintained by the interpreter and to functions that interact strongly with the interpreter.
- **gspread** - Google Spreadsheets client library.
- **google.oauth2.service_account** - A module for the Google authentication.
- **termcolor** - The module for ANSI color formatting for output in terminal.

### Frameworks And Programs Used

- [Heroku](https://heroku.com/ "Link to Heroku") was used for the app deployment.
- [GitPod](https://gitpod.io/ "Link to GitPod") was used for writing, commiting, and pushing code to GitHub.
- [GitHub](https://github.com/ "Link to GitHub")
- [Am I Responsive?](https://ui.dev/amiresponsive "Link to Am I Responsive") was used for the web page picture of this README.md
- [Peek](https://github.com/phw/peek) was used to make screencasts for the documentation.

[Back to the top ⇧](#Who-Wants-To-Be-A-Millionaire-Kind-Of)

## Testing

Testing is documented on a separate page [Testing MD Page](TESTING.md).

## Deployment

The code was developed on Gitpod, and deployed on GitHub.

### Deploying on Heroku

Deploying on Heroky required the following:

- Type "pip3 freeze > requirements.txt" in your Github terminal to update the requirements.txt file with the list of dependencies used in the project. Save, commit and push.

- On Heroku web site, these two steps are necessary if the developer don't have a Heroku account yet:

  - Create an Heroku account, select Python as the 'Primary development language'.
  - Open the email sent to your address and click the link to verify your email address. Follow the instructions to create a password and log in.

- On Heroku web site, once you're logged in, click the 'create new app' button on the dashboard. Name your app, select your region and click 'Create App'

- In the "Settings" tab, add both the python and node.js build packs.

- Create a "Config VAR" named 'CREDS' KEY and copy/paste the creds.json file in it.

- Create another "Config VAR" called PORT as the KEY with 8000 as VALUE.

- In the "Deploy" tab, choose GitHub as a deployment method.

- Search for the right repository (in this case 'millionaire-kindof').

- Click on deploy branch.

- Once the app is built, and the link click "View", click on it to go to the site with the deployed Python app.

The application is finally deployed on the link [https://millionaire-kindof.herokuapp.com/](https://millionaire-kindof.herokuapp.com/).

[Back to the top ⇧](#Who-Wants-To-Be-A-Millionaire-Kind-Of)

## Credits

### Code

- In order to develop the application, the developer has consulted frequently the following web sites:
  - [Stack Overflow](https://stackoverflow.com/ "Link to Stack Overflow")
  - [Geeks for Geeks](https://www.geeksforgeeks.org/ "Link to Geeks for Geeks")
    - especially [Python sort list by second element of a sublist](https://www.geeksforgeeks.org/python-sort-list-according-second-element-sublist/)
  - [W3Schools](https://www.w3schools.com/ 'Link to W3Schools)
  - Info about the clearing screen in Python came from [Scaler](https://www.scaler.com/topics/how-to-clear-screen-in-python/ 'Link to explanation from Scaler for clear screen)

### Contents

- For the questions database, the developer has used the following web API:
  - [The Trivia API](https://the-trivia-api.com/) The questions are taken from the Film and TV category on the web API app and copied into the json files divided by difficulty level (easy, medium, hard).

[Back to the top ⇧](#Who-Wants-To-Be-A-Millionaire-Kind-Of)

## Acknowledgements

I would like to thank:

- My mentor, the Supergirl Koko, for all the encouragement, advices, help and expertise.
- My colleagues from the Code Institute who tested my code and gave me some wonderful feedback.
- To my inner circle, who are secretly following my ongoing coding adventure.

[Back to the top ⇧](#Who-Wants-To-Be-A-Millionaire-Kind-Of)

---

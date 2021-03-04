<!-- omit in toc -->
# **Match Card Game**
Match card game is a simple card matching game built with pygame. To maximize learning opportunities, the game is developed entirely by myself with occasional reference to pygame documentation and python specific syntax through google.

<!-- omit in toc -->
## **Table of Content**
- [**Motivation**](#motivation)
- [**Features**](#features)
- [**How to run**](#how-to-run)
    - [Running the game with python](#running-the-game-with-python)
- [**Screenshots**](#screenshots)
- [**Code formatter**](#code-formatter)



## **Motivation**
Example of a card game in MapleStory
![Card game](https://i.redd.it/rulwt80bdyox.png)

When I was young, I spent quite a lot of time on gaming and one particular game is MapleStory. Within the game itself, you can create a public match card game where anyone can join it. I always enjoy playing it. 

Im trying to build more side project to improve my programming skills instead of just passive learning. Since the mechanism of this game is relatively easy, I decided to build it with pygame.

This is my second side project! Do checkout my first side project [classic-snake-game](https://github.com/kahkeong/classic-snake-game) .

## **Features**
- Randomized fruit images for each match (taken randomly from 20 images in the fruits folder)
- Customized board grid size through command prompt (default is 4x3)
- Restart the game through option button whenever you like
- End game statistic to show how many rounds you took to complete the match

## **How to run**
 <!-- An executable file is included and it is generated with the help of [auto-py-to-exe] https://pypi.org/project/auto-py-to-exe/. Hence, you can run the game even without python installed in your device. If you do have python installed, you can use either approaches. Note that Im using a Windows machine. !-->

#### Running the game with python
- change directory to the downloaded project
- ensure python is set in your windows path
- type 'python main.py' at your command prompt to run it
 
<!-- 
#### Running the game without python
- click on the executable file to run the game
!-->

## **Screenshots**
Main menu screen

![Main Menu](./screenshots/main_menu.PNG)

Card initializing

![Card initialization](./screenshots/card_initialization.gif)

A pair of card matched will always stay open

![Card matched](./screenshots/card_matched.PNG)

End game screen

![End](./screenshots/end_game.PNG)

## **Code formatter**
I used [black](https://black.readthedocs.io/en/stable/) formatter with max line length set to 100
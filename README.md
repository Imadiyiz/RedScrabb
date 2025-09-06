# RedScrabble Project Overview

This is a word game built in Python, which is a crossover between the infamous gameshow countdown and Scrabble the household board game. The project was originally completed during Summer 2023 as an extension of a college project.

### The game includes:

Word validation against a Scrabble dictionary

Score tracking with an SQLite database

A text-based interface for playing locally

It is a practice project that helped me learn about Python, game logic, and databases.

## How to Play

Run the main script to launch the game in your terminal.

### Place words 

This is a single player game. Each round you form valid words from your given letters, pressing enter to submit your word. You may use the same letter multiple times.

### Scoring

Each word is checked for validity. Scores are assigned based on letter values (as in Scrabble). Scores are saved to a local SQLite database (Highscore.db).

### Power-ups 

There are two power-ups in this game

The first being the 'shuffle rack' option. This enables you to replay a round with another deck of letters

The second being the 'X2 score' option. If you believe you have a high scoring word, you can use the X2 score power-up before submitting the word to double the value of the letters.

*REMINDER:* These power-ups can be used in the same round and can only be used once in total.

### Winning

After 5 rounds your scores are combined to give you your final score.

## Requirements

Python 3.7+

## Running the Game

Clone the repository and run:

python RedScrabble.py

A Highscore.db database will be created automatically if it doesn’t exist.

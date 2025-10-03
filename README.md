# Wordle Solver

A simple Wordle solver with a Streamlit UI.  
It uses NLTK’s English word corpus (downloaded locally) and ranks possible guesses by letter frequency.  

## Features
- Filters words based on green, yellow, and gray feedback (Wordle rules).
- Ranks words by letter frequency for better guessing.
- Streamlit web app interface.

## Installation
Clone the repo:

git clone https://github.com/your-username/WordleSolver.git
cd WordleSolver

## Install Dependencies

pip install -r requirements.txt

## Running the App

Start the Streamlit app:

streamlit run app.py

## Notes

The first run will download the NLTK words corpus into a local nltk_data/ folder.

The nltk_data/ folder is excluded from GitHub with .gitignore.
import os

# Auth
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN") or "A_DISCORD_TOKEN"

# Guessing Game
MAX_GUESS = 10
GAME_LENGTH_SECONDS = 10

# Word tracker
MIN_WORD_LENGTH = 3

# Charting data
WORD_COUNT_CHART_FILENAME = "chart.png"
NUMBER_OF_WORDS_PER_CHART = 25

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Auth
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN") or "A_DISCORD_TOKEN"

# Guessing Game
GUESSING_GAME_MAX = 10
GUESSING_GAME_LENGTH = 10

# Word tracker
MIN_WORD_LENGTH = 3

# Charting data
WORD_COUNT_CHART_FILENAME = "{}/word_chart.png".format(PROJECT_ROOT)
NUMBER_OF_WORDS_PER_CHART = 25

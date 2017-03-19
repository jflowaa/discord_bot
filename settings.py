import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Auth
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN") or "A_DISCORD_TOKEN"

# Guessing Game
GUESSING_GAME_MAX = 10
GUESSING_GAME_LENGTH = 10
GUESSING_GAME_COMMANDS = [
    "!guess -- Starts the guessing game if one is not running"
]

# Charting data
WORD_COUNT_CHART_FILENAME = "{}/word_chart.png".format(PROJECT_ROOT)
WORD_COUNT_WORDS_PER_CHART = 25

# Word Statistics
MIN_WORD_LENGTH = 3
WORD_STATISTICS_COMMANDS = [
    "!statssme -- Generates a chart of your top {} used words".format(WORD_COUNT_WORDS_PER_CHART),
    "!statsall -- Generates a chart of everyone's collective top {} used words".format(WORD_COUNT_WORDS_PER_CHART),
    "!statsword *word* -- Returns the number of times *word* has been used by everyone",
    "!statsperson @person -- Generates a chart for that person's top {} used words".format(WORD_COUNT_WORDS_PER_CHART)
]



import string

from database import increment_word_count_for_author, get_count_for_all, get_count_for_author, get_word_count
from utils import chart_stats
import settings


def track_word_count(author_id, message):
    """
    Someone said a message, let's add the contents to the DB, along with the person who said it
    :param author_id: The person's ID
    :param message: The content of the message
    :return:
    """
    for word in message:
        # Go word by word
        word = strip_punctuation(word)
        if len(word) >= settings.MIN_WORD_LENGTH:
            # Word is at least min word length
            increment_word_count_for_author(author_id, word)


def get_word_stats(author_id=None):
    """
    Gets the count for all words said by everyone or author
    :param author_id: Author ID if given
    :return:
    """
    if author_id:
        stats = get_count_for_author(author_id)
    else:
        stats = get_count_for_all()
    chart_stats(stats)


def get_stats_for_word(word):
    """
    Strips any punctuation and gets the count for that word.
    Words are stored in DB without punctuation
    :param word: The word to get stats for
    :return:
    """
    count = get_word_count(strip_punctuation(word))
    return "The word '{}' has been used **{}** times".format(word, count)


def strip_punctuation(word):
    """Strips punctuation from a word."""
    return "".join([c for c in word if c not in string.punctuation]).lower()


def get_commands():
    """Lists all the available commands."""
    commands = []
    commands.extend(settings.GUESSING_GAME_COMMANDS)
    commands.extend(settings.WORD_STATISTICS_COMMANDS)
    message = "A listing of all available commands: \n"
    for command in commands:
        message += command + "\n"
    return message

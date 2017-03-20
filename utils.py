import re
import string
from contextlib import contextmanager

import matplotlib
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

matplotlib.use("agg")
import matplotlib.pyplot as plt

from models import Base
import settings

engine = create_engine("sqlite:///{}/bot.db".format(settings.PROJECT_ROOT), echo=False)
Base.metadata.create_all(engine)  # Creates database if not exists
Session = sessionmaker(bind=engine)

url_pattern = re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",
                         re.IGNORECASE)


@contextmanager
def session_scope():
    """Yields a database session"""
    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print("Database Error: \n{}".format(e))
    finally:
        session.close()


def chart_stats(stats):
    """Creates a chart with the given dictionary"""
    word_list, count_list = zip(*stats[:settings.WORD_COUNT_WORDS_PER_CHART])
    plt.barh(range(len(word_list)), count_list, align="center", height=0.5)
    plt.yticks(range(len(word_list)), word_list)
    plt.xlabel("Number of Times")
    plt.xticks(range(max(count_list) + 1))
    plt.savefig(settings.WORD_COUNT_CHART_FILENAME)
    plt.clf()


def strip_punctuation(word):
    """Strips punctuation from a word."""
    return "".join([c for c in word if c not in string.punctuation]).lower()


def check_if_url(word):
    """Checks if the word is the URL."""
    return url_pattern.match(word)

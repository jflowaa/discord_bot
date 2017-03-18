from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

from models import Base
import settings

engine = create_engine("sqlite:///cacabot.db", echo=False)
Base.metadata.create_all(engine)  # Creates database if not exists
Session = sessionmaker(bind=engine)


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
    word_list, count_list = zip(*stats[:settings.NUMBER_OF_WORDS_PER_CHART])
    plt.barh(range(len(word_list)), count_list, align="center", height=0.5)
    plt.yticks(range(len(word_list)), word_list)
    plt.xlabel("Number of Times")
    plt.xticks(range(max(count_list) + 1))
    plt.savefig(settings.WORD_COUNT_CHART_FILENAME)

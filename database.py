import operator

from sqlalchemy import and_

from models import Word
from utils import session_scope


def increment_word_count_for_author(author_id, word_to_increment):
    """
    Queries the database for a word record with both the word and author id value
    :param author_id: The author who said the word
    :param word_to_increment: the word said
    :return:
    """
    with session_scope() as session:
        word = session.query(Word).filter(and_(Word.author == author_id, Word.word == word_to_increment)).first()
        if word:
            word.count += 1
        else:
            # Word has never been said by the other, let's change that
            word = Word()
            word.author = author_id
            word.word = word_to_increment
            session.add(word)


def get_count_for_all():
    """Gets all the word records in database"""
    with session_scope() as session:
        words = session.query(Word).all()
        return create_word_stat_dict(words)


def get_count_for_author(author_id):
    """Gets all the word records in database by author given"""
    with session_scope() as session:
        words = session.query(Word).filter(Word.author == author_id).all()
        return create_word_stat_dict(words)


def get_word_count(word):
    """Gets the count for all the records with matching word"""
    with session_scope() as session:
        words = session.query(Word).filter(Word.word == word).all()
        count = 0
        for word in words:
            count += word.count
        return count


def create_word_stat_dict(words):
    """
    Due to database structure a word can record can have a repeated word value.
    So we need to go one by one through the words and create a dictionary holding the word as a key
    and the count as a value
    :param words: Word models from database
    :return:
    """
    stats = {}
    for word in words:
        if stats.get(word.word):
            stats[word.word] += word.count
        else:
            stats[word.word] = word.count
    sorted_stats = sorted(stats.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_stats

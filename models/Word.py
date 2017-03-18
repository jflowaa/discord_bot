from sqlalchemy import Column, Integer, String

from models import Base


class Word(Base):
    """Word model for Cacabot"""
    __tablename__ = "word"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String, nullable=False)
    author = Column(Integer, nullable=False, default=1)
    count = Column(Integer, nullable=False, default=1)

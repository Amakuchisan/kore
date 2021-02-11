import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import text

from db.setting import session
from model.article_word import *
from db import article, word

def create(name: str, count: int, url: str):
    article_id = article.find_article_by_url(url)
    word_id = word.find_name(name)
    article_word = Article_Word()
    article_word.article_id = article_id
    article_word.word_id = word_id
    article_word.word_count = count
    session.add(article_word)
    session.commit()

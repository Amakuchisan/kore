import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import text

from db.setting import session
from model.article import *

def find_article_by_url(url: str):
    article = session.query(Article.id).filter(Article.url==url).first()
    if article is not None:
        return article.id
    return None

def create(url: str):
    article = Article()
    article.url = url
    # article.title = title
    session.add(article)
    session.commit()

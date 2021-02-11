import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import text

from db.setting import session
from model.user_article import *
from db import user, article

def create(hatena_id: str, url: str):
    user_id = user.find_id(hatena_id)
    article_id = article.find_article_by_url(url)
    user_article = User_Article()
    user_article.user_id = user_id
    user_article.article_id = article_id
    session.add(user_article)
    session.commit()

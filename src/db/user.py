import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import text

from db.setting import session
from model.user import *


def find_wordcloud(hatena_id: str):
    user = session.query(User.wordcloud).filter(
        User.hatena_id == hatena_id).first()
    if user is not None:
        return user.wordcloud
    return None

def find_id(hatena_id: str):
    user = session.query(User.id).filter(User.hatena_id==hatena_id).first()
    if user is not None:
        return user.id
    return None

def save_img(hatena_id: str, image):
    if find_id(hatena_id) is None:
        create(hatena_id)
    user = session.query(User).filter(User.hatena_id == hatena_id).first()
    user.wordcloud = image
    session.commit()

def create(hatena_id: str):
    user = User()
    user.hatena_id = hatena_id
    session.add(user)
    session.commit()

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import text

from db.setting import session
from model.user import *

def find_wordcloud(hatena_id: str):
    user = session.query(User.wordcloud).filter(User.hatena_id==hatena_id).first()
    if user is not None:
        return user.wordcloud
    return None

def save_img(hatena_id: str, image):
    if find_wordcloud(hatena_id) is None:
        user = User()
        user.hatena_id = hatena_id
        user.wordcloud = image
        session.add(user)
        session.commit()
        return
    user = session.query(User).filter(User.hatena_id==hatena_id).first()
    user.wordcloud = image
    session.commit()

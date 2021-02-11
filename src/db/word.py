import sqlalchemy
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy.sql import text

from db.setting import session
from model.word import *
from model.article_word import *
from model.article import *
from model.user_article import *
from model.user import *

def find_name(name: str):
    word = session.query(Word.id).filter(Word.name==name).first()
    if word is not None:
        return word.id
    return None

# 辞書型で返却
def find_word(hatena_id: str):
    word = session.query(Word.name, func.sum(Article_Word.word_count))\
    .join(Article_Word)\
    .join(Article)\
    .join(User_Article)\
    .join(User).filter(User.hatena_id==hatena_id).group_by(Word.name).all()
    # 同じwordは、word.nameとcountを足して返却する
    # できれば上からArticleを除外したい
    # select name, SUM(word_count) from word join article_word on
    # word.id=article_word.word_id where user.hatena_id=hatena_id GROUP BY name;
    return dict(word)

def create(name: str):
    word = Word()
    word.name = name
    session.add(word)
    session.commit()

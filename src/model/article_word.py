import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import current_timestamp
from setting import Base
from setting import ENGINE

class Article_Word(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'article_word'
    id = Column('id', BigInteger, autoincrement=True, nullable=False, primary_key = True)
    article_id = Column('article_id', BigInteger, nullable=False)
    word_id = Column('word_id', BigInteger, nullable=False)
    word_count = Column('word_count', Integer, nullable=False)
    created_at = Column('created_at', TIMESTAMP, nullable=False, server_default=current_timestamp())
    updated_at = Column('updated_at', TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column('deleted_at', TIMESTAMP)

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)

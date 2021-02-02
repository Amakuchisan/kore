import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, TIMESTAMP, Text
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import current_timestamp
from db.setting import Base
from db.setting import ENGINE

class Article(Base):
    """
    アーティクルモデル
    """
    __tablename__ = 'article'
    id = Column('id', BigInteger, autoincrement=True, nullable=False, primary_key = True)
    url = Column('url', Text, nullable=False)
    title = Column('title', Text, nullable=False)
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

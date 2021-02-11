import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP, MEDIUMBLOB
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import current_timestamp
from db.setting import Base
from db.setting import ENGINE

class User(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'user'
    id = Column('id', INTEGER(unsigned=True), autoincrement=True, nullable=False, primary_key = True)
    hatena_id = Column('hatena_id', String(200), nullable=False)
    wordcloud = Column('wordcloud', MEDIUMBLOB)
    created_at = Column('created_at', TIMESTAMP, nullable=False, server_default=current_timestamp())
    updated_at = Column('updated_at', TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column('deleted_at', TIMESTAMP)

    user_article = relationship("User_Article", back_populates="user")



def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)

import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import current_timestamp
from db.setting import Base
from db.setting import ENGINE
from model import user


class User_Article(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'user_article'
    id = Column('id', BIGINT(unsigned=True), autoincrement=True,
                nullable=False, primary_key=True)
    user_id = Column('user_id', INTEGER(unsigned=True),
                     ForeignKey('user.id'), nullable=False)
    article_id = Column('article_id', BIGINT(unsigned=True),
                        ForeignKey('article.id'), nullable=False)
    created_at = Column('created_at', TIMESTAMP, nullable=False,
                        server_default=current_timestamp())
    updated_at = Column('updated_at', TIMESTAMP, nullable=False, server_default=text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column('deleted_at', TIMESTAMP)

    user = relationship(
        "User", back_populates="user_article", foreign_keys=[user_id])
    article = relationship(
        "Article", back_populates="user_article", foreign_keys=[article_id])


def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main(sys.argv)

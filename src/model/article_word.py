import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.functions import current_timestamp
from db.setting import Base
from db.setting import ENGINE

class Article_Word(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'article_word'
    id = Column('id', BIGINT(unsigned=True), autoincrement=True, nullable=False, primary_key = True)
    article_id = Column('article_id', BIGINT(unsigned=True), ForeignKey('article.id'), nullable=False)
    word_id = Column('word_id', BIGINT(unsigned=True), ForeignKey('word.id'), nullable=False)
    word_count = Column('word_count', INTEGER(unsigned=True), nullable=False)
    created_at = Column('created_at', TIMESTAMP, nullable=False, server_default=current_timestamp())
    updated_at = Column('updated_at', TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted_at = Column('deleted_at', TIMESTAMP)

    article = relationship("Article", back_populates="article_word", foreign_keys=[article_id])
    word = relationship("Word", back_populates="article_word", foreign_keys=[word_id])

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)

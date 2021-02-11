from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

# mysqlのDBの設定
url = 'mysql+pymysql://kore:kore@db/kore?charset=utf8'

DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8mb4' % (
    "kore",
    "kore",
    "db",
    "kore",
)
ENGINE = create_engine(
    DATABASE,
    encoding = "utf-8",
    echo=True # Trueだと実行のたびにSQLが出力される
)

session = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = ENGINE
    )
)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()

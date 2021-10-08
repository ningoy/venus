from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = "venus"
password = "d7c2fea3e449e36529ac40ea93d03f04"
postgresserver = "127.0.0.1:5432"
db = "venus"
url = "postgresql://{}:{}@{}/{}".format(user,
                                        password,
                                        postgresserver,
                                        db)
engine = create_engine(
    url, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

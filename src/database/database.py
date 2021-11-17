from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os
load_dotenv() 
 
USER_MYSQL = os.environ.get("USER_MYSQL") 
PASSWORD_MYSQL = os.environ.get('PASSWORD_MYSQL') 
SERVER_MYSQL = os.environ.get('SERVER_MYSQL') 
DATABASE_MYSQL = os.environ.get('DATABASE_MYSQL') 
# from sqlalchemy_utils import create_database, database_exists
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USER_MYSQL}:{PASSWORD_MYSQL}@{SERVER_MYSQL}/{DATABASE_MYSQL}"
print("-"*100)
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Database URL - SQlite for local development only
DATABASE_URL = 'sqlite:///./community_support.db'

#Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False}
)
#connect_args is specific to SQLite to allow connections from multiple threads

#Create a session class
SessionLocal = sessionmaker(
    autocommit = False,  #Disabling autocommit
    autoflush = False,  #Disabling autoflush for greater control
    bind = engine  #Binding session to engine
)

#Base class for creating database models later
Base = declarative_base()

# get_db is a generator function that does the following...
# makes a new db session
# yields the session to the calling function 
# closes the session after use
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import os
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# Read the Alembic configuration file
config = ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), '..', 'alembic.ini')
config.read(config_path)
db_url = config.get('alembic', 'sqlalchemy.url')



engine = create_engine(db_url, echo=True,  pool_size=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
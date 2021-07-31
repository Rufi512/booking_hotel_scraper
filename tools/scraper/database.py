#from sqlalchemy import create_engine
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


from dotenv import load_dotenv

import os
load_dotenv()

user:str = os.getenv('POSTGRES_USER')
password:str = os.getenv('POSTGRES_PASSWORD')
host:str = os.getenv('POSTGRES_HOST')
port:str = os.getenv('POSTGRES_PORT')
db_name:str = os.getenv('POSTGRES_DB')

engine = db.create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
    )
#

Session = scoped_session( sessionmaker(bind=engine) )
session = Session()

#connection = engine.connect()
metadata = db.MetaData()

db_hotel = db.Table('scraper_hotel', metadata, autoload=True, autoload_with=engine)
db_room = db.Table('scraper_room', metadata, autoload=True, autoload_with=engine)


db_review = db.Table('scraper_review', metadata, autoload=True, autoload_with=engine)
db_commentary = db.Table('scraper_commentary', metadata, autoload=True, autoload_with=engine)

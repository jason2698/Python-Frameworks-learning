from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql+psycopg2://postgres:Jason%402698@localhost:5432/jason"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
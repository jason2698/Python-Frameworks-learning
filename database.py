from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql+psycopg2://postgres:Krya%401234@localhost:5432/jason"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
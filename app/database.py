#db file
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///csv_data.db"
engine = create_engine("sqlite:///csv_data.db", echo=False)
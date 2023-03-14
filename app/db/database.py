import databases
import sqlalchemy
import os
from dotenv import load_dotenv
load_dotenv('./.env')

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")

DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)

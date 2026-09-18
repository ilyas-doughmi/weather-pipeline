import pandas as pd
from dotenv import load_dotenv
import os
import sqlalchemy

load_dotenv()

def readCSV(path):
    return pd.read_csv(path)

def connect():
    conn = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    print("connected")
    return conn


if __name__ == "__main__":
    connect()
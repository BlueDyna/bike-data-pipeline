import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")  # bv. postgresql://user:pass@host/dbname

df = pd.read_csv("transformed.csv")

engine = create_engine(DATABASE_URL)

df.to_sql("traffic_data", engine, if_exists="append", index=False)

print(f"Loaded {len(df)} rows into traffic_data")
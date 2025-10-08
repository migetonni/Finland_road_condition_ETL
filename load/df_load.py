import pandas as pd
import os
from supabase import create_client, Client
from sqlalchemy import create_engine
from dotenv import load_dotenv



load_dotenv()



def create_postgres_engine():
    user=os.getenv("USER")
    password=os.getenv("PASSWORD") 
    host=os.getenv("HOST")
    port=os.getenv("PORT")
    dbname=os.getenv("DBNAME")
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(connection_string)
    return engine
    


def load_tracks_postgres(df):
    
    engine = create_postgres_engine()
    try:
            # Load data using to_sql
            df.to_sql(
                name='road_sections',
                con=engine,
                if_exists='replace',
                index=False,
                method='multi',
                chunksize=5000
            )
            
            
            return True
            
    except Exception as e:
        print(f"Error loading to PostgreSQL: {e}")
        return False
import pandas as pd
import os
from sqlalchemy import create_engine, text
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
    
ENGINE = create_postgres_engine()

def load_tracks_postgres(df):
    if df.empty:
        raise ValueError("DataFrame is empty aborting load.")


    try:
         with ENGINE.begin() as connection:
            # Remove all old data since we only need the latest data in our use case
            connection.execute(text("TRUNCATE TABLE road_sections"))

            # Insert fresh data
            df.to_sql(
                name="road_sections",
                con=connection,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=5000
            )
            
            
    
            
    except Exception as e:
        raise RuntimeError("Failed to load data into PostgreSQL") from e
    return len(df)
        
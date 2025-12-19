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

def load_tracks_postgres(
    road_df,
    forecast_df,
    precipitation_df,
    road_condition_df,
    overall_condition_df,
    reliability_df,
):

    if road_df.empty or forecast_df.empty:
        raise ValueError("DataFrame is empty aborting load.")


    try:
         with ENGINE.begin() as connection:
            # Remove all old data since we only need the latest data in our use case
            connection.execute(text("TRUNCATE TABLE road_forecasts, road_sections, precipitation_types, road_condition_types, overall_road_condition_types, reliability_types"))
            


            # Insert fresh data
            precipitation_df.to_sql(
                name="precipitation_types",
                con=connection,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=5000,
            )

            road_condition_df.to_sql(
                name="road_condition_types",
                con=connection,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=5000,
            )

            overall_condition_df.to_sql(
                name="overall_road_condition_types",
                con=connection,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=5000,
            )

            reliability_df.to_sql(
                name="reliability_types",
                con=connection,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=5000,
            )

            # Load road sections
            road_df.to_sql(
                name="road_sections",
                con=connection,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=5000,
            )

            # Load forecasts last
            forecast_df.to_sql(
                name="road_forecasts",
                con=connection,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=5000,
            )         
            
    
            
    except Exception as e:
        import traceback
        print("LOAD FAILED. Underlying exception:")
        traceback.print_exc()

        # If it's a SQLAlchemy DBAPI error, print original DB error too
        try:
            orig = getattr(e, "orig", None)
            if orig is not None:
                print("DBAPI orig error:", repr(orig))
        except Exception:
            pass

        raise

    return {
        "road_sections": len(road_df),
        "road_forecasts": len(forecast_df),
        "precipitation_types": len(precipitation_df),
        "road_condition_types": len(road_condition_df),
        "overall_road_condition_types": len(overall_condition_df),
        "reliability_types": len(reliability_df),
    }
        
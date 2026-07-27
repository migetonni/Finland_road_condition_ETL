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

def load_domain_table(
    connection,
    table_name,
    column_name,
    values
):
 





    statement = text(f"""
        INSERT INTO {table_name} ({column_name})
        VALUES (:value)
        ON CONFLICT DO NOTHING
    """)

    connection.execute(
        statement,
        [{"value": v} for v in values]
    )


def load_tracks_postgres(
    road_df,
    forecast_df,
    precip, 
    road_cond, 
    overall_cond, 
    reliability
):

    if road_df.empty or forecast_df.empty:
        raise ValueError("DataFrame is empty aborting load.")


    try:
         with ENGINE.begin() as connection:
            # Remove all old data since we only need the latest data in our use case
            connection.execute(text("TRUNCATE TABLE road_forecasts, road_sections"))
            


            # Insert domain data with helper function
            load_domain_table(connection, "precipitation_types", "precipitation_condition", precip)
            load_domain_table(connection, "road_condition_types", "road_condition", road_cond)
            load_domain_table(connection, "overall_road_condition_types", "overall_road_condition", overall_cond)
            load_domain_table(connection, "reliability_types", "reliability", reliability)





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
            
            #load persistent historical data
            forecast_df.to_sql(
                name="historical_road_conditions",
                con=connection,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=5000,
            )

            
            connection.execute(text("""
                UPDATE road_forecasts rf
                SET datetime_key = dt.datetime_key
                FROM datetime dt
                WHERE rf.datetime_key IS NULL
                AND date_trunc('hour', rf.forecast_time) = dt.full_timestamp;
            """))
            
    
            
    except Exception as e:
        print("LOAD ERROR:", e)
        raise


    return {
        "road_sections": len(road_df),
        "road_forecasts": len(forecast_df),
        "precipitation_types": len(precip),
        "road_condition_types": len(road_cond),
        "overall_road_condition_types": len(overall_cond),
        "reliability_types": len(reliability),
    }
        
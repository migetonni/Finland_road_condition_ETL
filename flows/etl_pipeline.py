import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prefect import flow, task, get_run_logger
from extract.road_condition_extract import load_street_forecast
from load.df_load import load_tracks_postgres
from transform.transform_df import transform_track_df

@task(retries=3, retry_delay_seconds=10)
def extract_task():
    return load_street_forecast()

@task
def transform_task(df):
    if df.empty:
        raise RuntimeError("df is empty")
    return transform_track_df(df)  

@task(retries=3, retry_delay_seconds=10)
def load_task(df):
    load_tracks_postgres(df)  

@flow
def main():
    logger = get_run_logger()
    df = extract_task()
    df_clean = transform_task(df)
    
    
    load_task(df_clean)
    logger.info(f"Loaded {load_task} rows into PostgreSQL")

if __name__ == "__main__":
    main()

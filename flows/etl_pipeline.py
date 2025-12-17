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
def transform_task(road_df, forecast_df):
    if road_df.empty or forecast_df.empty:
        raise RuntimeError("df is empty")
    return transform_track_df(road_df, forecast_df)  

@task(retries=3, retry_delay_seconds=10)
def load_task(road_df, forecast_df):
    return load_tracks_postgres(road_df, forecast_df)  

@flow
def main():
    logger = get_run_logger()

    road_df, forecast_df = extract_task()
    road_df_clean, forecast_df_clean = transform_task(road_df, forecast_df)
    load_task(road_df_clean, forecast_df_clean)
    logger.info(f"Loaded {load_task} rows into PostgreSQL")

if __name__ == "__main__":
    main()

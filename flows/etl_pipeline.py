import sys
import os
from datetime import datetime, timezone
import pytz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prefect import flow, task, get_run_logger
from prefect.runtime import flow_run
from extract.road_condition_extract import load_street_forecast
from load.df_load import load_tracks_postgres, ENGINE
from load.etl_metadata_load import load_etl_metadata
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
def load_task(
    road_df,
    forecast_df,
    precipitation_df,
    road_condition_df,
    overall_condition_df,
    reliability_df,
):
    return load_tracks_postgres(
        road_df,
        forecast_df,
        precipitation_df,
        road_condition_df,
        overall_condition_df,
        reliability_df,
    ) 

@flow
def main():
    logger = get_run_logger()
    run_id = str(flow_run.id)
    flow_name = flow_run.name

    current_time = datetime.now()
    timezone = pytz.timezone('Europe/Helsinki')
    started_at = timezone.localize(current_time)

    
    status = "SUCCESS"
    error_message = None
    try:
        road_df, forecast_df = extract_task()

        (road_df_clean, 
        forecast_df_clean, 
        precip, 
        road_cond, 
        overall_cond, 
        reliability) = transform_task(road_df, forecast_df)
        
        
        rows_loaded = load_task(
        road_df_clean,
        forecast_df_clean,
        precip, 
        road_cond, 
        overall_cond, 
        reliability
        )
    except Exception as e:
        status = "FAILED"
        error_message = str(e)
        raise
    finally:
        current_time = datetime.now()
        finished_at = timezone.localize(current_time)
        duration_seconds = int((finished_at - started_at).total_seconds())
        load_etl_metadata(ENGINE, run_id, flow_name, started_at, finished_at, status, duration_seconds, error_message)


    logger.info(f"Loaded {rows_loaded} rows into PostgreSQL")

if __name__ == "__main__":
    main()

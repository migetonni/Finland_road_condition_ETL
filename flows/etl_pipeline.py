import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prefect import flow, task
from extract.road_condition_extract import load_street_forecast
from load.df_load import load_tracks_postgres
from transform.transform_df import transform_track_df

@task
def extract_task():
    return load_street_forecast()

@task
def transform_task(df):
    return transform_track_df(df)  

@task
def load_task(df):
    load_tracks_postgres(df)  

@flow
def main():
    df = extract_task()
    df_clean = transform_task(df)
    print(df_clean.columns.tolist())
    
    load_task(df_clean)

if __name__ == "__main__":
    main()

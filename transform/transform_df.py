import pandas as pd
import json

def prepare_domain_dfs(forecast_df):

    precipitation_df = (
        forecast_df[["precipitation_condition"]]
        .dropna()
        .drop_duplicates()
    )

    road_condition_df = (
        forecast_df[["road_condition"]]
        .dropna()
        .drop_duplicates()
    )

    overall_condition_df = (
        forecast_df[["overall_road_condition"]]
        .dropna()
        .drop_duplicates()
    )

    reliability_df = (
        forecast_df[["reliability"]]
        .dropna()
        .drop_duplicates()
    )

    return (
        precipitation_df,
        road_condition_df,
        overall_condition_df,
        reliability_df,
    )


def ensure_unknown(df, col):
    return (
        pd.concat([df, pd.DataFrame({col: ["UNKNOWN"]})])
        .drop_duplicates()
        .reset_index(drop=True)
    )

 


def transform_track_df(road_df, forecast_df):

    #copy dataframes
    road_df = road_df.copy()
    forecast_df = forecast_df.copy()

    #time to datetime 

    forecast_df["forecast_time"] = pd.to_datetime(forecast_df["forecast_time"], utc=True)
    #dropping duplicates
    road_df = road_df.drop_duplicates(subset=["section_id"], keep="last")
    forecast_df = forecast_df.drop_duplicates(subset=["section_id", "forecast_time", "road_condition"], keep="last")
    



    #transforming the contents of the coordinates columns to json  string so no index of different sizes errors in the load phase
    if "coordinates" in road_df.columns:
        road_df["coords_json"] =road_df["coordinates"].apply(lambda x: json.dumps(x))

        road_df = road_df.drop(columns=["coordinates"])

    #drop rows with old information since we only want the latest road condition data
    forecast_times = ['0h', '2h', '4h', '6h']

    forecast_df = forecast_df[forecast_df["forecast_name"].isin(forecast_times)]

    road_df["road_number"] = (
            road_df["section_id"]
            .str.split("_")
            .str[0]
            .astype("Int64")
        )
    
    for col in [
    "road_condition",
    "precipitation_condition",
    "overall_road_condition",
    "reliability",
    ]:
        forecast_df[col] = forecast_df[col].fillna("UNKNOWN")
    

    def road_classifier(num):
        if pd.isna(num):
            return "unknown"
        if num < 40:
            return "mainRoad"
        elif num > 39 and num < 100:
            
            return "secondaryRoad"
        else:
            return "minorRoad"
        
    road_df["road_type"] = road_df["road_number"].apply(road_classifier)

    #create dataframes for domains for our sql schema
    precipitation_df, road_condition_df, overall_condition_df, reliability_df = prepare_domain_dfs(forecast_df)
    precipitation_df = ensure_unknown(precipitation_df, "precipitation_condition")
    road_condition_df = ensure_unknown(road_condition_df, "road_condition")
    overall_condition_df = ensure_unknown(overall_condition_df, "overall_road_condition")
    reliability_df = ensure_unknown(reliability_df, "reliability")

    
    
    

    return road_df, forecast_df, precipitation_df, road_condition_df, overall_condition_df, reliability_df
    





    

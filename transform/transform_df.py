import pandas as pd
import json

def transform_track_df(road_df, forecast_df):

    #copy dataframes
    road_df = road_df.copy()
    forecast_df = forecast_df.copy()

    #dropping duplicates

    road_df = road_df.drop_duplicates(subset=["section_id"], keep="last")
    forecast_df = forecast_df.drop_duplicates(subset=["section_id","forecast_time"], keep="last")

    #time to datetime 
    forecast_df["forecast_time"] = pd.to_datetime(forecast_df["forecast_time"], utc=True)


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

    
    
    

    return road_df, forecast_df
    





    
